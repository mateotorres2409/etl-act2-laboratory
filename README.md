# Análisis Global de Causas de Mortalidad (ETL & Visualización)

Este proyecto implementa un pipeline de datos (ETL) robusto en Python para analizar las causas de mortalidad a nivel mundial, su impacto porcentual y su evolución histórica (2010-2017). Aplicando principios de *Data Engineering* y arquitectura limpia, el sistema unifica, transforma y enriquece los datos base con una taxonomía médica externa para generar visualizaciones analíticas avanzadas.

## 📋 Tabla de Contenidos
1. [Descripción del Proyecto y Metodología](#descripción-del-proyecto-y-metodología)
2. [Arquitectura del Directorio](#arquitectura-del-directorio)
3. [Fuentes de Datos](#fuentes-de-datos)
4. [Requisitos Previos](#requisitos-previos)
5. [Instalación y Configuración](#instalación-y-configuración)
6. [Ejecución del Pipeline (Paso a Paso)](#ejecución-del-pipeline)
7. [Observabilidad y Trazabilidad](#observabilidad-y-trazabilidad)
8. [Entregables Visuales](#entregables-visuales)

## 🎯 Descripción del Proyecto y Metodología
Ante la naturaleza inmutable del dataset original (el cual cuenta únicamente con una desagregación a nivel "Global"), se diseñó una arquitectura de datos orientada a la causa de muerte. 

Para cumplir con el enriquecimiento de datos multivariado, el pipeline genera dinámicamente un catálogo basado en la **Taxonomía de la Organización Mundial de la Salud (OMS)**, clasificando las enfermedades en:
- Transmisibles (Infecciosas/Maternas)
- No Transmisibles (Crónicas)
- Lesiones (Accidentes/Violencia)

A partir del cruce de estas fuentes, se construyen matrices de riesgo y análisis de carga global de morbilidad.

## 📂 Arquitectura del Directorio
El proyecto sigue el estándar *Cookiecutter Data Science*, garantizando la separación de responsabilidades (SRP) entre extracción, transformación y visualización:

```text
etl-act2-laboratory/
│
├── data/
│   ├── raw/               # Dataset original inmutable (causeofdeath.csv)
│   ├── external/          # Catálogo OMS autogenerado (who_disease_taxonomy.csv)
│   └── processed/         # Dataset final unificado (analytical_dataset.csv)
│
├── logs/                  # Archivos de observabilidad (ingestion.log, processing.log)
│
├── reports/
│   └── figures/           # Gráficas exportadas en alta resolución (.png)
│
├── src/
│   ├── data/              
│   │   ├── E_make_dataset.py       # (Extracción) Genera la fuente externa
│   │   └── T_process_dataset.py    # (Transformación) Pivota y cruza los datos
│   └── visualization/     
│       └── visualize.py            # Generación de gráficos y reportes
│
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Documentación principal