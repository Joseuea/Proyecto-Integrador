/* ==============================================
   script.js - Solicitudes de cotización
   Registrar, mostrar, contar y eliminar sin
   recargar la página, con validaciones.
   ============================================== */

/* Elementos de la página que voy a usar */
const formularioPedido = document.getElementById("formularioPedido");
const campoNombre = document.getElementById("campoNombre");
const campoDescripcion = document.getElementById("campoDescripcion");
const campoCategoria = document.getElementById("campoCategoria");
const errorNombre = document.getElementById("errorNombre");
const errorDescripcion = document.getElementById("errorDescripcion");
const errorCategoria = document.getElementById("errorCategoria");
const alertaFormulario = document.getElementById("alertaFormulario");
const listaPedidos = document.getElementById("listaPedidos");
const contadorPedidos = document.getElementById("contadorPedidos");
const mensajeVacio = document.getElementById("mensajeVacio");

/* Arreglo con las solicitudes (más adelante estos datos vendrán de una base de datos con Flask) */
let solicitudes = [
    { id: 1, nombre: "Rosa Simbaña", descripcion: "20 quintales de cemento Selvalegre y 100 bloques de 15 cm.", categoria: "Cemento y bloques" },
    { id: 2, nombre: "Luis Guamán", descripcion: "Flete de una volqueta de ripio hasta Calderón, sector San José.", categoria: "Flete o mudanza" }
];

let siguienteId = 3; // id para la próxima solicitud

/* ---------- Validaciones ---------- */

// El nombre no puede estar vacío y debe tener mínimo 3 caracteres
function validarNombre() {
    const valor = campoNombre.value.trim();

    if (valor === "") {
        marcarInvalido(campoNombre);
        errorNombre.textContent = "El nombre es obligatorio.";
        return false;
    }

    if (valor.length < 3) {
        marcarInvalido(campoNombre);
        errorNombre.textContent = "El nombre debe tener al menos 3 caracteres.";
        return false;
    }

    marcarValido(campoNombre);
    return true;
}

// La descripción no puede estar vacía y debe tener mínimo 10 caracteres
function validarDescripcion() {
    const valor = campoDescripcion.value.trim();

    if (valor === "") {
        marcarInvalido(campoDescripcion);
        errorDescripcion.textContent = "La descripción es obligatoria.";
        return false;
    }

    if (valor.length < 10) {
        marcarInvalido(campoDescripcion);
        errorDescripcion.textContent = "La descripción debe tener al menos 10 caracteres.";
        return false;
    }

    marcarValido(campoDescripcion);
    return true;
}

// Debe elegirse una categoría de la lista
function validarCategoria() {
    if (campoCategoria.value === "") {
        marcarInvalido(campoCategoria);
        errorCategoria.textContent = "Debe seleccionar una categoría.";
        return false;
    }

    marcarValido(campoCategoria);
    return true;
}

// Pinta el campo de rojo cuando hay error
function marcarInvalido(campo) {
    campo.classList.add("is-invalid");
    campo.classList.remove("is-valid");
}

// Pinta el campo de verde cuando está correcto
function marcarValido(campo) {
    campo.classList.add("is-valid");
    campo.classList.remove("is-invalid");
}

// Muestra una alerta general y la oculta a los 3 segundos
function mostrarAlerta(mensaje, tipo) {
    alertaFormulario.textContent = mensaje;
    alertaFormulario.className = "alert mt-3 alert-" + tipo;
    setTimeout(function () {
        alertaFormulario.className = "alert mt-3 d-none";
    }, 3000);
}

/* ---------- Mostrar las solicitudes en pantalla ---------- */

function renderizarSolicitudes() {
    listaPedidos.innerHTML = ""; // limpio la lista antes de volver a dibujarla

    // Si no hay solicitudes, muestro el mensaje de lista vacía
    if (solicitudes.length === 0) {
        mensajeVacio.classList.remove("d-none");
    } else {
        mensajeVacio.classList.add("d-none");
    }

    // Recorro el arreglo y creo una tarjeta por cada solicitud
    for (let i = 0; i < solicitudes.length; i++) {
        const solicitud = solicitudes[i];

        const columna = document.createElement("div");
        columna.className = "col-12";

        const tarjeta = document.createElement("div");
        tarjeta.className = "card shadow-sm tarjeta-pedido";

        const cuerpo = document.createElement("div");
        cuerpo.className = "card-body";

        const fila = document.createElement("div");
        fila.className = "d-flex justify-content-between align-items-start";

        const contenido = document.createElement("div");

        const titulo = document.createElement("h4");
        titulo.className = "fs-6 fw-bold mb-1";
        titulo.textContent = solicitud.id + ". " + solicitud.nombre;

        const categoria = document.createElement("span");
        categoria.className = "badge bg-obra mb-2";
        categoria.textContent = solicitud.categoria;

        const descripcion = document.createElement("p");
        descripcion.className = "m-0 text-muted";
        descripcion.textContent = solicitud.descripcion;

        const botonEliminar = document.createElement("button");
        botonEliminar.className = "btn btn-outline-danger btn-sm";
        botonEliminar.textContent = "🗑 Eliminar";

        // Al hacer clic en el botón se elimina esta solicitud
        botonEliminar.addEventListener("click", function () {
            eliminarSolicitud(solicitud.id);
        });

        // Armo la tarjeta y la agrego a la página
        contenido.appendChild(titulo);
        contenido.appendChild(categoria);
        contenido.appendChild(descripcion);
        fila.appendChild(contenido);
        fila.appendChild(botonEliminar);
        cuerpo.appendChild(fila);
        tarjeta.appendChild(cuerpo);
        columna.appendChild(tarjeta);
        listaPedidos.appendChild(columna);
    }

    actualizarContador();
}

// Actualiza el total de solicitudes
function actualizarContador() {
    contadorPedidos.textContent = "Total: " + solicitudes.length;
}

/* ---------- Registrar y eliminar ---------- */

// Agrega la solicitud del formulario al arreglo
function registrarSolicitud() {
    const nuevaSolicitud = {
        id: siguienteId,
        nombre: campoNombre.value.trim(),
        descripcion: campoDescripcion.value.trim(),
        categoria: campoCategoria.value
    };

    solicitudes.push(nuevaSolicitud);
    siguienteId = siguienteId + 1;
    renderizarSolicitudes();
}

// Elimina la solicitud que tenga el id indicado
function eliminarSolicitud(id) {
    solicitudes = solicitudes.filter(function (solicitud) {
        return solicitud.id !== id;
    });

    renderizarSolicitudes();
    mostrarAlerta("La solicitud fue eliminada correctamente.", "success");
}

// Limpia el formulario y quita los colores de validación
function limpiarFormulario() {
    formularioPedido.reset();
    campoNombre.classList.remove("is-valid", "is-invalid");
    campoDescripcion.classList.remove("is-valid", "is-invalid");
    campoCategoria.classList.remove("is-valid", "is-invalid");
}

/* ---------- Eventos ---------- */

// Al enviar el formulario: valido todo y, si está correcto, registro
formularioPedido.addEventListener("submit", function (evento) {
    evento.preventDefault(); // evita que la página se recargue

    const nombreValido = validarNombre();
    const descripcionValida = validarDescripcion();
    const categoriaValida = validarCategoria();

    if (nombreValido && descripcionValida && categoriaValida) {
        registrarSolicitud();
        limpiarFormulario();
        mostrarAlerta("¡Solicitud registrada con éxito! Pronto nos contactaremos.", "success");
    } else {
        mostrarAlerta("Revise los campos marcados en rojo.", "danger");
    }
});

// Validaciones en tiempo real mientras el usuario escribe
campoNombre.addEventListener("input", validarNombre);
campoNombre.addEventListener("blur", validarNombre);
campoDescripcion.addEventListener("input", validarDescripcion);
campoDescripcion.addEventListener("blur", validarDescripcion);
campoCategoria.addEventListener("change", validarCategoria);

/* Al cargar la página muestro las solicitudes de ejemplo */
renderizarSolicitudes();
