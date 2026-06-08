# Diagnóstico Agropecuário — Semiárido Mineiro (1985–2024)

Pipeline ETL para análise histórica da agropecuária em 217 municípios do semiárido
de Minas Gerais, com dados extraídos da API SIDRA/IBGE e armazenados em PostgreSQL.

## Volumetria

| Dimensão | Valor |
|----------|-------|
| Municípios analisados | 217 (delimitação oficial do Semiárido) |
| Série histórica | 40 anos (1985–2024) |
| Registros processados | ~8.682 linhas por cultura e rebanho |
| Granularidade | Anual |

## Pipeline ETL

**Extração** — Consumo da API SIDRA/IBGE para rebanhos e lavouras

**Transformação** — Limpeza, tratamento de nulos e estruturação tabular via Pandas

**Carga** — Ingestão automatizada em PostgreSQL com credenciais via variáveis de ambiente

**Análise** — Queries SQL para identificar padrões de crescimento e transição produtiva

## Estrutura do repositório

| Arquivo | Descrição |
|---------|-----------|
| `main.py` | Extração e carga |
| `analise.sql` | Queries analíticas |
| `.env.example` | Modelo de configuração do banco |
| `MUN_SEMIARIDO_MG.csv` | Base de municípios para filtro |

## Resultado

A análise evidencia a migração de culturas de subsistência para grandes rebanhos bovinos
ao longo de quase 40 anos, permitindo compreender padrões de transição econômica e
produtiva no semiárido mineiro.

---

**Stack:** Python · Pandas · Requests · PostgreSQL · API SIDRA/IBGE
