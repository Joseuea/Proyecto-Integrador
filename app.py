"""
app.py - Aplicación web de JM Ferretería
Rutas del sistema y datos que se envían a las plantillas.
"""

from flask import Flask, render_template, redirect, url_for, flash

from forms import ProductoForm, ClienteForm, ProveedorForm, FacturacionForm

app = Flask(__name__)

# Clave necesaria para la protección CSRF de los formularios
app.config['SECRET_KEY'] = 'jm-ferreteria-clave-secreta-2026'


# ----------------------------------------------------------
# Datos generales del negocio
# Son variables simples que se usan en todas las páginas
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


# ----------------------------------------------------------
# Datos de ejemplo
# Por ahora la información está en listas de diccionarios.
# Más adelante estos datos vendrán de una base de datos.
# ----------------------------------------------------------

productos_lista = [
    {"codigo": "P001", "nombre": "Cemento Selvalegre 50 kg", "categoria": "Cemento", "stock": 120, "precio": 8.50},
    {"codigo": "P002", "nombre": "Bloque de 15 cm", "categoria": "Bloques", "stock": 850, "precio": 0.65},
    {"codigo": "P003", "nombre": "Varilla de hierro 12 mm", "categoria": "Hierro", "stock": 240, "precio": 12.30},
    {"codigo": "P004", "nombre": "Malla Armex R-84", "categoria": "Hierro", "stock": 45, "precio": 28.90},
    {"codigo": "P005", "nombre": "Tubería Plastigama 110 mm", "categoria": "Tuberías", "stock": 0, "precio": 18.75},
    {"codigo": "P006", "nombre": "Bondex Intaco 25 kg", "categoria": "Acabados", "stock": 75, "precio": 9.40},
    {"codigo": "P007", "nombre": "Metro cúbico de ripio", "categoria": "Áridos", "stock": 30, "precio": 22.00},
    {"codigo": "P008", "nombre": "Polvo azul (saco)", "categoria": "Áridos", "stock": 0, "precio": 6.80},
]

clientes_lista = [
    {"cedula": "1719283746", "nombre": "Rosa Simbaña", "telefono": "0991234567", "ciudad": "Quito", "tipo": "Frecuente", "activo": True},
    {"cedula": "1712345678", "nombre": "Luis Guamán", "telefono": "0987654321", "ciudad": "Calderón", "tipo": "Mayorista", "activo": True},
    {"cedula": "1798765432", "nombre": "Constructora Andina S.A.", "telefono": "022345678", "ciudad": "Quito", "tipo": "Empresa", "activo": True},
    {"cedula": "1701122334", "nombre": "Marco Tipán", "telefono": "0962959355", "ciudad": "Carapungo", "tipo": "Ocasional", "activo": False},
]

proveedores_lista = [
    {"ruc": "1790012345001", "empresa": "Holcim Ecuador", "producto": "Cemento", "contacto": "Ing. Pedro Salas", "telefono": "023456789", "convenio": True},
    {"ruc": "1790067890001", "empresa": "Adelca", "producto": "Hierro y varillas", "contacto": "Sra. Ana Lema", "telefono": "023987654", "convenio": True},
    {"ruc": "1790054321001", "empresa": "Plastigama", "producto": "Tuberías y accesorios", "contacto": "Ing. Jorge Vaca", "telefono": "024567890", "convenio": False},
    {"ruc": "1790098765001", "empresa": "Intaco Ecuador", "producto": "Bondex y acabados", "contacto": "Sr. Diego Cruz", "telefono": "025678901", "convenio": True},
]

facturas_lista = [
    {"numero": "001-001-000125", "fecha": "2026-08-02", "cliente": "Rosa Simbaña", "total": 245.80, "estado": "Pagada"},
    {"numero": "001-001-000126", "fecha": "2026-08-05", "cliente": "Luis Guamán", "total": 480.00, "estado": "Pendiente"},
    {"numero": "001-001-000127", "fecha": "2026-08-08", "cliente": "Constructora Andina S.A.", "total": 1320.50, "estado": "Pagada"},
    {"numero": "001-001-000128", "fecha": "2026-08-12", "cliente": "Marco Tipán", "total": 96.25, "estado": "Pendiente"},
]

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
# Rutas de la aplicación
# ----------------------------------------------------------

@app.route('/')
def index():
    """Página principal informativa de la ferretería."""
    return render_template(
        'index.html',
        titulo_modulo="Inicio",
        contacto=informacion_contacto,
        productos=productos_lista
    )


@app.route('/productos')
def productos():
    """Módulo de productos: muestra el inventario de materiales."""
    # Cuento cuántos productos están agotados
    agotados = [p for p in productos_lista if p["stock"] == 0]

    return render_template(
        'productos.html',
        titulo_modulo="Productos",
        productos=productos_lista,
        total_agotados=len(agotados)
    )


@app.route('/clientes')
def clientes():
    """Módulo de clientes: muestra los clientes registrados."""
    return render_template(
        'clientes.html',
        titulo_modulo="Clientes",
        clientes=clientes_lista
    )


@app.route('/proveedores')
def proveedores():
    """Módulo de proveedores: muestra las empresas que nos abastecen."""
    return render_template(
        'proveedores.html',
        titulo_modulo="Proveedores",
        proveedores=proveedores_lista
    )


@app.route('/facturacion')
def facturacion():
    """Módulo de facturación: muestra las facturas emitidas."""
    # Calculo los totales para mostrarlos como resumen
    total_facturado = sum(factura["total"] for factura in facturas_lista)
    total_pendiente = sum(f["total"] for f in facturas_lista if f["estado"] == "Pendiente")

    return render_template(
        'facturacion.html',
        titulo_modulo="Facturación",
        facturas=facturas_lista,
        total_facturado=total_facturado,
        total_pendiente=total_pendiente
    )



# ----------------------------------------------------------
# Rutas de los formularios
# Cada una acepta GET para mostrar el formulario
# y POST para procesar los datos enviados.
# ----------------------------------------------------------

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    """Registra un producto nuevo en el inventario."""
    form = ProductoForm()

    # validate_on_submit() es True solo si se envió por POST y pasó las validaciones
    if form.validate_on_submit():
        productos_lista.append({
            "codigo": form.codigo.data.upper(),
            "nombre": form.nombre.data,
            "categoria": form.categoria.data,
            "stock": form.stock.data,
            "precio": form.precio.data
        })
        flash(f"El producto {form.nombre.data} fue registrado correctamente.", "success")
        return redirect(url_for('productos'))

    return render_template(
        'formulario_producto.html',
        titulo_modulo="Nuevo producto",
        form=form,
        accion="Registrar"
    )


@app.route('/productos/editar/<codigo>', methods=['GET', 'POST'])
def editar_producto(codigo):
    """Edita un producto usando la misma clase de formulario."""
    # Busco el producto por su código
    producto = next((p for p in productos_lista if p["codigo"] == codigo), None)

    if producto is None:
        flash("El producto solicitado no existe.", "danger")
        return redirect(url_for('productos'))

    # obj=producto carga los datos actuales en el formulario
    form = ProductoForm(data=producto)

    if form.validate_on_submit():
        producto["codigo"] = form.codigo.data.upper()
        producto["nombre"] = form.nombre.data
        producto["categoria"] = form.categoria.data
        producto["stock"] = form.stock.data
        producto["precio"] = form.precio.data
        flash(f"El producto {form.nombre.data} fue actualizado.", "success")
        return redirect(url_for('productos'))

    return render_template(
        'formulario_producto.html',
        titulo_modulo="Editar producto",
        form=form,
        accion="Actualizar"
    )


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    """Registra un cliente nuevo."""
    form = ClienteForm()

    if form.validate_on_submit():
        clientes_lista.append({
            "cedula": form.cedula.data,
            "nombre": form.nombre.data,
            "telefono": form.telefono.data,
            "correo": form.correo.data,
            "ciudad": form.ciudad.data,
            "tipo": form.tipo.data,
            "activo": form.activo.data
        })
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
        proveedores_lista.append({
            "ruc": form.ruc.data,
            "empresa": form.empresa.data,
            "producto": form.producto.data,
            "contacto": form.contacto.data,
            "telefono": form.telefono.data,
            "correo": form.correo.data,
            "convenio": form.convenio.data
        })
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

    # Cargo la lista de clientes en el desplegable
    form.cliente.choices = [("", "-- Seleccione un cliente --")] + [
        (c["nombre"], c["nombre"]) for c in clientes_lista
    ]

    if form.validate_on_submit():
        facturas_lista.append({
            "numero": form.numero.data,
            "fecha": form.fecha.data.strftime("%Y-%m-%d"),
            "cliente": form.cliente.data,
            "total": form.total.data,
            "estado": form.estado.data
        })
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
