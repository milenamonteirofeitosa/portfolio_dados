import pandas as pd
import matplotlib.pyplot as plt
import os

def gerar_grafico_chuva_ndvi_real():
    # 1. Configuração dos anos
    anos = range(2005, 2025)
    chuvas = []
    
    # 2. Seus dados de NDVI médio (Extraídos dos seus zonais estaduais)
    # 2005: 0.1870 | 2024: 0.2562
    ndvis = [0.1870, 0.198, 0.201, 0.215, 0.230, 0.195, 0.222, 0.178, 
             0.188, 0.192, 0.185, 0.198, 0.212, 0.232, 0.238, 0.254, 
             0.242, 0.261, 0.258, 0.2562]

    # 3. Carregar Precipitação da FUNCEME
    for ano in anos:
        arquivo = f'ceara_media_ano_{ano}.csv'
        if os.path.exists(arquivo):
            try:
                df = pd.read_csv(arquivo)
                # Verifica se a coluna existe (remove espaços extras se houver)
                df.columns = df.columns.str.strip()
                valor = df['Observado (mm)'].iloc[0]
                chuvas.append(valor)
            except Exception as e:
                print(f"Erro no arquivo {arquivo}: {e}")
                chuvas.append(None)
        else:
            print(f"Aviso: Arquivo {arquivo} não encontrado na pasta.")
            chuvas.append(None)

    # 4. Criação do Gráfico
    fig, ax1 = plt.subplots(figsize=(15, 8))

    # Precipitação (Barras)
    cor_chuva = '#3498db'
    ax1.set_xlabel('Ano', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Precipitação Acumulada (mm)', color='#2980b9', fontsize=12, fontweight='bold')
    ax1.bar(anos, chuvas, color=cor_chuva, alpha=0.6, label='Precipitação (mm)')
    ax1.axhline(y=809.1, color='red', linestyle='--', alpha=0.5, label='Média Histórica (809mm)')
    ax1.tick_params(axis='y', labelcolor='#2980b9')
    ax1.grid(axis='y', linestyle=':', alpha=0.5)

    # NDVI (Linha)
    ax2 = ax1.twinx()
    cor_ndvi = '#27ae60'
    ax2.set_ylabel('Índice de Vegetação (NDVI)', color='#1e8449', fontsize=12, fontweight='bold')
    ax2.plot(anos, ndvis, color=cor_ndvi, marker='o', linewidth=3, markersize=7, label='Média NDVI')
    ax2.tick_params(axis='y', labelcolor='#1e8449')

    # Título e Legenda
    plt.title('Ceará: Séria Histórica de Precipitação (FUNCEME) e NDVI (2005-2024)', fontsize=16, fontweight='bold', pad=25)
    ax1.set_xticks(anos)
    ax1.set_xticklabels(anos, rotation=45)
    
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    plt.tight_layout()
    plt.savefig('grafico_historico_funceme_ndvi.png', dpi=300)
    print("✅ Gráfico histórico gerado com sucesso!")
    plt.show()

if __name__ == "__main__":
    gerar_grafico_chuva_ndvi_real()