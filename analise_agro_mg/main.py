import pandas as pd
import requests
import time
import urllib.parse
from sqlalchemy import create_engine
import os
import psycopg2
from dotenv import load_dotenv  # Biblioteca para carregar o .env

# --- 1. CARREGAR CONFIGURAÇÕES SEGURAS ---
load_dotenv()  # Lê o arquivo .env da pasta

USUARIO = os.getenv('DB_USER')
SENHA = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST')
PORTA = os.getenv('DB_PORT')
BANCO_ALVO = os.getenv('DB_NAME')

# Caminho do CSV permanece fixo (ou pode colocar no .env também)
CAMINHO_CSV = r"C:\pasta_dados_portfolio\projeto_semiárido\MUN_SEMIARIDO_MG.csv"

# Trata caracteres especiais na senha (como o @)
SENHA_SAFE = urllib.parse.quote_plus(SENHA)

# IDs das culturas na Tabela 5457 do IBGE
CULTURAS = {
    '40102': 'arroz',      # Arroz (em casca)
    '40112': 'feijao',     # Feijão (em grão)
    '40119': 'mandioca',   # Mandioca
    '40122': 'milho',      # Milho (em grão)
    '40139': 'cafe'        # Café (em grão) Total
}

def criar_banco_se_nao_existe():
    try:
        conn = psycopg2.connect(dbname='postgres', user=USUARIO, password=SENHA, host=HOST, port=PORTA)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{BANCO_ALVO}'")
        if not cursor.fetchone():
            print(f"💎 Criando banco de dados '{BANCO_ALVO}'...")
            cursor.execute(f"CREATE DATABASE {BANCO_ALVO}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠️ Erro ao verificar banco: {e}")

def extrair_dados_lote(tabela, variavel, classificacao, lista_geocodes, anos="1985-2024"):
    df_acumulado = pd.DataFrame()
    for i in range(0, len(lista_geocodes), 50):
        lote = lista_geocodes[i:i + 50]
        lote_str = ",".join(lote)
        url = (f"https://servicodados.ibge.gov.br/api/v3/agregados/{tabela}/periodos/{anos}/"
               f"variaveis/{variavel}?localidades=N6[{lote_str}]&classificacao={classificacao}")
        try:
            r = requests.get(url, timeout=60)
            data = r.json()
            registros = []
            if data and 'resultados' in data[0]:
                for serie in data[0]['resultados'][0]['series']:
                    g_id, g_nome = serie['localidade']['id'], serie['localidade']['nome']
                    for ano, val in serie['serie'].items():
                        # Limpeza de valores nulos do IBGE
                        val_limpo = float(val) if val not in [None, '..', '-', '...'] else 0
                        registros.append({'geocode': str(g_id), 'municipio': g_nome, 'ano': int(ano), 'valor': val_limpo})
            df_acumulado = pd.concat([df_acumulado, pd.DataFrame(registros)], ignore_index=True)
            time.sleep(0.5) # Pausa para evitar bloqueio da API
        except Exception as e:
            print(f"  [ERRO] Tabela {tabela}, Var {variavel}: {e}")
    return df_acumulado

def main():
    criar_banco_se_nao_existe()
    
    print(f"📖 Lendo municípios em: {CAMINHO_CSV}")
    df_ref = pd.read_csv(CAMINHO_CSV, sep=';')
    lista_geocodes = df_ref['CODIGO'].astype(str).tolist()

    # 1. Iniciar com os dados de Pecuária
    print("🐄 Coletando Efetivo Bovino (1985-2024)...")
    df_final = extrair_dados_lote(3939, 105, "79[2670]", lista_geocodes).rename(columns={'valor': 'efetivo_bovino'})

    # 2. Coletar Área e Valor para cada cultura
    for id_ibge, nome_cultura in CULTURAS.items():
        print(f"🌾 Processando: {nome_cultura.upper()}...")
        
        # Área Colhida (Variável 216)
        df_area = extrair_dados_lote(5457, 216, f"782[{id_ibge}]", lista_geocodes)
        df_area = df_area.rename(columns={'valor': f'area_colhida_{nome_cultura}'})
        
        # Valor da Produção (Variável 215)
        df_valor = extrair_dados_lote(5457, 215, f"782[{id_ibge}]", lista_geocodes)
        df_valor = df_valor.rename(columns={'valor': f'valor_producao_{nome_cultura}'})

        # Unir ao DataFrame principal
        df_final = df_final.merge(df_area, on=['geocode', 'municipio', 'ano'], how='outer')
        df_final = df_final.merge(df_valor, on=['geocode', 'municipio', 'ano'], how='outer')

    # 3. Enviar para o PostgreSQL
    engine = create_engine(f'postgresql://{USUARIO}:{SENHA_SAFE}@{HOST}:{PORTA}/{BANCO_ALVO}')
    try:
        # Criando uma nova tabela para não misturar com a anterior
        df_final.to_sql('tbl_detalhada_culturas_agro_mg', engine, if_exists='replace', index=False)
        print(f"🚀 Sucesso! Dados de 1985-2024 salvos na tabela 'tbl_detalhada_culturas_agro_mg'.")
    except Exception as e:
        print(f"❌ Erro ao salvar no banco: {e}")

if __name__ == "__main__":
    main()