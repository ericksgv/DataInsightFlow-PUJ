#!/bin/bash

# Navega al directorio del proyecto
cd /home/camposjulca/Repos_cristhiamdaniel/DataInsightFlow-PUJ

# Activa tu entorno virtual
source .venv11/bin/activate

# Ejecuta los scripts en orden
python src/etl/extract_tweets.py
python src/etl/transform_tweets.py
python src/etl/load_to_mongodb.py

# Desactiva el entorno virtual
deactivate
