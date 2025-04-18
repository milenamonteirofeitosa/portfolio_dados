# 🌱 NDVI Analysis for Ceará (2024) - Python + Google Earth Engine

![NDVI Example](https://gisgeography.com/wp-content/uploads/2015/11/NDVI-Formula-NDVI-Index.png)  
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
