FROM node:14 AS node-stage

# Crear directorio de trabajo
WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar los scripts Node.js
COPY etl/extract_data.js etl/transform_data.js ./etl/

FROM python:3.9 AS python-stage

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements.txt
COPY requirements.txt ./

# Instalar dependencias
RUN pip install -r requirements.txt

# Copiar el script Python
COPY etl/load_to_mongo.py ./etl/

# Copiar el archivo .env
COPY .env ./

# Crear directorio para los scripts Node.js
RUN mkdir -p /app/etl

# Copiar archivos Node.js desde la etl
COPY --from=node-stage /app/etl /app/etl

# Instalar Node.js y npm en esta imagen
RUN apt-get update && \
    apt-get install -y nodejs npm

# Copiar script de entrada
COPY entrypoint.sh /entrypoint.sh

# Cambiar los permisos del script de entrada para que sea ejecutable
RUN chmod +x /entrypoint.sh

# Comando por defecto para ejecutar el script de entrada
ENTRYPOINT ["/entrypoint.sh"]
