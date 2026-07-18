import pandas as pd
import logging
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os
from pathlib import Path

# Configuração de log
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def carregar_para_postgres(caminho_csv: Path):
    """Carrega os dados de um CSV para uma tabela no PostgreSQL."""
    logging.info("Iniciando processo de carga para o banco de dados...")

    try:
        # 1. Carrega o CSV
        df = pd.read_csv(caminho_csv, sep=';')
        logging.info(f"CSV carregado. {len(df)} linhas encontradas.")

        # 2. Configura os parâmetros de conexão usando variáveis de ambiente (SEGURANÇA)
        # Se não encontrar a variável, usa um valor padrão seguro ou levanta erro
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5433")
        db_name = os.getenv("DB_NAME", "farmacia_expansao")

        if not db_password:
            raise ValueError("A variável de ambiente DB_PASSWORD não foi definida no arquivo .env")

        conexao_url = URL.create(
            drivername="postgresql",
            username=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_name
        )

        # 3. Cria o motor de conexão
        engine = create_engine(conexao_url)

        # 4. Envia os dados para o PostgreSQL
        # if_exists='replace' apaga a tabela e recria. 
        # index=False não cria a coluna de índice do pandas no banco.
        df.to_sql('inteligencia_territorial', engine, if_exists='replace', index=False)
        
        logging.info("Migração concluída com sucesso! Dados enviados para a tabela 'inteligencia_territorial'.")

    except Exception as e:
        logging.error(f"Falha ao carregar dados para o PostgreSQL: {e}")

if __name__ == "__main__":
    # Pega o diretório onde este script está rodando
    BASE_DIR = Path(__file__).resolve().parent
    
    # Como o script está em .../data/scripts/, 
    # BASE_DIR.parent aponta para .../data/.
    # Logo, só precisamos entrar em "processed"
    CSV_FILE = BASE_DIR.parent / "processed" / "Dados_Inteligencia_Territorial.csv"
    
    carregar_para_postgres(CSV_FILE)