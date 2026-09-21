"""
app.py - Aplicación web de JM Ferretería
Rutas del sistema, formularios y conexión con la base de datos.
"""

import os

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf.csrf import CSRFProtect
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

import database as bd
import conexion
import models
from forms import (
    ProductoForm, ClienteForm, ProveedorForm, FacturacionForm,
    LoginForm, UsuarioForm
)

app = Flask(__name__)

# Clave necesaria para las sesiones y la protección CSRF de los formularios
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'jm-ferreteria-clave-secreta-2026')

# Activa la protección CSRF en toda la aplicación
csrf = CSRFProtect(app)

# ----------------------------------------------------------
# Configuración del sistema de login
# ----------------------------------------------------------

login_manager = LoginManager(app)

# Si alguien entra a una página protegida sin sesión, lo envío al login
login_manager.login_view = 'login'
login_manager.login_message = "Debe iniciar sesión para acceder a esta página."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(id_usuario):
    """Flask-Login usa esta función para recuperar al usuario de la sesión."""
    return models.buscar_por_id(id_usuario)

# Compruebo que la base de datos MySQL responda al iniciar
if conexion.probar_conexion():
    print("Conexión con MySQL establecida correctamente.")
else:
    print("ATENCIÓN: no se pudo conectar con MySQL.")
    print("Revise que el servidor esté encendido y que haya ejecutado sql/esquema.sql")


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


def cargar_proveedores(form):
    """Llena el desplegable de proveedores del formulario de productos."""
    form.id_proveedor.choices = [("", "-- Sin proveedor asignado --")] + [
        (str(p["id_proveedor"]), p["empresa"]) for p in bd.listar_proveedores()
    ]


# ----------------------------------------------------------
# Rutas del sistema de login
# ----------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Muestra el formulario de acceso y comprueba las credenciales."""
    # Si el usuario ya inició sesión, lo mando directo al panel
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()

    if form.validate_on_submit():
        # Busco el usuario en la base de datos
        usuario = models.buscar_por_usuario(form.usuario.data)

        # check_password_hash compara la contraseña escrita con el hash guardado
        if usuario and check_password_hash(usuario.password, form.password.data):
            login_user(usuario)
            flash(f"Bienvenido, {usuario.nombre}.", "success")

            # Si venía de una página protegida, lo devuelvo a esa página
            siguiente = request.args.get('next')
            if siguiente and siguiente.startswith('/'):
                return redirect(siguiente)
            return redirect(url_for('dashboard'))

        # El mismo mensaje para usuario inexistente o contraseña incorrecta,
        # así no se revela cuál de los dos datos está mal
        flash("Usuario o contraseña incorrectos.", "danger")

    return render_template('login.html', titulo_modulo="Iniciar sesión", form=form)


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Registra un usuario nuevo guardando su contraseña con hash."""
    form = UsuarioForm()

    if form.validate_on_submit():
        nombre_usuario = form.usuario.data.strip().lower()

        if models.existe_usuario(nombre_usuario):
            flash(f"El usuario {nombre_usuario} ya está registrado.", "danger")
        else:
            # Nunca guardo la contraseña tal cual: guardo su hash
            clave_cifrada = generate_password_hash(form.password.data)
            models.crear_usuario(nombre_usuario, form.nombre.data, clave_cifrada)

            flash("Usuario registrado correctamente. Ya puede iniciar sesión.", "success")
            return redirect(url_for('login'))

    return render_template('registro.html', titulo_modulo="Registro de usuario", form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    """Panel principal del sistema. Solo se ve con la sesión iniciada."""
    total_facturado, total_pendiente = bd.totales_facturacion()

    return render_template(
        'dashboard.html',
        titulo_modulo="Panel de administración",
        total_productos=len(bd.listar_productos()),
        total_agotados=bd.contar_agotados(),
        total_clientes=len(bd.listar_clientes()),
        total_proveedores=len(bd.listar_proveedores()),
        total_facturas=len(bd.listar_facturas()),
        total_facturado=total_facturado,
        total_pendiente=total_pendiente
    )


@app.route('/logout')
@login_required
def logout():
    """Cierra la sesión del usuario."""
    logout_user()
    flash("Su sesión fue cerrada correctamente.", "success")
    return redirect(url_for('login'))


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
@login_required
def productos():
    """Módulo de productos: consulta el inventario guardado en la base de datos."""
    return render_template(
        'productos.html',
        titulo_modulo="Productos",
        productos=bd.listar_productos(),
        total_agotados=bd.contar_agotados()
    )


@app.route('/clientes')
@login_required
def clientes():
    """Módulo de clientes: consulta los clientes guardados."""
    return render_template(
        'clientes.html',
        titulo_modulo="Clientes",
        clientes=bd.listar_clientes()
    )


@app.route('/proveedores')
@login_required
def proveedores():
    """Módulo de proveedores: consulta los proveedores guardados."""
    return render_template(
        'proveedores.html',
        titulo_modulo="Proveedores",
        proveedores=bd.listar_proveedores()
    )


@app.route('/facturacion')
@login_required
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
@login_required
def nuevo_producto():
    """Registra un producto nuevo en la base de datos."""
    form = ProductoForm()
    cargar_proveedores(form)

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
                form.precio.data,
                form.id_proveedor.data or None
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
@login_required
def editar_producto(id_producto):
    """Edita un producto usando la misma clase de formulario."""
    producto = bd.obtener_producto(id_producto)

    if producto is None:
        flash("El producto solicitado no existe.", "danger")
        return redirect(url_for('productos'))

    # Cargo los datos actuales del producto en el formulario
    if producto.get("id_proveedor") is not None:
        producto["id_proveedor"] = str(producto["id_proveedor"])

    form = ProductoForm(data=producto)
    cargar_proveedores(form)

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
                form.precio.data,
                form.id_proveedor.data or None
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
@login_required
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
@login_required
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
@login_required
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
@login_required
def nueva_factura():
    """Registra una factura nueva."""
    form = FacturacionForm()

    # El desplegable guarda el id_cliente, que es la clave foránea
    form.cliente.choices = [("", "-- Seleccione un cliente --")] + [
        (str(c["id_cliente"]), c["nombre"]) for c in bd.listar_clientes()
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
