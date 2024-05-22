const { Client } = require('@threadsjs/threads.js');
const fs = require('fs');
const path = require('path');
const { setTimeout } = require('timers');
require('dotenv').config();

async function iniciarSesion() {
    await cliente.login(usuario, contrasena);
}

// Función para generar un valor aleatorio entre min (incluido) y max (excluido)
function obtenerTiempoAleatorio(min, max) {
    return Math.floor(Math.random() * (max - min) + min) * 1000; // Convertir a milisegundos
}

//Función para obtener desde Threads las publicaciones de un usuario
async function obtenerPublicacionesThreads() {
    let publicaciones = [];
    let ids = [];
    // Definir el directorio y el nombre del archivo
    const filePath = path.join(directorio, 'IdPostBuscado.txt');
    const filePathPosts = path.join(directorio, 'publicaciones.json');
    // Asegurarse de que el directorio existe antes de escribir el archivo
    if (!fs.existsSync(directorio)) {
        fs.mkdirSync(directorio, { recursive: true });
    }
    try {
        for (const idPublicacion of publicacionesBuscadas) {
            console.log(idPublicacion)
            const post = await cliente.posts.embed(idPublicacion);
                    // Convertir el objeto JSON a una cadena
                    console.log(post)
            publicaciones.push(post);
            ids.push(post.media.id.split('_')[0]);
        }
        // Estructurar los datos en un objeto con una propiedad "publicaciones"
        const datosAguardar = { "publicaciones": publicaciones };
        // Guardar el objeto estructurado en el archivo JSON
        const idsGuardar = ids.join('\n');
        fs.writeFileSync(filePath, idsGuardar, { flag: 'w' });
        fs.writeFileSync(filePathPosts, JSON.stringify(datosAguardar, null, 2), { flag: 'w' });
    } catch (error) {
        console.error('Error al obtener las publicaciones:', error);
    }
}


//Función para obtener desde Threads los comentarios de cada publicación
async function obtenerComentariosThreads() {
    
    const rutaArchivoLectura = path.join(directorio, 'IdPostBuscado.txt');
    try {
        let idsPublicaciones = [];
        // Leer el archivo línea por línea
        try {
            // Leer el contenido del archivo como un string
            const data = fs.readFileSync(rutaArchivoLectura, 'utf-8');

            // Dividir el string en un array de líneas
            idsPublicaciones = data.split('\n');
        } catch (error) {
            console.error('Error al leer el archivo:', error);
        }
        console.log(idsPublicaciones)
        for (let id of idsPublicaciones) {
            let tokenSiguientePagina = null;
            do {
                const paginaActual = await cliente.posts.fetch(id, tokenSiguientePagina);
                paginaActual.id = id;
                //const postID = paginaActual.containing_thread.thread_items[0].post.id;
                const fileName = `PaginaComentariosPost_${tokenSiguientePagina}.json`;
                const rutaArchivoEscritura = path.join(directorio, fileName);
                // Escribir los posts de la página actual en un archivo JSON
                fs.writeFileSync(rutaArchivoEscritura, JSON.stringify(paginaActual, null, 2), 'utf-8');
                if (paginaActual.paging_tokens.downwards) {
                    tokenSiguientePagina = paginaActual.paging_tokens.downwards;
                } else {
                    tokenSiguientePagina = null;
                }
                const tiempoDeEspera = obtenerTiempoAleatorio(10, 15);
                await new Promise(resolve => setTimeout(resolve, tiempoDeEspera));
            } while (tokenSiguientePagina);
        }
    } catch (error) {
        console.error('Error fetching threads:', error);
    }
}



const usuario = process.env.USUARIO;
const contrasena = process.env.CONTRASENA;
const publicacionesBuscadas = process.env.PUBLICACIONES_BUSCADAS.split(',');
const directorio = path.join(__dirname, '..', 'data', 'raw');

const cliente = new Client();

(async () => {
    try {
        await iniciarSesion();
        await obtenerPublicacionesThreads();
        await obtenerComentariosThreads(); 
    } catch (error) {
        console.error('Error:', error);
    }
})();
