"""
database.py - Conexión y consultas a la base de datos SQLite.
Aquí están todas las funciones que crean las tablas, guardan
y recuperan la información de la ferretería.
"""

import os
import sqlite3

# Ruta donde se guarda la base de datos: data/ferreteria.db
CARPETA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
RUTA_BD = os.path.join(CARPETA_DATOS, "ferreteria.db")


def conectar():
    """Abre la conexión con la base de datos."""
    # Si la carpeta data no existe, la creo
    os.makedirs(CARPETA_DATOS, exist_ok=True)

    conn = sqlite3.connect(RUTA_BD)
    # Con esto puedo leer los campos por su nombre y no por su posición
    conn.row_factory = sqlite3.Row
    return conn


def crear_tablas():
    """Crea las tablas si todavía no existen."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            stock INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula TEXT NOT NULL,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            correo TEXT,
            ciudad TEXT NOT NULL,
            tipo TEXT NOT NULL,
            activo INTEGER NOT NULL DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ruc TEXT NOT NULL,
            empresa TEXT NOT NULL,
            producto TEXT NOT NULL,
            contacto TEXT NOT NULL,
            telefono TEXT NOT NULL,
            correo TEXT,
            convenio INTEGER NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL,
            fecha TEXT NOT NULL,
            cliente TEXT NOT NULL,
            total REAL NOT NULL,
            estado TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def cargar_datos_iniciales():
    """Carga registros de ejemplo solo la primera vez que se crea la base."""
    conn = conectar()
    cursor = conn.cursor()

    # Solo inserto los ejemplos si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        productos = [
            ("P001", "Cemento Selvalegre 50 kg", "Cemento", 120, 8.50),
            ("P002", "Bloque de 15 cm", "Bloques", 850, 0.65),
            ("P003", "Varilla de hierro 12 mm", "Hierro", 240, 12.30),
            ("P004", "Malla Armex R-84", "Hierro", 45, 28.90),
            ("P005", "Tubería Plastigama 110 mm", "Tuberías", 0, 18.75),
            ("P006", "Bondex Intaco 25 kg", "Acabados", 75, 9.40),
            ("P007", "Metro cúbico de ripio", "Áridos", 30, 22.00),
            ("P008", "Polvo azul (saco)", "Áridos", 0, 6.80),
        ]
        cursor.executemany(
            "INSERT INTO productos (codigo, nombre, categoria, stock, precio) VALUES (?, ?, ?, ?, ?)",
            productos
        )

    cursor.execute("SELECT COUNT(*) FROM clientes")
    if cursor.fetchone()[0] == 0:
        clientes = [
            ("1719283746", "Rosa Simbaña", "0991234567", "", "Quito", "Frecuente", 1),
            ("1712345678", "Luis Guamán", "0987654321", "", "Calderón", "Mayorista", 1),
            ("1798765432", "Constructora Andina S.A.", "022345678", "", "Quito", "Empresa", 1),
            ("1701122334", "Marco Tipán", "0962959355", "", "Carapungo", "Ocasional", 0),
        ]
        cursor.executemany(
            "INSERT INTO clientes (cedula, nombre, telefono, correo, ciudad, tipo, activo) VALUES (?, ?, ?, ?, ?, ?, ?)",
            clientes
        )

    cursor.execute("SELECT COUNT(*) FROM proveedores")
    if cursor.fetchone()[0] == 0:
        proveedores = [
            ("1790012345001", "Holcim Ecuador", "Cemento", "Ing. Pedro Salas", "023456789", "", 1),
            ("1790067890001", "Adelca", "Hierro y varillas", "Sra. Ana Lema", "023987654", "", 1),
            ("1790054321001", "Plastigama", "Tuberías y accesorios", "Ing. Jorge Vaca", "024567890", "", 0),
            ("1790098765001", "Intaco Ecuador", "Bondex y acabados", "Sr. Diego Cruz", "025678901", "", 1),
        ]
        cursor.executemany(
            "INSERT INTO proveedores (ruc, empresa, producto, contacto, telefono, correo, convenio) VALUES (?, ?, ?, ?, ?, ?, ?)",
            proveedores
        )

    cursor.execute("SELECT COUNT(*) FROM facturas")
    if cursor.fetchone()[0] == 0:
        facturas = [
            ("001-001-000125", "2026-08-02", "Rosa Simbaña", 245.80, "Pagada"),
            ("001-001-000126", "2026-08-05", "Luis Guamán", 480.00, "Pendiente"),
            ("001-001-000127", "2026-08-08", "Constructora Andina S.A.", 1320.50, "Pagada"),
            ("001-001-000128", "2026-08-12", "Marco Tipán", 96.25, "Pendiente"),
        ]
        cursor.executemany(
            "INSERT INTO facturas (numero, fecha, cliente, total, estado) VALUES (?, ?, ?, ?, ?)",
            facturas
        )

    conn.commit()
    conn.close()


# ----------------------------------------------------------
# Consultas del módulo de productos
# ----------------------------------------------------------

def listar_productos():
    """Devuelve todos los productos guardados."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos ORDER BY codigo")
    filas = cursor.fetchall()
    conn.close()
    # Convierto cada fila en un diccionario para usarla fácilmente en las plantillas
    return [dict(fila) for fila in filas]


def obtener_producto(id_producto):
    """Busca un producto por su id."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
    fila = cursor.fetchone()
    conn.close()
    return dict(fila) if fila else None


def existe_codigo(codigo, id_excluir=None):
    """Comprueba si un código ya está registrado, para no repetirlo."""
    conn = conectar()
    cursor = conn.cursor()
    if id_excluir is None:
        cursor.execute("SELECT COUNT(*) FROM productos WHERE codigo = ?", (codigo,))
    else:
        cursor.execute("SELECT COUNT(*) FROM productos WHERE codigo = ? AND id != ?", (codigo, id_excluir))
    resultado = cursor.fetchone()[0] > 0
    conn.close()
    return resultado


def agregar_producto(codigo, nombre, categoria, stock, precio):
    """Guarda un producto nuevo en la base de datos."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (codigo, nombre, categoria, stock, precio) VALUES (?, ?, ?, ?, ?)",
        (codigo, nombre, categoria, stock, precio)
    )
    conn.commit()
    conn.close()


def actualizar_producto(id_producto, codigo, nombre, categoria, stock, precio):
    """Modifica los datos de un producto existente."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE productos SET codigo = ?, nombre = ?, categoria = ?, stock = ?, precio = ? WHERE id = ?",
        (codigo, nombre, categoria, stock, precio, id_producto)
    )
    conn.commit()
    conn.close()


def eliminar_producto(id_producto):
    """Borra un producto de la base de datos."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    conn.commit()
    conn.close()


def contar_agotados():
    """Cuenta cuántos productos están sin stock."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM productos WHERE stock = 0")
    total = cursor.fetchone()[0]
    conn.close()
    return total


# ----------------------------------------------------------
# Consultas del módulo de clientes
# ----------------------------------------------------------

def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes ORDER BY nombre")
    filas = cursor.fetchall()
    conn.close()
    return [dict(fila) for fila in filas]


def agregar_cliente(cedula, nombre, telefono, correo, ciudad, tipo, activo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clientes (cedula, nombre, telefono, correo, ciudad, tipo, activo) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (cedula, nombre, telefono, correo, ciudad, tipo, activo)
    )
    conn.commit()
    conn.close()


# ----------------------------------------------------------
# Consultas del módulo de proveedores
# ----------------------------------------------------------

def listar_proveedores():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM proveedores ORDER BY empresa")
    filas = cursor.fetchall()
    conn.close()
    return [dict(fila) for fila in filas]


def agregar_proveedor(ruc, empresa, producto, contacto, telefono, correo, convenio):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO proveedores (ruc, empresa, producto, contacto, telefono, correo, convenio) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (ruc, empresa, producto, contacto, telefono, correo, convenio)
    )
    conn.commit()
    conn.close()


# ----------------------------------------------------------
# Consultas del módulo de facturación
# ----------------------------------------------------------

def listar_facturas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM facturas ORDER BY fecha DESC")
    filas = cursor.fetchall()
    conn.close()
    return [dict(fila) for fila in filas]


def agregar_factura(numero, fecha, cliente, total, estado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO facturas (numero, fecha, cliente, total, estado) VALUES (?, ?, ?, ?, ?)",
        (numero, fecha, cliente, total, estado)
    )
    conn.commit()
    conn.close()


def totales_facturacion():
    """Calcula el total facturado y el total pendiente de cobro."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COALESCE(SUM(total), 0) FROM facturas")
    facturado = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(total), 0) FROM facturas WHERE estado = ?", ("Pendiente",))
    pendiente = cursor.fetchone()[0]

    conn.close()
    return facturado, pendiente
