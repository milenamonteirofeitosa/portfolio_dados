# 🌱 NDVI Analysis for Ceará (2024) - Python + Google Earth Engine

*Normalized Difference Vegetation Index (NDVI)*

## 📌 Sobre o Projeto
Este script calcula o **Índice de Vegetação por Diferença Normalizada (NDVI)** para o estado do Ceará em 2024 usando:
- 🛰️ Dados do **Landsat 8** (Coleção Surface Reflectance Tier 1)
- 🔥 Processamento em nuvem com **Google Earth Engine**
- 🐍 Bibliotecas Python para análise geoespacial

## 🛠️ Tecnologias
```python
import ee          # Google Earth Engine
import geemap      # Visualização de dados geoespaciais
import geopandas   # Processamento de shapefiles
```

 ## 🌟 Principais Funções

| Função          | Ícone | Descrição                          |
|-----------------|-------|-----------------------------------|
| `maskL8sr()`    | ☁️➡️☀️ | Remove nuvens e pixels saturados das imagens Landsat 8 |
| `NDVI()`        | 🌿➡️📊 | Calcula o índice de vegetação usando bandas NIR (B5) e Red (B4) |
| `simplify()`    | ✂️📐  | Otimiza a geometria do shapefile para processamento mais rápido |

## 📊 Saída Esperada
- **Arquivo**: `NDVI_Medio_Anual_Ceara_2024.tif` no Google Drive
  - 📁 Pasta: `EarthEngineExports`
  - 🔢 Valores NDVI: 
    - `-1.0` a `0.0` → Água/solo exposto
    - `0.0` a `0.3` → Vegetação esparsa
    - `0.3` a `1.0` → Vegetação densa
  - 🖼️ Resolução: 30m/pixel
  - 🌍 SRID: EPSG:4326 (WGS84)

## ⚠️ Limitações
| Limitação | Solução Possível |
|-----------|------------------|
| 📉 Cotas do Earth Engine | Monitorar uso em [EE Dashboard](https://code.earthengine.google.com/) |
| 🗺️ Shapefile em WGS84 | Converter com `gdalwarp` ou QGIS |
| ⏳ Processamento lento | Dividir área em tiles menores |

## 📚 Recursos Úteis
- [Google Earth Engine Docs](https://developers.google.com/earth-engine) 📘
- [NDVI Explained (GIS Geography)](https://gisgeography.com/ndvi-normalized-difference-vegetation-index/) 🌎
- [Geemap Tutorials](https://geemap.org/) 🐍

---

Feito com ❤️ por [Milena Monteiro Feitosa](https://github.com/milenamonteirofeitosa)  
[![GitHub](https://img.shields.io/badge/Ver_no-GitHub-181717?style=flat&logo=github)](https://github.com/milenamonteirofeitosa/portfolio_dados)
 


   



