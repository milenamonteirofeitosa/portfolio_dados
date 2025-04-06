# 📊 Consulta ao PIB per capita dos Municípios do Ceará via API SIDRA/IBGE

Este script em Python consulta a API do SIDRA (Sistema IBGE de Recuperação Automática) para obter os dados de **PIB per capita** dos municípios do estado do **Ceará (UF 23)** e permite salvar os resultados em arquivos CSV ou Excel.

## 🔧 Requisitos

Antes de executar o script, certifique-se de que as seguintes bibliotecas estão instaladas:

```bash
pip install pandas requests openpyxl
```

## 🚀 Como funciona
**Consulta a API do SIDRA** com a tabela 5938 (PIB per capita dos municípios).

**Filtra os dados** apenas para o estado do Ceará (código 23).

**Processa os dados** e exibe os municípios com maior PIB per capita.

**Pergunta ao usuário** se deseja salvar os dados como CSV, Excel ou nenhum.

## 📁 Estrutura do Código
`consultar_api_sidra()`

Realiza a requisição HTTP à API do SIDRA para o período informado.

`processar_dados()`

Transforma a resposta JSON em um DataFrame do Pandas, filtra os dados do Ceará e realiza o tratamento necessário.

`salvar_dados()`

Salva os dados no formato desejado, de acordo com a escolha do usuário.

`main()`

Função principal que orquestra o fluxo: consulta → processamento → exibição → salvamento.

## 🧪 Exemplo de uso
Ao executar o script:

```bash
python PIB_analise.py
```

O script exibirá os municípios com maior PIB per capita no Ceará e perguntará:

```bash
"Deseja salvar os dados? (csv/excel/nenhum):"

```

Digite sua opção e o arquivo será salvo no diretório atual.

## 📎 Fonte dos Dados

**SIDRA/IBGE - Tabela 5938**

[Link da API](https://apisidra.ibge.gov.br/)

## 🏆 Ranking dos Municípios do Ceará com Maior PIB

A tabela abaixo mostra os municípios com os maiores PIBs no Ceará em 2021, com base nos dados obtidos da API do SIDRA/IBGE.

| Município | PIB |
| ------------- | ------------- |
| Fortaleza - CE | 73436128 |
| Maracanaú - CE | 12337017 |
| Caucaia - CE | 10414373| 
| São Gonçalo do Amarante - CE | 8633637 |
| Sobral - CE | 5395130 |

## 🧑‍💻 Autor(a)
Este script foi desenvolvido com o objetivo de facilitar o acesso a dados públicos do IBGE sobre o desenvolvimento econômico dos municípios cearenses.


