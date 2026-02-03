import rasterio
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.colors import ListedColormap, BoundaryNorm
from rasterio.enums import Resampling

def gerar_mapa_final_municipios(path_2005, path_2024):
    if not os.path.exists('visualizacao'):
        os.makedirs('visualizacao')

    # Paleta oficial (Simbologia QGIS solicitada)
    cores_qgis = ["#d73a3c", '#ee9167', "#faf399", "#71ce70", "#239724"]
    cmap_custom = ListedColormap(cores_qgis)
    cmap_custom.set_bad(color='white', alpha=0)

    # --- ESCALA DEFINITIVA (Baseada nos seus CSVs municipais) ---
    # O vermelho inicia em -0.31 (mínimo absoluto de 2005)
    # O verde escuro inicia em 0.45 para destacar as matas densas de 2024
    limites = [-0.31, 0.0, 0.18, 0.28, 0.45, 0.62] 
    norm = BoundaryNorm(limites, cmap_custom.N)

    def ler_limpar_dados(path, fator=8):
        with rasterio.open(path) as src:
            out_shape = (int(src.height / fator), int(src.width / fator))
            data = src.read(1, out_shape=out_shape, resampling=Resampling.nearest).astype('float32')
            # Limpeza técnica: remove fundo (0) e valores espúrios
            data = np.where((data == 0) | (data < -1.0) | (data > 1.0), np.nan, data)
            return np.ma.masked_invalid(data)

    data05 = ler_limpar_dados(path_2005)
    data24 = ler_limpar_dados(path_2024)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 11))

    # Mapa 2005: Visão da Seca (Média Municipal 0.18)
    ax1.imshow(data05, cmap=cmap_custom, norm=norm, interpolation='nearest')
    ax1.set_title('NDVI Ceará - 2005', fontsize=14, fontweight='bold')
    ax1.axis('off')

    # Mapa 2024: Visão da Recuperação (Média Municipal 0.25)
    img2 = ax2.imshow(data24, cmap=cmap_custom, norm=norm, interpolation='nearest')
    ax2.set_title('NDVI Ceará - 2024', fontsize=14, fontweight='bold')
    ax2.axis('off')

    plt.suptitle('Monitoramento de NDVI no Ceará: Comparativo de 20 Anos (2005-2024)', 
                 fontsize=22, fontweight='bold', y=0.96)

    # Barra de Legenda Horizontal
    cbar_ax = fig.add_axes([0.35, 0.08, 0.3, 0.02])
    cbar = fig.colorbar(img2, cax=cbar_ax, orientation='horizontal', ticks=limites)
    cbar.set_label('Escala NDVI: Água/Solo (Vermelho) → Vegetação Densa (Verde)', fontsize=12)

    plt.savefig('visualizacao/resultado_final_geoprocessamento.png', bbox_inches='tight', dpi=200)
    print("✅ Resultado gerado com sucesso! Verifique a pasta 'visualizacao'.")
    plt.show()

if __name__ == "__main__":
    gerar_mapa_final_municipios('NDVI_Medio_Anual_Ceara_2005.tif', 'NDVI_Medio_Anual_Ceara_2024.tif')