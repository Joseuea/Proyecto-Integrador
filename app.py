"""
app.py - Aplicación web de JM Ferretería
Rutas del sistema y datos que se envían a las plantillas.
"""

from flask import Flask, render_template

app = Flask(__name__)

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
# Ejecución de la aplicación
# ----------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
