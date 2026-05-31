# Análisis Comparativo de Mortalidad: Mundo vs. Colombia (Pipeline ETL)

Este proyecto implementa una arquitectura de datos (ETL) robusta en Python para analizar las causas de mortalidad a nivel mundial (2010-2017) y contrastarlas con la realidad nacional de Colombia. El sistema unifica, limpia y enriquece múltiples fuentes de datos para generar visualizaciones analíticas que apoyan la toma de decisiones en salud pública.

## 📋 Tabla de Contenidos
1. [Metodología y Fuentes de Datos](#metodología-y-fuentes-de-datos)
2. [Arquitectura del Proyecto](#arquitectura-del-proyecto)
3. [Requisitos y Configuración (Setup)](#requisitos-y-configuración-setup)
4. [Proceso de Ejecución (Pipeline ETL)](#proceso-de-ejecución-pipeline-etl)
5. [Resultados y Conclusiones](#resultados-y-conclusiones)

## 📊 Metodología y Fuentes de Datos
Para superar la limitación del dataset base (que solo poseía granularidad global), se implementó una estrategia de enriquecimiento de datos de tres vías:
1. **Raw Global:** Dataset original con métricas de mortalidad mundial y su variación anual (`causeofdeath.csv`).
2. **Enriquecimiento Taxonómico (OMS):** Generación algorítmica de un catálogo basado en la Clasificación Internacional de Enfermedades, separando los datos en: Transmisibles, No Transmisibles y Lesiones.
3. **Microdatos DANE (Colombia):** Desempaquetado y homologación del Cuadro 5 de Defunciones No Fetales (2017) para contrastar el comportamiento mundial con la realidad nacional.

## 📂 Arquitectura del Proyecto
El proyecto sigue el estándar de *Data Engineering*, aislando la ingesta, transformación y visualización:

```text
etl-act2-laboratory/
│
├── data/
│   ├── raw/               # Dataset original inmutable y Excel del DANE
│   │   └── dane/          # CSVs aplanados generados automáticamente
│   ├── external/          # Diccionarios maestros (OMS y homologación DANE)
│   └── processed/         # Modelo de datos final listo para analítica
│
├── logs/                  # Trazabilidad de ejecución del pipeline ETL
│
├── notebooks/             
│   └── 01_analisis_causas_muerte_unificado.ipynb  # Entorno analítico visual
│
├── src/
│   └── data/              
│       ├── E_unpack_dane.py        # (Extracción) Aplana Excel multipestaña a CSV
│       ├── E_make_dataset.py       # (Extracción) Genera catálogos de variables
│       └── T_process_dataset.py    # (Transformación) Pivot, limpieza y unificación (Joins)
│
├── requirements.txt       # Dependencias
└── README.md              # Documentación
```

## ⚙️ Requisitos y Configuración (Setup)

Para garantizar la reproducibilidad del proyecto, se ha configurado un entorno virtual. Asegúrese de tener instalado **Python 3.10 o superior** antes de comenzar.

**1. Clonar el repositorio:**

Abra su terminal de preferencia y descargue el código fuente:

```bash
git clone [https://github.com/mateotorres2409/etl-act2-laboratory.git](https://github.com/mateotorres2409/etl-act2-laboratory.git)
cd etl-act2-laboratory
python3 -m venv venv
source venv/bin/activate
```

*   **En Windows (Command Prompt / PowerShell):**

```cmd
python -m venv venv
venv\Scripts\activate
```

**3. Instalación de Dependencias:**

Con el entorno virtual activo, instale las librerías requeridas (incluyendo motores para manipulación de Excel y visualización de datos):

```bash
pip install -r requirements.txt
```

## 🚀 Proceso de Ejecución (Pipeline ETL)

El sistema está diseñado bajo una arquitectura modular. Para que los datos fluyan correctamente desde la capa cruda (*Raw*) hasta la capa analítica (*Processed*), **los scripts deben ejecutarse en este orden estricto**:

### Fase I: Extracción e Ingesta (Extract - Unpacking)

Desempaqueta el archivo original en formato Excel del DANE (separando sus múltiples pestañas) y lo convierte en archivos planos CSV ligeros dentro de la carpeta `data/raw/dane/`.

```bash
python src/data/E_unpack_dane.py

```

### Fase II: Generación de Datos Maestros (Master Data Management)

Genera físicamente los diccionarios de homologación para cruzar las bases. Crea la taxonomía de la OMS y el mapeo de equivalencias del DANE depositándolos en la capa `data/external/`.

```bash
python src/data/E_make_dataset.py

```

### Fase III: Transformación y Carga (Transform & Load)

Es el motor principal del pipeline. Lee los datos crudos, estandariza columnas, ejecuta el pivotaje de métricas anuales (de formato largo a ancho) y realiza el cruce (*Left Join* múltiple) entre las bases globales, los diccionarios y los microdatos de Colombia. El modelo final unificado se guarda en la capa `data/processed/` como `analytical_dataset.csv`.

```bash
python src/data/T_process_dataset.py

```

### Fase IV: Análisis y Visualización (Data Analytics)

Una vez finalizado el procesamiento automatizado del backend, levante el entorno de *Jupyter Lab* para consumir los datos procesados, visualizar el análisis exploratorio y obtener las métricas de transición epidemiológica.

```bash
jupyter lab notebooks/01_analisis_causas_muerte_unificado.ipynb

```

> **💡 Nota de Evaluación:** Dentro del entorno de Jupyter, seleccione `Run -> Run All Cells` para renderizar las gráficas interactivas. Para generar el reporte final de entrega en formato PDF con la más alta calidad, utilice la función `Export to HTML` y proceda a guardar mediante la opción de "Imprimir como PDF" de su navegador web (asegurándose de activar la opción de "Gráficos de fondo").
