import requests
import pandas as pd
import os

# Função para consultar a API do SIDRA
def consultar_api_sidra(base_url, periodos):
    url = base_url.format(periodos)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao acessar a API para {periodos}: {response.status_code}, {response.text}")
        return None

# Função para processar os dados da API
def processar_dados(dados):
    # Converte os dados JSON em um DataFrame
    df = pd.DataFrame(dados[1:], columns=dados[0])
    
    # Filtra apenas os dados do Ceará (código do estado = 23)
    df_ce = df[df['D1C'].str.startswith('23')]
    
    # Seleciona e renomeia as colunas relevantes
    df_ce = df_ce[['D1N', 'V']]
    df_ce.columns = ['Municipio', 'PIB'] 
    
    # Converte a coluna de PIB para numérico
    df_ce['PIB'] = pd.to_numeric(df_ce['PIB'], errors='coerce')
    
    return df_ce

# Função para salvar os dados
def salvar_dados(df, local_directory):
    save_choice = input("Deseja salvar os dados? (csv/excel/nenhum): ").strip().lower()
    if save_choice == 'csv':
        file_path = os.path.join(local_directory, 'pib_municipios_ceara.csv')
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"Arquivo CSV salvo com sucesso em {file_path}!")
    elif save_choice == 'excel':
        file_path = os.path.join(local_directory, 'pib_municipios_ceara.xlsx')
        df.to_excel(file_path, index=False, engine='openpyxl')
        print(f"Arquivo Excel salvo com sucesso em {file_path}!")
    else:
        print("Nenhum arquivo foi salvo.")

# Função principal
def main():
    # Parâmetros base da API SIDRA do IBGE
    base_url = "https://apisidra.ibge.gov.br/values/t/5938/n6/in%20n3%2023/v/37/p/{}?formato=json"
    all_data = []

    # Diretório local onde os arquivos serão salvos
    local_directory = os.path.abspath('.')

    try:
        # Consulta a API para o último ano disponível
        periodos = "last"
        dados = consultar_api_sidra(base_url, periodos)

        # Processa os dados
        if dados:
            df_ce = processar_dados(dados)
            
            # Ordena os municípios por PIB
            df_ce = df_ce.sort_values(by="PIB", ascending=False)
            
            # Exibe os dados
            print(df_ce.head())
            
            # Salva os dados
            salvar_dados(df_ce, local_directory)
        else:
            print("Não foi possível obter os dados da API.")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

# Chamando a função principal
if __name__ == "__main__":
    main()