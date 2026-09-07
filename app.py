"""
app.py - Aplicación web de JM Ferretería
Rutas del sistema, formularios y conexión con la base de datos.
"""

from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect

import database as bd
from forms import ProductoForm, ClienteForm, ProveedorForm, FacturacionForm

app = Flask(__name__)

# Clave necesaria para la protección CSRF de los formularios
app.config['SECRET_KEY'] = 'jm-ferreteria-clave-secreta-2026'

# Activa la protección CSRF en toda la aplicación
csrf = CSRFProtect(app)

# Preparo la base de datos al iniciar la aplicación
bd.crear_tablas()
bd.cargar_datos_iniciales()


# ----------------------------------------------------------
# Datos generales del negocio
# ----------------------------------------------------------

EMPRESA = "JM Ferretería"
LEMA = "Construyendo tus sueños"
CIUDAD = "Carapungo, Quito"
ESTUDIANTE = "José Quiroz"
ASIGNATURA = "Desarrollo de Aplicaciones Web"
ANIO = 2026


@app.context_processor
def datos_generales():
    """Envía estas variables a todas las plantillas sin repetirlas en cada ruta."""
    return {
        "empresa": EMPRESA,
        "lema": LEMA,
        "ciudad": CIUDAD,
        "estudiante": ESTUDIANTE,
        "asignatura": ASIGNATURA,
        "anio": ANIO
    }


# Diccionario con la información de contacto del negocio
informacion_contacto = {
    "propietario": "Sr. Javier Chávez",
    "administrador": "Ing. Milton Chávez",
    "correo": "miljavierferreteria@hotmail.com",
    "telefono1": "098 367 7076",
    "telefono2": "096 295 9355",
    "direccion": "Panamericana Norte, sector del hierro y los cisnes, Carapungo, Quito",
    "horario": "Lunes a sábado, de 07h30 a 18h00"
}


# ----------------------------------------------------------
# Rutas de los módulos
# ----------------------------------------------------------

@app.route('/')
def index():
    """Página principal informativa de la ferretería."""
    return render_template(
        'index.html',
        titulo_modulo="Inicio",
        contacto=informacion_contacto,
        productos=bd.listar_productos()
    )


@app.route('/productos')
def productos():
    """Módulo de productos: consulta el inventario guardado en la base de datos."""
    return render_template(
        'productos.html',
        titulo_modulo="Productos",
        productos=bd.listar_productos(),
        total_agotados=bd.contar_agotados()
    )


@app.route('/clientes')
def clientes():
    """Módulo de clientes: consulta los clientes guardados."""
    return render_template(
        'clientes.html',
        titulo_modulo="Clientes",
        clientes=bd.listar_clientes()
    )


@app.route('/proveedores')
def proveedores():
    """Módulo de proveedores: consulta los proveedores guardados."""
    return render_template(
        'proveedores.html',
        titulo_modulo="Proveedores",
        proveedores=bd.listar_proveedores()
    )


@app.route('/facturacion')
def facturacion():
    """Módulo de facturación: consulta las facturas guardadas."""
    total_facturado, total_pendiente = bd.totales_facturacion()

    return render_template(
        'facturacion.html',
        titulo_modulo="Facturación",
        facturas=bd.listar_facturas(),
        total_facturado=total_facturado,
        total_pendiente=total_pendiente
    )


# ----------------------------------------------------------
# Rutas de los formularios
# Aceptan GET para mostrar el formulario y POST para guardar.
# ----------------------------------------------------------

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    """Registra un producto nuevo en la base de datos."""
    form = ProductoForm()

    # Solo entra aquí si se envió por POST y pasó todas las validaciones
    if form.validate_on_submit():
        codigo = form.codigo.data.upper()

        # Reviso que el código no esté repetido
        if bd.existe_codigo(codigo):
            flash(f"Ya existe un producto con el código {codigo}.", "danger")
        else:
            bd.agregar_producto(
                codigo,
                form.nombre.data,
                form.categoria.data,
                form.stock.data,
                form.precio.data
            )
            flash(f"El producto {form.nombre.data} fue registrado correctamente.", "success")
            return redirect(url_for('productos'))

    return render_template(
        'formulario_producto.html',
        titulo_modulo="Nuevo producto",
        form=form,
        accion="Registrar"
    )


@app.route('/productos/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    """Edita un producto usando la misma clase de formulario."""
    producto = bd.obtener_producto(id_producto)

    if producto is None:
        flash("El producto solicitado no existe.", "danger")
        return redirect(url_for('productos'))

    # Cargo los datos actuales del producto en el formulario
    form = ProductoForm(data=producto)

    if form.validate_on_submit():
        codigo = form.codigo.data.upper()

        if bd.existe_codigo(codigo, id_excluir=id_producto):
            flash(f"Ya existe otro producto con el código {codigo}.", "danger")
        else:
            bd.actualizar_producto(
                id_producto,
                codigo,
                form.nombre.data,
                form.categoria.data,
                form.stock.data,
                form.precio.data
            )
            flash(f"El producto {form.nombre.data} fue actualizado.", "success")
            return redirect(url_for('productos'))

    return render_template(
        'formulario_producto.html',
        titulo_modulo="Editar producto",
        form=form,
        accion="Actualizar"
    )


@app.route('/productos/eliminar/<int:id_producto>', methods=['POST'])
def borrar_producto(id_producto):
    """Elimina un producto de la base de datos."""
    producto = bd.obtener_producto(id_producto)

    if producto is None:
        flash("El producto solicitado no existe.", "danger")
    else:
        bd.eliminar_producto(id_producto)
        flash(f"El producto {producto['nombre']} fue eliminado.", "success")

    return redirect(url_for('productos'))


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    """Registra un cliente nuevo."""
    form = ClienteForm()

    if form.validate_on_submit():
        bd.agregar_cliente(
            form.cedula.data,
            form.nombre.data,
            form.telefono.data,
            form.correo.data,
            form.ciudad.data,
            form.tipo.data,
            1 if form.activo.data else 0
        )
        flash(f"El cliente {form.nombre.data} fue registrado correctamente.", "success")
        return redirect(url_for('clientes'))

    return render_template(
        'formulario_cliente.html',
        titulo_modulo="Nuevo cliente",
        form=form,
        accion="Registrar"
    )


@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def nuevo_proveedor():
    """Registra un proveedor nuevo."""
    form = ProveedorForm()

    if form.validate_on_submit():
        bd.agregar_proveedor(
            form.ruc.data,
            form.empresa.data,
            form.producto.data,
            form.contacto.data,
            form.telefono.data,
            form.correo.data,
            1 if form.convenio.data else 0
        )
        flash(f"El proveedor {form.empresa.data} fue registrado correctamente.", "success")
        return redirect(url_for('proveedores'))

    return render_template(
        'formulario_proveedor.html',
        titulo_modulo="Nuevo proveedor",
        form=form,
        accion="Registrar"
    )


@app.route('/facturacion/nueva', methods=['GET', 'POST'])
def nueva_factura():
    """Registra una factura nueva."""
    form = FacturacionForm()

    # Cargo en el desplegable los clientes guardados en la base de datos
    form.cliente.choices = [("", "-- Seleccione un cliente --")] + [
        (c["nombre"], c["nombre"]) for c in bd.listar_clientes()
    ]

    if form.validate_on_submit():
        bd.agregar_factura(
            form.numero.data,
            form.fecha.data.strftime("%Y-%m-%d"),
            form.cliente.data,
            form.total.data,
            form.estado.data
        )
        flash(f"La factura {form.numero.data} fue registrada correctamente.", "success")
        return redirect(url_for('facturacion'))

    return render_template(
        'formulario_facturacion.html',
        titulo_modulo="Nueva factura",
        form=form,
        accion="Registrar"
    )


# ----------------------------------------------------------
# Ejecución de la aplicación
# ----------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
