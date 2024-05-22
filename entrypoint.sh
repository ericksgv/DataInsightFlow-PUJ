#!/bin/bash

# Ejecutar extract_data.js y esperar a que termine
echo "Ejecutando extract_data.js..."
node etl/extract_data.js

# Esperar a que extract_data.js termine antes de ejecutar transform_data.js
echo "Ejecutando transform_data.js..."
node etl/transform_data.js

# Esperar a que transform_data.js termine antes de ejecutar load_to_mongo.py
echo "Ejecutando load_to_mongo.py..."
python etl/load_to_mongo.py

# Todos los scripts han terminado, detener el contenedor
echo "Todos los scripts se han ejecutado. Deteniendo el contenedor..."
exit 0
