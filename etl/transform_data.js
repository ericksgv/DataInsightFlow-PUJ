const fs = require('fs');
const path = require('path');

// Directorios de entrada y salida

// Ruta al directorio 'raw'
const directorioRaw = path.join(__dirname, '..', 'data', 'raw');

// Ruta al directorio 'processed'
const directorioProcessed = path.join(__dirname, '..', 'data', 'processed');

// Función principal para generar el JSON de publicaciones
function generarJSONPublicaciones() {
    try {
        // Nombre del archivo de entrada
        const nombreArchivoLectura = 'publicaciones.json';
        const rutaArchivoLectura = path.join(directorioRaw, nombreArchivoLectura);
        const publicacionesJSON = fs.readFileSync(rutaArchivoLectura, 'utf-8');
        const contenido = JSON.parse(publicacionesJSON);
        const publicaciones = contenido.publicaciones;

        // Verificar si el contenido de publicaciones es un arreglo
        if (!Array.isArray(publicaciones)) {
            throw new TypeError('La propiedad "publicaciones" no es un arreglo o no existe en el archivo JSON');
        }

        const publicacionesSalida = [];

        // Procesar cada publicación
        publicaciones.forEach(publicacion => {
            // Obtener el ID de la publicación
            const post_id = publicacion.media.id.split('_')[0];
            // Obtener la descripción de la publicación si existe
            let usuario = "";
            let descripcion = "";
            if (publicacion.media.caption !== null) {
                descripcion = publicacion.media.caption.text;
            }
            if (publicacion.media.user.username !== null) {
                usuario = publicacion.media.user.username;
            }
            // Inicializar el arreglo de comentarios
            const comentarios = [];
            // Convertir el timestamp a una fecha legible
            const fecha = convertirTimestampALegible(publicacion.media.device_timestamp);
            // Definir la fuente de la publicación
            const fuente = "Threads";
            const enlace = publicacion.media.permalink
            // Crear objeto de salida para la publicación actual
            const publicacionSalida = {
                id: post_id,
                usuario: usuario,
                descripcion: descripcion,
                comentarios: comentarios,
                fecha: fecha,
                fuente: fuente,
                enlace: enlace
            };
            // Agregar la publicación procesada al arreglo de salida
            publicacionesSalida.push(publicacionSalida);
        });

        const datosAguardar = { "publicaciones": publicacionesSalida };
        const jsonStr = JSON.stringify(datosAguardar, null, 2);
        const nombreArchivoEscritura = 'publicaciones.json';
        const rutaArchivoEscritura = path.join(directorioProcessed, nombreArchivoEscritura);
        // Escribir el JSON procesado en el archivo de salida
        fs.writeFileSync(rutaArchivoEscritura, jsonStr, { encoding: 'utf-8', flag: 'w' });

    } catch (error) {
        console.error(`Error al procesar el archivo: ${error}`);
    }
}

// Función para generar el JSON de comentarios
function generarJSONComentarios() {
    try {
        let comentarios = [];
        const nombreArchivoEscritura = 'comentarios.json';
        const rutaArchivoEscritura = path.join(directorioProcessed, nombreArchivoEscritura);

        // Verificar si el archivo de salida existe y eliminarlo si es así
        if (fs.existsSync(rutaArchivoEscritura)) {
            fs.unlinkSync(rutaArchivoEscritura);
        }

        // Obtener la lista de archivos JSON que contienen comentarios
        const archivosJSON = fs.readdirSync(directorioRaw).filter(file => file.includes('PaginaComentariosPost_'));

        archivosJSON.forEach(file => {
            try {
                const filePath = path.join(directorioRaw, file);
                const datos = JSON.parse(fs.readFileSync(filePath, 'utf-8'));

                // Verificar si hay hilos de respuestas
                if (datos.reply_threads.length > 0) {
                    for (const thread of datos.reply_threads) {
                        for (const comentario of thread.thread_items) {
                            if (comentario.post.caption != null) {
                                // Agregar el comentario al arreglo de comentarios
                                comentarios.push({
                                    "id": datos.id,
                                    "usuario": comentario.post.user.username,
                                    "descripcion": comentario.post.caption.text,
                                    "reacciones": comentario.post.like_count,
                                    "fecha": convertirTimestampALegible(comentario.post.device_timestamp)
                                });
                            }
                        }
                    }
                }
            } catch (error) {
                console.error(`Error al procesar el archivo ${file}: ${error}`);
            }
        });

        // Escribir todos los comentarios en el archivo JSON
        const nuevoContenido = JSON.stringify({ comentarios }, null, 2);
        fs.writeFileSync(rutaArchivoEscritura, nuevoContenido, 'utf-8');
    } catch (error) {
        console.error(`Error al procesar los comentarios: ${error}`);
    }
}

// Función para generar el JSON de publicaciones y comentarios
function generarJSONPublicacionesYComentarios() {
    try {
        // Leer los archivos JSON de publicaciones y comentarios
        const nombreArchivoPublicaciones = 'publicaciones.json';
        const rutaArchivoLectura = path.join(directorioProcessed, nombreArchivoPublicaciones);
        const publicacionesJSON = fs.readFileSync(rutaArchivoLectura, 'utf-8');

        const nombreArchivoComentarios = 'comentarios.json';
        const rutaArchivoEscritura = path.join(directorioProcessed, nombreArchivoComentarios);
        const comentariosJSON = fs.readFileSync(rutaArchivoEscritura, 'utf-8');

        const publicaciones = JSON.parse(publicacionesJSON).publicaciones;
        const comentarios = JSON.parse(comentariosJSON).comentarios;

        // Agrupar los comentarios por ID de publicación
        const comentariosPorPublicacion = comentarios.reduce((acc, comentario) => {
            if (!acc[comentario.id]) {
                acc[comentario.id] = [];
            }
            const { id, ...comentarioSinId } = comentario;
            acc[comentario.id].push(comentarioSinId);
            return acc;
        }, {});

        // Agregar los comentarios a las publicaciones correspondientes
        publicaciones.forEach(publicacion => {
            const comentariosDePublicacion = comentariosPorPublicacion[publicacion.id];
            if (comentariosDePublicacion) {
                publicacion.comentarios = comentariosDePublicacion;
            } else {
                publicacion.comentarios = [];
            }
        });

        // Ruta de salida para el archivo JSON
        const nombreArchivoPublicacionesComentarios = 'publicacionesYComentarios.json';
        const rutaSalida = path.join(directorioProcessed, nombreArchivoPublicacionesComentarios);


        // Escribir el JSON modificado en el archivo de salida
        const nuevoContenido = JSON.stringify({ publicaciones }, null, 2);
        fs.writeFileSync(rutaSalida, nuevoContenido, 'utf-8');
    } catch (error) {
        console.error('Error al procesar los archivos JSON:', error.message);
    }
}

// Función para convertir un timestamp en microsegundos a una fecha legible
function convertirTimestampALegible(timestamp) {
    const milisegundos = timestamp / 1000;
    const fecha = new Date(milisegundos);
    const dia = fecha.getDate();
    const mes = fecha.getMonth() + 1;
    const año = fecha.getFullYear();
    return `${dia}-${mes}-${año}`;
}

// Ejecutar las funciones
generarJSONPublicaciones();
generarJSONComentarios();
generarJSONPublicacionesYComentarios();
