from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json
import logging
from pathlib import Path


project_root = Path(__file__).parent.parent.parent.absolute()

# Configuración del logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    handlers=[
                        logging.FileHandler(project_root / "etl_load.log"),  # Guarda logs en un archivo en la raíz del proyecto
                        logging.StreamHandler()  # Imprime logs en la consola
                    ])

# Carga las variables de entorno
load_dotenv()


def cargar_datos_en_mongodb(datos, uri, db_nombre, coleccion_nombre):
    client = MongoClient(uri)
    db = client[db_nombre]
    coleccion = db[coleccion_nombre]
    if datos:  # Verifica si hay datos para evitar inserción vacía
        resultado = coleccion.insert_many(datos)
        logging.info(f"Datos cargados en MongoDB. IDs de los documentos insertados: {resultado.inserted_ids}")
    else:
        logging.warning(f"No hay datos para cargar en la colección: {coleccion_nombre}")


def leer_datos_transformados(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)
    return datos


def main():
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NOMBRE = "BancoTweets"


    ruta_datos_procesados = project_root / "data" / "processed"

    # Iterar sobre cada archivo JSON en el directorio de datos procesados
    for archivo_json in ruta_datos_procesados.glob("*.json"):
        # Extraer el nombre del banco del nombre del archivo
        nombre_banco = archivo_json.stem  # 'stem' devuelve el nombre del archivo sin la extensión
        logging.info(f"Procesando archivo: {archivo_json} para el banco: {nombre_banco}")
        datos_transformados = leer_datos_transformados(archivo_json)
        cargar_datos_en_mongodb(datos_transformados, MONGO_URI, DB_NOMBRE, nombre_banco)


if __name__ == "__main__":
    main()
