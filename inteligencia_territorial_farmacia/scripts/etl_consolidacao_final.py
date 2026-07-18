import pandas as pd
import logging
from pathlib import Path

# Configuração de log
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# ==========================================
# DICIONÁRIOS DE MAPEAMENTO (Constantes)
# ==========================================
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

IBGE_PARA_UF = {
    '11': 'RO', '12': 'AC', '13': 'AM', '14': 'RR', '15': 'PA', '16': 'AP', '17': 'TO',
    '21': 'MA', '22': 'PI', '23': 'CE', '24': 'RN', '25': 'PB', '26': 'PE', '27': 'AL', '28': 'SE', '29': 'BA',
    '31': 'MG', '32': 'ES', '33': 'RJ', '35': 'SP',
    '41': 'PR', '42': 'SC', '43': 'RS',
    '50': 'MS', '51': 'MT', '52': 'GO', '53': 'DF'
}

def extrair_e_limpar_ibge(caminho_pop: Path, caminho_renda: Path) -> pd.DataFrame:
    """Extrai e limpa as tabelas de População e Rendimento do IBGE."""
    logging.info("Iniciando extração dos dados do IBGE...")
    
    # encoding='utf-8-sig' remove automaticamente o BOM (ï»¿) invisível do Windows
    df_pop = pd.read_csv(caminho_pop, sep=';', encoding='utf-8-sig', on_bad_lines='skip')
    df_pop.columns = df_pop.columns.str.strip()
    
    df_pop['nome'] = df_pop['nome'].astype(str).str.strip()
    df_pop = df_pop[df_pop['nome'].isin(UF_PARA_SIGLA.keys())].copy()
    df_pop['UF'] = df_pop['nome'].map(UF_PARA_SIGLA)
    
    df_pop['Populacao'] = df_pop['pop'].astype(str).str.replace('.', '', regex=False)
    df_pop['Populacao'] = pd.to_numeric(df_pop['Populacao'], errors='coerce')

    df_renda = pd.read_csv(caminho_renda, sep=';', encoding='utf-8-sig', on_bad_lines='skip')
    df_renda.columns = df_renda.columns.str.strip()
    
    df_renda['nome'] = df_renda['nome'].astype(str).str.strip()
    df_renda = df_renda[df_renda['nome'].isin(UF_PARA_SIGLA.keys())].copy()
    df_renda['UF'] = df_renda['nome'].map(UF_PARA_SIGLA)
    
    df_renda['RendimentoMediano'] = df_renda['renda_mediana'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
    df_renda['RendimentoMediano'] = pd.to_numeric(df_renda['RendimentoMediano'], errors='coerce')

    # Merge População + Renda
    df_ibge = pd.merge(df_pop[['UF', 'Populacao']], df_renda[['UF', 'RendimentoMediano']], on='UF', how='left')
    return df_ibge

def extrair_e_limpar_cnes(caminho_cnes: Path) -> pd.DataFrame:
    """Extrai a base do CNES, filtra farmácias e agrupa por UF."""
    logging.info("Iniciando extração e filtragem do CNES (DATASUS)...")
    
    df_cnes = pd.read_csv(
        caminho_cnes, 
        sep=";", 
        usecols=['TP_UNIDADE', 'CO_ESTADO_GESTOR'], 
        dtype=str, 
        encoding='latin1'
    )
    
    df_farmacias = df_cnes[df_cnes['TP_UNIDADE'] == '43']
    df_farma_agrupado = df_farmacias.groupby('CO_ESTADO_GESTOR').size().reset_index(name='TotalFarmacias')
    df_farma_agrupado['UF'] = df_farma_agrupado['CO_ESTADO_GESTOR'].map(IBGE_PARA_UF)
    
    return df_farma_agrupado[['UF', 'TotalFarmacias']]

def consolidar_e_exportar(df_ibge: pd.DataFrame, df_cnes: pd.DataFrame, caminho_saida: Path) -> None:
    """Cruza os dados do IBGE com o CNES e exporta o CSV final."""
    logging.info("Iniciando o cruzamento (Merge) das bases...")
    
    df_final = pd.merge(df_ibge, df_cnes, on='UF', how='left')
    df_final['TotalFarmacias'] = df_final['TotalFarmacias'].fillna(0).astype(int)
    df_final['Regiao'] = df_final['UF'].map(REGIAO_MAP)
    
    df_final = df_final[['UF', 'Regiao', 'Populacao', 'RendimentoMediano', 'TotalFarmacias']]

    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    df_final.to_csv(caminho_saida, sep=';', index=False, encoding='utf-8-sig', decimal=',')
    logging.info(f"Arquivo final exportado com sucesso para: {caminho_saida}")

if __name__ == "__main__":
    # ==========================================
    # CONFIGURAÇÃO DE CAMINHOS COM PATHLIB
    # ==========================================
    BASE_DIR = Path(__file__).resolve().parent
    DIR_RAW = BASE_DIR.parent / "raw"
    DIR_PROC = BASE_DIR.parent / "processed"
    
    POP_FILE = DIR_RAW / "Tabela_1209.csv"
    RENDA_FILE = DIR_RAW / "Tabela_10295.csv"
    CNES_FILE = DIR_RAW / "tbEstabelecimento202602.csv"
    OUTPUT_FILE = DIR_PROC / "Dados_Inteligencia_Territorial.csv"
    
    logging.info(f"Procurando arquivos em: {DIR_RAW}")
    
    try:
        df_ibge = extrair_e_limpar_ibge(POP_FILE, RENDA_FILE)
        df_cnes = extrair_e_limpar_cnes(CNES_FILE)
        consolidar_e_exportar(df_ibge, df_cnes, OUTPUT_FILE)
    except Exception as e:
        logging.error(f"Falha no pipeline ETL: {e}")