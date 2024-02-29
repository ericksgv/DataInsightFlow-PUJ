# DataInsightFlow-PUJ

## Descripción

Este proyecto implementa un pipeline ETL (Extract, Transform, Load) para recolectar, procesar y almacenar tweets relacionados con bancos colombianos. El objetivo es analizar la percepción pública y el sentimiento hacia estas instituciones financieras a través de las menciones en Twitter.

## Estructura del Proyecto

```
DataInsightFlow-PUJ/
│
├── data/
│   ├── raw/                  # Tweets sin procesar
│   └── processed/            # Tweets procesados y listos para análisis
│
├── environment.yml          # Archivo para recrear el entorno de desarrollo
│
├── logs/                    # Logs de las ejecuciones
│
├── notebooks/               # Jupyter notebooks para análisis y experimentación
│
├── README.md                # Este archivo
│
├── run_etl.sh               # Script para ejecutar el pipeline ETL
│
├── src/
│   ├── analysis/            # Scripts para análisis de datos
│   ├── etl/                 # Scripts para las etapas ETL
│   │   ├── __init__.py
│   │   ├── load_to_mongodb.py
│   │   ├── transform_tweets.py
│   │   └── twitter_fetch.py
│   └── nlp/                 # Scripts para procesamiento de lenguaje natural
│
└── tests/                   # Tests unitarios y de integración
```

## Configuración del Entorno

Para configurar el entorno de desarrollo, se recomienda usar [Conda](https://docs.conda.io/en/latest/):

```bash
conda env create -f environment.yml
conda activate newenv
```

## Ejecución del Pipeline ETL

El script `run_etl.sh` se encarga de ejecutar las tareas de extracción, transformación y carga de datos. Para ejecutar este script manualmente:

```bash
./run_etl.sh
```

Este script también se configura para ejecutarse automáticamente cada cierto tiempo mediante una tarea cron.

## Estructura de los Scripts ETL

### Extract

`twitter_fetch.py`: Se conecta a la API de Twitter para recolectar tweets según criterios predefinidos.

### Transform

`transform_tweets.py`: Procesa los tweets brutos para limpiarlos y estructurarlos.

### Load

`load_to_mongodb.py`: Carga los tweets procesados en una base de datos MongoDB.

## Contribuciones

Las contribuciones al proyecto son bienvenidas. Por favor, consulta los issues abiertos o crea uno nuevo para discutir cambios o mejoras.

