# 🚜 Análise da Evolução Agropecuária - Semiárido Mineiro (1985-2024)

Este projeto realiza o processo de **ETL (Extract, Transform, Load)** de dados históricos da agropecuária em municípios do semiárido de Minas Gerais, utilizando a API do IBGE (SIDRA).

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.x
* **Bibliotecas:** `requests` (API), `pandas` (Tratamento de dados), `python-dotenv` (Segurança)
* **Banco de Dados:** PostgreSQL (Armazenamento e consultas analíticas)
* **Segurança:** Uso de variáveis de ambiente para proteção de credenciais.

## 📋 Funcionalidades
1. **Extração Automática:** Consome dados da API SIDRA/IBGE sobre rebanhos e lavouras.
2. **Transformação de Dados:** Limpeza, tratamento de valores nulos e estruturação tabular via Pandas.
3. **Carga (Load):** Ingestão automatizada no banco de dados PostgreSQL.
4. **Análise SQL:** Consultas complexas para identificar o crescimento da pecuária e agricultura na região ao longo de quase 40 anos.

## 📊 Abrangência e Volumetria de Dados
Este projeto processa uma base de dados robusta e histórica, garantindo uma análise profunda do Semiárido Mineiro:

* **Municípios Analisados:** 217 cidades mineiras integrantes da delimitação oficial do Semiárido.
* **Série Histórica:** 40 anos de dados evolutivos (1985–2024).
* **Escalabilidade:** Processamento de aproximadamente 8.682 linhas de registros detalhados por cultura e rebanho.
* **Granularidade:** Dados anuais que permitem identificar padrões de transição econômica e produtiva na região.

## 📂 Estrutura do Projeto
* `main.py`: Script principal de extração e carga.
* `analise.sql`: Queries analíticas para extração de insights do banco.
* `.env.example`: Modelo de configuração para conexão com o banco de dados.
* `MUN_SEMIARIDO_MG.csv`: Base de municípios utilizada no filtro da análise.

## 📈 Conclusões da Análise (SQL)
O projeto permite identificar, por exemplo, a migração de culturas de subsistência para grandes rebanhos bovinos, auxiliando na compreensão do impacto econômico no semiárido mineiro.