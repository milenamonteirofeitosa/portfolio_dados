# Análise do PIB Municipal — Ceará via API SIDRA/IBGE

Script Python para consulta automatizada à API do SIDRA/IBGE, obtendo dados de
PIB *per capita* dos municípios do Ceará (UF 23) com exportação para CSV ou Excel.

## Requisitos

```bash
pip install pandas requests openpyxl
```

## Como executar

```bash
python PIB_analise.py
```

O script consulta a API, processa os dados e pergunta:

```bash
Deseja salvar os dados? (csv/excel/nenhum):
```

## Estrutura do código

| Função | Responsabilidade |
|--------|-----------------|
| `consultar_api_sidra()` | Requisição HTTP à API SIDRA — Tabela 5938 |
| `processar_dados()` | Transforma JSON em DataFrame, filtra Ceará e trata inconsistências |
| `salvar_dados()` | Exporta no formato escolhido pelo usuário |
| `main()` | Orquestra o fluxo: consulta → processamento → exibição → salvamento |

## Resultado — Top 5 municípios por PIB (2021)

| Município | PIB 2021 (R$ mil) |
|-----------|-------------------|
| Fortaleza | 73.436.128 |
| Maracanaú | 12.337.017 |
| Caucaia | 10.414.373 |
| São Gonçalo do Amarante | 8.633.637 |
| Sobral | 5.395.130 |

*Fonte: SIDRA/IBGE — [Tabela 5938](https://apisidra.ibge.gov.br/)*

---

**Stack:** Python · Pandas · Requests · API SIDRA/IBGE
