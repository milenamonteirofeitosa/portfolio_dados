# 🧬 Pharma Intelligence BR | Inteligência Territorial Farmacêutica

![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)
![Python](https://img.shields.io/badge/Backend-Python_3.12-blue)
![JavaScript](https://img.shields.io/badge/Frontend-Vanilla_JS-yellow)

🌐 **Dashboard:** [Explore o Painel Interativo de Inteligência Territorial](https://milenamonteirofeitosa.github.io/portfolio_dados/pharma-intelligence/)

## 📊 Sobre o Projeto
Este projeto é uma aplicação *Full-Stack* de Business Intelligence (BI) desenvolvida para apoiar decisões estratégicas de nível executivo no varejo farmacêutico brasileiro. 

Em vez de focar apenas no passado (Sell-Out), a ferramenta cruza dados de consumo com variáveis sociodemográficas e de infraestrutura de saúde para identificar **"Oceanos Azuis"** — mercados com alto poder de compra, demanda reprimida e baixa saturação da concorrência.

### 🎯 Principais Funcionalidades
* **Análise de Saturação (Market Share Real):** Cálculo de densidade de farmácias por 100 mil habitantes utilizando dados oficias e atualizados.
* **Matriz de Correlação (Scatter Plot):** Cruzamento entre Renda *per capita* (IBGE) e volume de estabelecimentos (CNES) para encontrar assimetrias de mercado.
* **Smart Insights (Textos Dinâmicos):** Um motor de regras em JavaScript que lê os dados em tempo real e escreve a interpretação analítica do cenário automaticamente.
* **Mapas de Calor (Heatmaps) e Rankings:** Classificação automática das 27 Unidades Federativas em quadrantes de investimento (Prioridade, Consolidado, Emergente, Eficiente).

## 🛠️ Arquitetura e Tecnologias
O projeto foi construído para lidar de forma eficiente com bases de dados governamentais massivas, utilizando o conceito de *Data Freezing* para o deployment estático.

**Engenharia de Dados (Backend):**
* **Python & Pandas:** Scripts pesados (`main.py`) desenvolvidos para extrair, limpar e cruzar milhões de linhas de dados brutos (ETL), filtrando erros de tipagem e resolvendo inconsistências em bases de centenas de Megabytes.
* **FastAPI:** Criação de rotas API locais para servir os dados consolidados.

**Visualização (Frontend):**
* **HTML5 / CSS3 / Vanilla JS:** Design executivo *Dark Mode / Cyberpunk*, focado em UI/UX de alta performance sem dependência de bibliotecas pesadas de gráficos. Tudo renderizado nativamente ou via CSS Grid/Flexbox.

## 🗄️ Fontes de Dados (Data Sources)
Todos os dados utilizados são públicos e oficiais:
1. **Ministério da Saúde / CNES (Fevereiro/2026):** Extração do Cadastro Nacional de Estabelecimentos de Saúde, filtrando exclusivamente estabelecimentos ativos do tipo "Farmácia" (Código 43).
2. **IBGE (Censo Demográfico 2022):** Tabelas 10295 e 1209. Extração da População residente e cruzamento com o Rendimento domiciliar mensal per capita nominal mediano, garantindo uma leitura precisa do poder de compra da maioria populacional, sem distorção por extremos de riqueza.
3. **ANVISA / SNGPC (Q1 2026):** Microdados de vendas de medicamentos industrializados para modelagem do perfil de consumo por princípio ativo, faixa etária e sexo.

