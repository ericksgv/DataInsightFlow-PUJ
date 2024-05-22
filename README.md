# WebScrapingThreads

Este proyecto es realizado únicamente con fines educativos y de aprendizaje. Se utiliza la librería [threads.js](https://github.com/threadsjs/threads.js) para poder realizar web scraping sobre los comentarios de las publicaciones de un usuario de la red social Threads.

> [!NOTE]
> La [librería](https://github.com/threadsjs/threads.js) utiliza paginación para obtener las publicaciones y los comentarios. Por lo tanto, en el código se obtiene la paginación actual para continuar extrayendo a partir de ese punto y así obtener todas las publicaciones y comentarios. Es importante tener en cuenta que el número de publicaciones y comentarios a veces no coincide con los mostrados en la red social, ya que no se consideran publicaciones de solo imágenes ni videos.

> [!CAUTION]
> Es importante tener en cuenta que el scraping de la red social Threads está prohibido por sus términos de servicio. Por lo tanto, el uso de este proyecto para recolectar datos de Threads puede infringir dichos términos y condiciones. Se advierte que el uso de este proyecto para tales fines puede resultar en consecuencias como la suspensión o el cierre de la cuenta de usuario en Threads. Por lo anterior, se recomienda no utilizar una cuenta personal, ya que existe el riesgo de que dicha cuenta sea bloqueada. Para evitar este problema, se sugiere crear una cuenta secundaria exclusivamente para este proyecto.

> [!WARNING]
> Es importante no realizar peticiones de forma continua, se recomienda dejar un lapso de al menos 30 minutos entre cada solicitud para evitar ser baneado por la red social Threads. Además, es importante no compartir la cuenta para evitar solicitudes desde diferentes direcciones IP, lo cual podría resultar en un bloqueo de la cuenta.

## Instalación Y configuración ⚙️🛠️

### Verificar la instalación de Node.js
Antes de comenzar, asegúrate de tener Node.js instalado en tu sistema. Puedes verificar si Node.js está instalado ejecutando el siguiente comando en tu terminal:
```
node -v
```
Si Node.js está instalado, este comando mostrará la versión actual de Node.js. Si no está instalado, puedes descargar e instalar Node.js desde el [sitio oficial de Node.js](https://nodejs.org/en/download).

### Clonar el repositorio
Para clonar este repositorio
```
git clone https://github.com/ericksgv/WebScrapingThreads
```
### Instalar las dependencias
```
npm install @threadsjs/threads.js
```
```
npm install dotenv
```
### Configuración del Archivo .env

1. En la raíz de tu proyecto, crea un nuevo archivo llamado `.env`.

2. Abre el archivo `.env` en tu editor de texto preferido.

3. **Variables de Entorno**
El proyecto utiliza variables de entorno para la configuración de la conexión a la base de datos MongoDB y otros parámetros relacionados con la aplicación. Antes de ejecutar la aplicación, asegúrate de configurar estas variables de entorno adecuadamente.

Variables requeridas:

MONGO_HOST: La dirección IP o el nombre de host del servidor de MongoDB.
MONGO_PORT: El puerto en el que MongoDB está escuchando las conexiones.
MONGO_DB: El nombre de la base de datos MongoDB a la que se conectará la aplicación.
MONGO_USER: El nombre de usuario para autenticarse en MongoDB.
MONGO_PASS: La contraseña asociada al nombre de usuario para autenticarse en MongoDB.
Otras variables opcionales:
USUARIO: Tu nombre de usuario para la plataforma Threads.
CONTRASENA: Tu contraseña para la plataforma Threads.
PERFILTHREADS: El perfil de Threads del que se extraerán los posts.
PUBLICACIONES_BUSCADAS: Lista separada por comas del enlace de la publicación
PUBLICACION_ANALISIS: Enlace de la publicación a analizar

Configuración del archivo .env:
Crea un archivo .env en la raíz del proyecto y define las variables de entorno necesarias según el ejemplo proporcionado en el archivo example.env. Asegúrate de reemplazar los valores de ejemplo con tus propias credenciales y configuraciones.

 3. **Definir las variables de entorno**:
  - Para configurar tu nombre de usuario, agrega la siguiente línea al archivo `.env` y reemplaza `tu_nombre_de_usuario` con tu nombre de usuario de Threads:
    ```plaintext
    USUARIO="tu_nombre_de_usuario"
    ```
  - Para configurar tu contraseña, agrega la siguiente línea al archivo `.env` y reemplaza `tu_contraseña` con tu contraseña de Threads:
    ```plaintext
    CONTRASENA="tu_contraseña"
    ```
   - Para configurar el perfil de Threads del que se extraerán los posts, agrega la siguiente línea al archivo `.env` y reemplaza `tu_perfil_de_threads` con el perfil de Threads que deseas utilizar:
     ```plaintext
     PERFILTHREADS="tu_perfil_de_threads"
     ```
 4. Guarda los cambios realizados en el archivo `.env`.
 
## Uso 📦

1. Verificar si docker se encuentra instalado.

     ```
     docker -v
     ```

2. Compilar la imagen de docker, para generar los contenedores de la base de datos y de la etl.

     ```
     docker-compose build
     ```

3. Ejecutar la imagen de docker, para iniciar los contenedores de la base de datos y de la etl.

     ```
     docker-compose up -d
     ```

4. Para ejecutar la ETL, si tiene Linux o el subsistema de Linux para Windows, ejecute:

     ```
     make run-etl
     ```

5. En caso contrario, ejecute el siguiente comando:
   
     ```
     docker-compose up -d etl
     ```

6. Para el análisis de sentimientos primero asegúrece de que tiene instalas las dependencias correctamente.

     ```
     cd pln
     ```

     ```
     pip install -r requirements.txt
     ```

7. En las variables de entorno establezca la publicación a la que le desea analizar los comentarios:
      
      ```
      PUBLICACION_ANALISIS=
      ```

8. Para ejecutar el análisis
      
      ```
      python sentiment_analysis.py
      ```

## Autores ✒️
* **Santiago Mejía** - [SantiagoMejiaF](https://github.com/SantiagoMejiaF)
* **Ana Ortegón** - [Arsete](https://github.com/Arsete)
* **Felipe García** - [felipe0525](https://github.com/felipe0525)
* **Santiago Gallo** - [KironStylo](https://github.com/KironStylo)
* **Erick Garavito** - [ericksgv](https://github.com/ericksgv)

## Tecnologías
<img align="left" alt="Nodejs" width="76px" src="https://user-images.githubusercontent.com/25181517/183568594-85e280a7-0d7e-4d1a-9028-c8c2209e073c.png" /> 
<img align="left" alt="JavaScript" width="76px" src="https://raw.githubusercontent.com/jmnote/z-icons/master/svg/javascript.svg" /> 

<br>
<br>
<br>


## Licencia 📄
Este proyecto está bajo la licencia [MIT](./LICENSE).


