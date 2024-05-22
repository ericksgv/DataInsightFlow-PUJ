import os
from pymongo import MongoClient
from dotenv import load_dotenv
import re
import emoji
import nltk
from nltk.corpus import stopwords
from pysentimiento import create_analyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from gensim import corpora, models
from collections import Counter

# Descargar recursos de NLTK
nltk.download('stopwords')

# Configuración inicial para español
stop_words = set(stopwords.words('spanish'))

def cargar_variables_entorno():
    load_dotenv()
    return {
        "MONGO_HOST": os.getenv('MONGO_HOST'),
        "MONGO_PORT": int(os.getenv('MONGO_PORT')),
        "MONGO_DB": os.getenv('MONGO_DB'),
        "MONGO_USER": os.getenv('MONGO_USER'),
        "MONGO_PASS": os.getenv('MONGO_PASS')
    }

def establecer_conexion_mongo(config):
    client = MongoClient(f"mongodb://{config['MONGO_USER']}:{config['MONGO_PASS']}@{config['MONGO_HOST']}:{config['MONGO_PORT']}/")
    db = client[config['MONGO_DB']]
    return db

def extraer_descripciones_comentarios(db, enlace=None):
    publicaciones_collection = db['publicaciones']
    descripciones = []
    objeto_publicacion = None
    for publicacion in publicaciones_collection.find():
        if enlace and publicacion.get('enlace') != enlace:
            continue
        comentarios = publicacion.get('comentarios', [])
        for comentario in comentarios:
            descripcion = comentario.get('descripcion')
            if descripcion:
                descripciones.append(descripcion)
        if enlace and publicacion.get('enlace') == enlace:
            objeto_publicacion = {
                'descripcion': publicacion.get('descripcion'),
                'fecha': publicacion.get('fecha'),
                'fuente': publicacion.get('fuente'),
                'usuario': publicacion.get('usuario'),
                'enlace': publicacion.get('enlace')
            }
    return descripciones, objeto_publicacion

def extraer_descripciones_comentarios_por_enlace(db, enlace):
    publicaciones_collection = db['publicaciones']
    descripciones = []
    objeto_publicacion = None
    for publicacion in publicaciones_collection.find():     
        if publicacion.get('enlace') == enlace:
            comentarios = publicacion.get('comentarios', [])
            for comentario in comentarios:
                descripcion = comentario.get('descripcion')
                if descripcion:
                    descripciones.append(descripcion)
            objeto_publicacion = {
                'descripcion': publicacion.get('descripcion'),
                'fecha': publicacion.get('fecha'),
                'fuente': publicacion.get('fuente'),
                'usuario': publicacion.get('usuario'),
                'enlace': publicacion.get('enlace')
            }
            return descripciones, objeto_publicacion
    return [], None

def limpiar_comentario(comentario):
    comentario = comentario.lower()  # Convertir a minúsculas
    comentario = re.sub(r'@\w+', '', comentario)  # Eliminar menciones
    comentario = re.sub(r'http\S+', '', comentario)  # Eliminar URLs
    comentario = re.sub(r'#(\w+)', r'\1', comentario)  # Convertir hashtags a texto
    comentario = re.sub(r'\d+', '', comentario)  # Eliminar números
    comentario = emoji.replace_emoji(comentario, replace='')
    palabras = comentario.split()
    palabras_filtradas = [palabra for palabra in palabras if palabra not in stop_words and len(palabra) > 2]
    comentario_limpio = ' '.join(palabras_filtradas)
    return comentario_limpio

def analisis_sentimientos(comentarios):
    analyzer = create_analyzer(task="sentiment", lang="es")
    # Analiza los sentimientos de los comentarios
    resultados_sentimientos = [analyzer.predict(comentario) for comentario in comentarios]
    # Extrae el sentimiento principal (POS, NEG, NEU) de cada resultado
    sentimientos = [resultado.output for resultado in resultados_sentimientos]
    return sentimientos

def generar_grafico_sentimientos(sentimientos):
    conteo_sentimientos = Counter(sentimientos)
    categorias = list(conteo_sentimientos.keys())
    valores = list(conteo_sentimientos.values())

    plt.figure(figsize=(10, 6))
    plt.bar(categorias, valores, color=['blue', 'red', 'green'])
    plt.title('Distribución de Sentimientos')
    plt.xlabel('Sentimiento')
    plt.ylabel('Número de Comentarios')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("sentimientos.png")

def generar_wordclouds(comentarios, num_topics=5):
    diccionario = corpora.Dictionary([tweet.split() for tweet in comentarios])
    corpus = [diccionario.doc2bow(tweet.split()) for tweet in comentarios]
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=diccionario, passes=15)

    for i, topic in enumerate(lda_model.show_topics(num_topics=num_topics, num_words=10)):
        words = dict([word, float(value)] for value, word in map(lambda kv: kv.split("*"), topic[1].split(" + ")))
        wordcloud = WordCloud(background_color='white', width=800, height=400)
        wordcloud.generate_from_frequencies(words)

        plt.figure(figsize=(10, 7))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'Tópico {i + 1}')
        plt.tight_layout()
        plt.savefig(f"wordcloud_topic_{i + 1}.png")

def generar_informe_pdf(objeto_publicacion, cantidad_comentarios):
    c = canvas.Canvas("informe.pdf", pagesize=letter)
    width, height = letter
    margin = 50
    y_position = height - margin

    if objeto_publicacion is not None:
        text = [
            f"Descripción: {objeto_publicacion['descripcion']}",
            f"Fecha: {objeto_publicacion['fecha']}",
            f"Fuente: {objeto_publicacion['fuente']}",
            f"Usuario: {objeto_publicacion['usuario']}",
            f"Enlace: {objeto_publicacion['enlace']}",
            f"Cantidad de comentarios: {cantidad_comentarios}"
        ]
        for line in text:
            c.drawString(margin, y_position, line)
            y_position -= 14
            if y_position < margin:
                c.showPage()
                y_position = height - margin

    y_position -= 20
    c.drawString(margin, y_position, "Gráfico de Sentimientos:")
    y_position -= 14
    c.drawInlineImage("sentimientos.png", margin, y_position - 200, width=400, height=200)
    y_position -= 220

    if y_position < margin:
        c.showPage()
        y_position = height - margin

    c.drawString(margin, y_position, "Wordclouds de Tópicos:")
    y_position -= 14

    for i in range(5):
        if y_position - 220 < margin:
            c.showPage()
            y_position = height - margin

        c.drawString(margin, y_position, f"Tópico {i + 1}:")
        y_position -= 14
        c.drawInlineImage(f"wordcloud_topic_{i + 1}.png", margin, y_position - 200, width=400, height=200)
        y_position -= 220

    c.save()

# Llamada a la función principal para probar la generación del PDF
def main():
    config = cargar_variables_entorno()
    db = establecer_conexion_mongo(config)
    enlace = os.getenv('PUBLICACION_ANALISIS')
    
    # Verificar y agregar '/' al final si no está presente
    if not enlace.endswith('/'):
        enlace += '/'
    print("Enlace", enlace)
    
    objeto_publicacion = None
    comentarios, objeto_publicacion = extraer_descripciones_comentarios_por_enlace(db, enlace)

    # Limpieza de los comentarios
    comentarios = [limpiar_comentario(comentario) for comentario in comentarios]
    sentimientos = analisis_sentimientos(comentarios)

    generar_grafico_sentimientos(sentimientos)
    generar_wordclouds(comentarios)
    generar_informe_pdf(objeto_publicacion, len(comentarios))

if __name__ == "__main__":
    main()