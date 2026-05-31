# Análisis Global de Causas de Mortalidad (ETL & Visualización)

Este proyecto implementa un pipeline de datos (ETL) robusto en Python para analizar las causas de mortalidad a nivel mundial (2017) y su evolución histórica. El desarrollo integra datos sociodemográficos externos para establecer correlaciones multivariadas, aplicando principios de arquitectura limpia, observabilidad y reproducibilidad.

## 📋 Tabla de Contenidos
1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Arquitectura del Directorio](#arquitectura-del-directorio)
3. [Fuentes de Datos](#fuentes-de-datos)
4. [Requisitos Previos](#requisitos-previos)
5. [Instalación y Configuración](#instalación-y-configuración)
6. [Ejecución del Pipeline](#ejecución-del-pipeline)
7. [Observabilidad y Logs](#observabilidad-y-logs)
8. [Autor](#autor)

## 🎯 Descripción del Proyecto
El objetivo principal es unificar, limpiar y estructurar el dataset base de causas de muerte, enriqueciéndolo con indicadores del Banco Mundial (Gasto en Salud como % del PIB). A partir de estos datos transformados, se generan visualizaciones estratégicas que responden a:
- Principales causas de muerte a nivel global.
- Tendencias de crecimiento o decrecimiento (2010-2017).
- Correlación entre la inversión en salud pública y las tasas de mortalidad por enfermedades específicas.

## 📂 Arquitectura del Directorio
El proyecto sigue el estándar *Cookiecutter Data Science* para garantizar la separación lógica entre datos crudos, código fuente y análisis exploratorio:

```text
etl-act2-laboratory/
│
├── data/
│   ├── raw/               # Dataset original inmutable (causeofdeath.csv)
│   ├── external/          # Datos extraídos vía API (Banco Mundial)
│   └── processed/         # Datos limpios y unificados listos para análisis
│
├── logs/                  # Archivos de trazabilidad de los scripts (.log)
│
├── notebooks/             # Jupyter Notebooks para Análisis Exploratorio (EDA)
│
├── src/
│   ├── __init__.py
│   ├── data/              # Scripts de ingesta y limpieza (make_dataset.py)
│   └── visualization/     # Scripts para generación de gráficos
│
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Documentación principal