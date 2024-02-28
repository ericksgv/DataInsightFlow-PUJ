import asyncio
import os
from pathlib import Path
from twscrape import API, gather
from dotenv import load_dotenv
import logging

# Configura el logging para escribir en un archivo, además de configurar el nivel y formato de los mensajes
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    handlers=[
                        logging.FileHandler("twitter_fetch.log"),  # Guarda logs en un archivo
                        logging.StreamHandler()  # Imprime logs en la consola
                    ])


async def search_tweets(api, query, filename, limit=100):
    logging.info(f"Iniciando búsqueda de tweets para '{query}' con límite de {limit}")
    try:
        tweets = await gather(api.search(query, limit=limit))
        filename.parent.mkdir(parents=True, exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as f:
            for tweet in tweets:
                f.write(f"{tweet.id}\t{tweet.user.username}\t{tweet.rawContent}\n")
        logging.info(f"Guardados {len(tweets)} tweets en {filename}.")
    except Exception as e:
        logging.error(f"Error al buscar tweets para '{query}': {e}")


async def main():
    load_dotenv()
    logging.info("Cargando variables de entorno y autenticando con la API...")

    username = os.getenv('TWITTER_USERNAME')
    password = os.getenv('TWITTER_PASSWORD')
    email = os.getenv('TWITTER_EMAIL')
    email_password = os.getenv('TWITTER_EMAIL_PASSWORD')

    api = API()
    await api.pool.add_account(username, password, email, email_password)
    await api.pool.login_all()
    logging.info("Autenticación exitosa con la API.")

    project_root = Path(__file__).parent.parent.parent.absolute()
    raw_data_directory = project_root / "data" / "raw"

    queries = [
        ("Bancolombia", raw_data_directory / "tweets_Bancolombia.txt"),
        ("Davivienda", raw_data_directory / "tweets_Davivienda.txt"),
        ("BBVA Colombia", raw_data_directory / "tweets_BBVA.txt"),
        ("Banco de Bogotá", raw_data_directory / "tweets_BancoBogota.txt"),
        ("Banco de Occidente", raw_data_directory / "tweets_BancoOccidente.txt"),
        ("Banco Popular", raw_data_directory / "tweets_BancoPopular.txt"),
        ("Banco Caja Social", raw_data_directory / "tweets_BancoCajaSocial.txt"),
        ("Banco AV Villas", raw_data_directory / "tweets_BancoAVVillas.txt"),
    ]

    for query, filename in queries:
        await search_tweets(api, query, filename)


if __name__ == "__main__":
    asyncio.run(main())
