# Inteligência Territorial Farmacêutica: Dashboard de Expansão de Mercado

Este projeto consiste em um pipeline de dados completo (End-to-End) e um painel de Business Intelligence (BI) avançado, desenvolvido para mapear o potencial de mercado farmacêutico em todo o território brasileiro. A solução cruza dados demográficos (IBGE) com dados de estabelecimentos de saúde (CNES/DATASUS) para identificar gaps de mercado e classificar o potencial de expansão por Unidade Federativa (UF).

![Demonstração do Dashboard](https://raw.githubusercontent.com/milenamonteirofeitosa/portfolio_dados/main/inteligencia_territorial_farmacia/dashboards/video_demonstracao.gif)

## Contexto do Problema

Redes farmacêuticas em processo de expansão enfrentam o desafio de identificar onde abrir novas lojas sem canibalizar o próprio mercado ou entrar em regiões saturadas. O objetivo deste projeto foi criar uma ferramenta analítica que classificasse as UFs não apenas pelo número absoluto de farmácias, mas pela densidade demográfica ajustada pela renda mediana da população.

## Pipeline de Dados (ETL com Python & PostgreSQL)

Antes da construção do dashboard, os dados foram extraídos, limpos e consolidados utilizando Python (Pandas) e armazenados em um banco de dados relacional.

* **Ingestão e Limpeza:** Extração de tabelas brutas do IBGE (SIDRA) e CNES (DATASUS), tratando problemas de encoding (Latin1/UTF-8), separadores decimais e otimização de memória (usecols e dtype).

* **Transformação:** Cruzamento (Merge) das bases demográficas com a contagem de estabelecimentos de saúde (filtro por código 43 - Farmácias), criando um modelo de dados enxuto.

* **Carga (Loading):** Inserção segura dos dados tratados em um banco de dados PostgreSQL utilizando SQLAlchemy, servindo como Source of Truth para o Power BI. (As credenciais são gerenciadas via variáveis de ambiente .env).

# Metodologia e Lógica de Negócios

O painel do Power BI foi estruturado em 4 visões principais (abas), utilizando uma lógica de classificação de mercado desenvolvida do zero:

* **Visão Geral:** KPIs nacionais, ranking de volume absoluto e mapa de calor de densidade farmacêutica (Lojas/100k habitantes).

* **Correlação:** Gráfico de dispersão cruzando População vs. Total de Farmácias para identificar outliers territoriais.

* **Ranking UF:** Tabela detalhada com a classificação algorítmica de potencial de cada estado.

* **Sinais de Expansão:** Filtro automático que destaca apenas as UFs com densidade inferior a 25 farmácias/100k hab., classificando-as como "Oportunidade Premium" (renda > R$ 1.000) ou "Mercado Emergente".

### Regra de Classificação (Algoritmo):

&nbsp;&nbsp;&nbsp;&nbsp;**Saturado:** Densidade >= 25 e Renda <= R$ 1.000<br>
&nbsp;&nbsp;&nbsp;&nbsp;**Consolidado:** Densidade >= 25 e Renda > R$ 1.000<br>
&nbsp;&nbsp;&nbsp;&nbsp;**Emergente:** Densidade < 25 e Renda <= R$ 1.000<br>
&nbsp;&nbsp;&nbsp;&nbsp;**Oportunidade Premium:** Densidade < 25 e Renda > R$ 1.000<br>
  
## Stack Tecnológico e Implementação Técnica

Este projeto destaca-se pelo uso de técnicas avançadas de Engenharia de Dados e Desenvolvimento BI:

* **Backend/ETL:** Python (Pandas, SQLAlchemy), PostgreSQL.

* **Power BI Desktop & DAX:** Criação de medidas complexas utilizando funções de iteração (CONCATENATEX), manipulação de variáveis (VAR) e formatação condicional aninhada.

* **Custom HTML/CSS Visual:** Em vez de visuais nativos, o painel é renderizado através de um visual de HTML Viewer. O DAX constrói dinamicamente o código HTML e CSS (incluindo Grid, Flexbox e componentes de UI) em tempo de execução.

* **SVG Map Customizado:** O mapa do Brasil é renderizado a partir de um código SVG embutido no CSS, com as coordenadas (X, Y) de cada UF recalibradas via função SWITCH no DAX para posicionar as bolhas de densidade com precisão.

* **CSS Tabs Navigation:** Navegação entre as 4 páginas do dashboard construída puramente com HTML/CSS (input radio buttons), dispensando a navegação tradicional do Power BI para criar uma experiência de usuário (UX) semelhante a um aplicativo web.

## Fontes de Dados

&nbsp;&nbsp;&nbsp;&nbsp;**IBGE:** Dados de População e Rendimento Mediano por UF.<br>
&nbsp;&nbsp;&nbsp;&nbsp;**CNES (Cadastro Nacional de Estabelecimentos de Saúde):** Quantitativo de farmácias ativas por UF.<br>
