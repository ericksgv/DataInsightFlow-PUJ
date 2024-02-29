#!/bin/bash

# Navega al directorio del proyecto
cd /home/camposjulca/Repos_cristhiamdaniel/DataInsightFlow-PUJ

# Activa tu entorno virtual
source .venv11/bin/activate

# Define un archivo de log
LOGFILE="/home/camposjulca/Repos_cristhiamdaniel/DataInsightFlow-PUJ/logs/etl_$(date +'%Y-%m-%d_%H-%M-%S').log"

# Ejecuta los scripts en orden y registra la salida
python src/etl/extract_tweets.py >> $LOGFILE 2>&1
python src/etl/transform_tweets.py >> $LOGFILE 2>&1
python src/etl/load_to_mongodb.py >> $LOGFILE 2>&1

# Desactiva el entorno virtual
deactivate

echo "ETL process completed on $(date)" >> $LOGFILE
