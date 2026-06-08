# Pharma Intelligence BR — Inteligência Territorial Farmacêutica

![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)
![Python](https://img.shields.io/badge/Backend-Python_3.12-blue)
![JavaScript](https://img.shields.io/badge/Frontend-Vanilla_JS-yellow)

**Dashboard:** [Explore o Painel Interativo](https://milenamonteirofeitosa.github.io/portfolio_dados/pharma-intelligence/)

---

## Sobre o projeto

Aplicação full-stack de Business Intelligence para apoio a decisões estratégicas no varejo
farmacêutico brasileiro. A ferramenta cruza dados de consumo com variáveis sociodemográficas
e de infraestrutura de saúde para identificar **"Oceanos Azuis"** — mercados com alto poder
de compra, demanda reprimida e baixa saturação competitiva.

## Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| Análise de saturação | Densidade de farmácias por 100 mil habitantes com dados oficiais atualizados |
| Matriz de correlação | Cruzamento entre renda *per capita* (IBGE) e volume de estabelecimentos (CNES) |
| Smart Insights | Motor de regras em JavaScript que interpreta o cenário analítico em tempo real |
| Rankings e heatmaps | Classificação das 27 UFs em quadrantes: Prioridade, Consolidado, Emergente, Eficiente |

## Arquitetura

**Backend — Engenharia de dados**
- `Python & Pandas` — pipeline ETL para extração, limpeza e cruzamento de bases governamentais massivas (centenas de MB), com tratamento de erros de tipagem e inconsistências
- `FastAPI` — rotas API locais para servir os dados consolidados
- *Data Freezing* para deployment estático

**Frontend — Visualização**
- `HTML5 / CSS3 / Vanilla JS` — interface dark mode sem dependência de bibliotecas externas de gráficos; renderização nativa via CSS Grid/Flexbox

## Fontes de dados

| Fonte | Dados | Referência |
|-------|-------|------------|
| Ministério da Saúde / CNES | Estabelecimentos ativos tipo "Farmácia" (Código 43) | Fev/2026 |
| IBGE — Censo 2022 | População residente + rendimento domiciliar mediano *per capita* (Tab. 10295 e 1209) | 2022 |
| ANVISA / SNGPC | Microdados de vendas de medicamentos por princípio ativo, faixa etária e sexo | Q1/2026 |

---

**Stack:** Python · Pandas · FastAPI · JavaScript · HTML5 · CSS3
