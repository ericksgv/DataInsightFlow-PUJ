from pathlib import Path
import json
import re
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

project_root = Path(__file__).parent.parent.parent.absolute()

# Configuración del logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    handlers=[
                        logging.FileHandler(project_root / "etl_process.log"),  # Guarda logs en un archivo en la raíz del proyecto
                        logging.StreamHandler()  # Imprime logs en la consola
                    ])


def extraer_hashtags(tweet_text):
    return re.findall(r"#(\w+)", tweet_text)


def extraer_menciones(tweet_text):
    return re.findall(r"@(\w+)", tweet_text)


def transformar_datos(ruta_archivo):
    tweets_transformados = []
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            if linea.strip() and linea.count('\t') == 2:
                id_tweet, usuario, tweet_text = linea.strip().split('\t', 2)
                fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                hashtags = extraer_hashtags(tweet_text)
                menciones = extraer_menciones(tweet_text)
                tweet_dict = {
                    "id": id_tweet,
                    "tweet_text": tweet_text,
                    "usuario": usuario,
                    "fecha": fecha,
                    "hashtags": hashtags,
                    "menciones": menciones
                }
                tweets_transformados.append(tweet_dict)
            else:
                logging.warning(f"Se encontró una línea en un formato inesperado: {linea.strip()}")
        logging.info(f"Total de tweets transformados: {len(tweets_transformados)}")
    return tweets_transformados


def guardar_datos_transformados(tweets_transformados, ruta_destino):
    with open(ruta_destino, 'w', encoding='utf-8') as archivo:
        json.dump(tweets_transformados, archivo, ensure_ascii=False, indent=4)
    logging.info(f"Datos transformados guardados en {ruta_destino}")


def main():
    load_dotenv()
    ruta_raw = project_root / "data" / "raw"

    # Iterar sobre todos los archivos en data/raw
    for ruta_archivo in ruta_raw.glob('*.txt'):
        logging.info(f"Procesando archivo: {ruta_archivo.name}")
        tweets_transformados = transformar_datos(ruta_archivo)

        # Define un nombre de archivo de salida basado en el archivo de entrada
        nombre_archivo_salida = f"{ruta_archivo.stem}_transformados.json"
        ruta_transformados = project_root / "data" / "processed" / nombre_archivo_salida

        guardar_datos_transformados(tweets_transformados, ruta_transformados)


if __name__ == "__main__":
    main()
