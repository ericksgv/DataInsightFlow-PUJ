import os
import json
from pymongo import MongoClient

# Cargar las variables de entorno
from dotenv import load_dotenv
load_dotenv()

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = int(os.getenv('MONGO_PORT'))
MONGO_DB = os.getenv('MONGO_DB')
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASS = os.getenv('MONGO_PASS')

# Establecer la conexión con MongoDB
client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/")
db = client[MONGO_DB]

# Obtener la ruta absoluta del archivo JSON
current_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_dir, '../data/processed/publicacionesYComentarios.json')

# Cargar el archivo JSON
with open(json_file_path, encoding='utf-8') as file:
    data = json.load(file)

# Insertar datos en MongoDB
usuarios_collection = db['usuarios']
publicaciones_collection = db['publicaciones']

for publicacion in data['publicaciones']:
    usuario = publicacion['usuario']
    publicacion_id = publicacion['id']
    # Insertar usuario si no existe
    if not usuarios_collection.find_one({'usuario': usuario}):
        usuarios_collection.insert_one({'usuario': usuario})

    # Insertar publicación
    publicacion_data = {
        'id': publicacion_id,
        'descripcion': publicacion['descripcion'],
        'comentarios': publicacion['comentarios'],
        'fecha': publicacion['fecha'],
        'fuente': publicacion['fuente'],
        'usuario': usuario,
        'enlace': publicacion['enlace']
    }
    publicaciones_collection.insert_one(publicacion_data)

print("Datos cargados exitosamente a MongoDB")
