from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import csv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mapeamentos para processar os ficheiros brutos do IBGE
UF_PARA_SIGLA = {
    'Acre': 'AC', 'Alagoas': 'AL', 'Amazonas': 'AM', 'Amapá': 'AP', 'Bahia': 'BA',
    'Ceará': 'CE', 'Distrito Federal': 'DF', 'Espírito Santo': 'ES', 'Goiás': 'GO',
    'Maranhão': 'MA', 'Minas Gerais': 'MG', 'Mato Grosso do Sul': 'MS', 'Mato Grosso': 'MT',
    'Pará': 'PA', 'Paraíba': 'PB', 'Pernambuco': 'PE', 'Piauí': 'PI', 'Paraná': 'PR',
    'Rio de Janeiro': 'RJ', 'Rio Grande do Norte': 'RN', 'Rondônia': 'RO', 'Roraima': 'RR',
    'Rio Grande do Sul': 'RS', 'Santa Catarina': 'SC', 'Sergipe': 'SE', 'São Paulo': 'SP',
    'Tocantins': 'TO'
}

REGIAO_MAP = {
    'AC': 'N', 'AM': 'N', 'AP': 'N', 'PA': 'N', 'RO': 'N', 'RR': 'N', 'TO': 'N',
    'AL': 'NE', 'BA': 'NE', 'CE': 'NE', 'MA': 'NE', 'PB': 'NE', 'PE': 'NE', 'PI': 'NE', 'RN': 'NE', 'SE': 'NE',
    'DF': 'CO', 'GO': 'CO', 'MS': 'CO', 'MT': 'CO',
    'ES': 'SE', 'MG': 'SE', 'RJ': 'SE', 'SP': 'SE',
    'PR': 'S', 'RS': 'S', 'SC': 'S'
}

# =====================================================================
# NOVO MOTOR: INTELIGÊNCIA IBGE DINÂMICA (Ficheiros Limpos)
# =====================================================================
def carregar_dados_reais_ibge():
    """Lê a população e o rendimento mediano dos ficheiros CSV do IBGE"""
    try:
        print("--- A processar Dados Oficiais do Censo 2022 ---")
        
        # 1. Carregar População (Ficheiro Limpo: Tabela 1209.csv)
        df_pop = pd.read_csv('Tabela 1209.csv', sep=';')
        df_pop['nome'] = df_pop['nome'].str.strip()
        df_pop = df_pop[df_pop['nome'].isin(UF_PARA_SIGLA.keys())]
        df_pop['uf'] = df_pop['nome'].map(UF_PARA_SIGLA)
        
        # 2. Carregar Rendimento Mediano (Ficheiro Limpo: Tabela 10295.csv)
        df_renda = pd.read_csv('Tabela 10295.csv', sep=';')
        df_renda['nome'] = df_renda['nome'].str.strip()
        df_renda = df_renda[df_renda['nome'].isin(UF_PARA_SIGLA.keys())]
        df_renda['uf'] = df_renda['nome'].map(UF_PARA_SIGLA)

        # 3. Consolidação e Limpeza
        df_unido = pd.merge(df_pop[['uf', 'pop']], df_renda[['uf', 'renda_mediana']], on='uf')
        
        resultado_dict = {}
        for _, row in df_unido.iterrows():
            uf = row['uf']
            # Limpeza de pontuação brasileira (ex: 1250,17 -> 1250.17)
            renda_str = str(row['renda_mediana']).replace('.', '').replace(',', '.')
            pop_str = str(row['pop']).replace('.', '')
            
            resultado_dict[uf] = {
                'renda': float(renda_str),
                'pop': int(pop_str),
                'reg': REGIAO_MAP.get(uf, 'N')
            }
        
        print(f"✓ {len(resultado_dict)} UFs carregadas com sucesso via IBGE CSV.")
        return resultado_dict
    except Exception as e:
        print(f"⚠️ Erro ao ler ficheiros do IBGE: {e}")
        return {}

# =====================================================================
# OUTROS MOTORES (CNES E ANVISA)
# =====================================================================
def carregar_vendas():
    try:
        print("--- A ler Vendas Anvisa (Mar/2026) ---")
        alvo = ['SG_SEXO', 'NU_IDADE', 'DS_PRINCIPIO_ATIVO', 'NO_CONSELHO_PRESCRITOR', 'QT_VENDIDA', 'SG_UF_VENDA']
        df = pd.read_csv("EDA_Industrializados_202603.csv", sep=";", usecols=alvo, encoding="latin1", low_memory=False, quoting=csv.QUOTE_NONE)
        for col in df.columns:
            df[col] = df[col].astype(str).str.replace('"', '', regex=False)
        df['NU_IDADE'] = df['NU_IDADE'].str.replace('.', '', regex=False)
        df['QT_VENDIDA'] = pd.to_numeric(df['QT_VENDIDA'], errors='coerce').fillna(0)
        df['NU_IDADE'] = pd.to_numeric(df['NU_IDADE'], errors='coerce').fillna(0)
        return df
    except Exception as e:
        print(f"Erro Anvisa: {e}")
        return pd.DataFrame()

def carregar_cnes():
    print("--- A procurar Farmácias no CNES (Fev/2026) ---")
    try:
        df_cnes = pd.read_csv("tbEstabelecimento202602.csv", sep=";", usecols=['TP_UNIDADE', 'CO_ESTADO_GESTOR'], dtype=str, encoding='latin1')
        df_farmacias = df_cnes[df_cnes['TP_UNIDADE'] == '43']
        contagem = df_farmacias.groupby('CO_ESTADO_GESTOR').size().reset_index(name='farma')
        
        # Mapeamento do código numérico IBGE para Sigla
        IBGE_PARA_UF = {
            '11': 'RO', '12': 'AC', '13': 'AM', '14': 'RR', '15': 'PA', '16': 'AP', '17': 'TO',
            '21': 'MA', '22': 'PI', '23': 'CE', '24': 'RN', '25': 'PB', '26': 'PE', '27': 'AL', '28': 'SE', '29': 'BA',
            '31': 'MG', '32': 'ES', '33': 'RJ', '35': 'SP',
            '41': 'PR', '42': 'SC', '43': 'RS',
            '50': 'MS', '51': 'MT', '52': 'GO', '53': 'DF'
        }
        contagem['uf'] = contagem['CO_ESTADO_GESTOR'].map(IBGE_PARA_UF)
        return dict(zip(contagem['uf'], contagem['farma']))
    except Exception as e:
        print(f"Erro no CNES: {e}")
        return {}

# INICIALIZAÇÃO DINÂMICA
DADOS_IBGE = carregar_dados_reais_ibge()
FARMACIAS_POR_UF = carregar_cnes()
df_vendas_mar = carregar_vendas()

# =====================================================================
# ROTAS DA API
# =====================================================================

@app.get("/api/dashboard")
async def get_vendas():
    if df_vendas_mar.empty: return {"erro": "Ficheiro Anvisa vazio"}
    caixas = int(df_vendas_mar['QT_VENDIDA'].sum())
    return {
        "kpis": {"caixas": f"{caixas:,}".replace(",", "."), "tendencia": "+12.4%"},
        "piramide": {"labels": [], "homens": [], "mulheres": []}
    }

@app.get("/api/expansao")
async def get_expansao():
    """Alimenta o dashboard de expansão com dados vivos do IBGE e CNES"""
    if not DADOS_IBGE:
        return {"erro": "Dados IBGE não carregados. Verifique os CSVs."}
        
    resultado = []
    for uf, dados in DADOS_IBGE.items():
        qtd_farma = FARMACIAS_POR_UF.get(uf, 0) 
        resultado.append({
            "uf": uf,
            "farma": int(qtd_farma),
            "renda": dados['renda'],
            "pop": dados['pop'],
            "reg": dados['reg']
        })
    return {"ufs": resultado}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)