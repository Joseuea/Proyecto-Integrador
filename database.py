"""
database.py - Consultas SQL de cada módulo del sistema.
Usa las funciones del paquete conexion para hablar con PostgreSQL.

Cada módulo tiene las cuatro operaciones básicas:
listar (SELECT), agregar (INSERT), actualizar (UPDATE) y eliminar (DELETE).
Todas las consultas usan parámetros %s en lugar de unir texto,
para evitar problemas de seguridad.
"""

from conexion import consultar, consultar_uno, ejecutar


# ==========================================================
# MÓDULO DE PRODUCTOS
# ==========================================================

def listar_productos():
    """SELECT con JOIN para mostrar también el proveedor de cada producto."""
    sql = """
        SELECT p.id_producto, p.codigo, p.nombre, p.categoria,
               p.stock, p.precio, p.id_proveedor,
               pr.empresa AS proveedor
        FROM productos p
        LEFT JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
        ORDER BY p.codigo
    """
    return consultar(sql)


def obtener_producto(id_producto):
    """SELECT de un solo producto usando WHERE."""
    return consultar_uno("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))


def existe_codigo(codigo, id_excluir=None):
    """Comprueba si un código ya está registrado, para no repetirlo."""
    if id_excluir is None:
        sql = "SELECT COUNT(*) AS total FROM productos WHERE codigo = %s"
        resultado = consultar_uno(sql, (codigo,))
    else:
        sql = "SELECT COUNT(*) AS total FROM productos WHERE codigo = %s AND id_producto <> %s"
        resultado = consultar_uno(sql, (codigo, id_excluir))
    return resultado["total"] > 0


def agregar_producto(codigo, nombre, categoria, stock, precio, id_proveedor):
    """INSERT de un producto nuevo."""
    sql = """
        INSERT INTO productos (codigo, nombre, categoria, stock, precio, id_proveedor)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    return ejecutar(sql, (codigo, nombre, categoria, stock, precio, id_proveedor))


def actualizar_producto(id_producto, codigo, nombre, categoria, stock, precio, id_proveedor):
    """UPDATE del producto seleccionado. El WHERE evita modificar los demás."""
    sql = """
        UPDATE productos
        SET codigo = %s, nombre = %s, categoria = %s,
            stock = %s, precio = %s, id_proveedor = %s
        WHERE id_producto = %s
    """
    return ejecutar(sql, (codigo, nombre, categoria, stock, precio, id_proveedor, id_producto))


def eliminar_producto(id_producto):
    """DELETE del producto seleccionado. El WHERE evita borrar toda la tabla."""
    return ejecutar("DELETE FROM productos WHERE id_producto = %s", (id_producto,))


def contar_agotados():
    """Cuenta los productos sin stock usando WHERE."""
    return consultar_uno("SELECT COUNT(*) AS total FROM productos WHERE stock = 0")["total"]


# ==========================================================
# MÓDULO DE CLIENTES
# ==========================================================

def listar_clientes():
    """SELECT de los clientes, con el número de facturas de cada uno."""
    sql = """
        SELECT c.id_cliente, c.cedula, c.nombre, c.telefono,
               c.correo, c.ciudad, c.tipo, c.activo,
               COUNT(f.id_factura) AS total_facturas
        FROM clientes c
        LEFT JOIN facturas f ON c.id_cliente = f.id_cliente
        GROUP BY c.id_cliente, c.cedula, c.nombre, c.telefono,
                 c.correo, c.ciudad, c.tipo, c.activo
        ORDER BY c.nombre
    """
    return consultar(sql)


def obtener_cliente(id_cliente):
    return consultar_uno("SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))


def agregar_cliente(cedula, nombre, telefono, correo, ciudad, tipo, activo):
    sql = """
        INSERT INTO clientes (cedula, nombre, telefono, correo, ciudad, tipo, activo)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    return ejecutar(sql, (cedula, nombre, telefono, correo, ciudad, tipo, activo))


def actualizar_cliente(id_cliente, cedula, nombre, telefono, correo, ciudad, tipo, activo):
    sql = """
        UPDATE clientes
        SET cedula = %s, nombre = %s, telefono = %s, correo = %s,
            ciudad = %s, tipo = %s, activo = %s
        WHERE id_cliente = %s
    """
    return ejecutar(sql, (cedula, nombre, telefono, correo, ciudad, tipo, activo, id_cliente))


def eliminar_cliente(id_cliente):
    return ejecutar("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))


# ==========================================================
# MÓDULO DE PROVEEDORES
# ==========================================================

def listar_proveedores():
    """SELECT de los proveedores, con la cantidad de productos que provee cada uno."""
    sql = """
        SELECT pr.id_proveedor, pr.ruc, pr.empresa, pr.producto,
               pr.contacto, pr.telefono, pr.correo, pr.convenio,
               COUNT(p.id_producto) AS total_productos
        FROM proveedores pr
        LEFT JOIN productos p ON pr.id_proveedor = p.id_proveedor
        GROUP BY pr.id_proveedor, pr.ruc, pr.empresa, pr.producto,
                 pr.contacto, pr.telefono, pr.correo, pr.convenio
        ORDER BY pr.empresa
    """
    return consultar(sql)


def obtener_proveedor(id_proveedor):
    return consultar_uno("SELECT * FROM proveedores WHERE id_proveedor = %s", (id_proveedor,))


def agregar_proveedor(ruc, empresa, producto, contacto, telefono, correo, convenio):
    sql = """
        INSERT INTO proveedores (ruc, empresa, producto, contacto, telefono, correo, convenio)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    return ejecutar(sql, (ruc, empresa, producto, contacto, telefono, correo, convenio))


def actualizar_proveedor(id_proveedor, ruc, empresa, producto, contacto, telefono, correo, convenio):
    sql = """
        UPDATE proveedores
        SET ruc = %s, empresa = %s, producto = %s, contacto = %s,
            telefono = %s, correo = %s, convenio = %s
        WHERE id_proveedor = %s
    """
    return ejecutar(sql, (ruc, empresa, producto, contacto, telefono, correo, convenio, id_proveedor))


def eliminar_proveedor(id_proveedor):
    """Al borrar un proveedor, sus productos quedan sin proveedor asignado."""
    return ejecutar("DELETE FROM proveedores WHERE id_proveedor = %s", (id_proveedor,))


# ==========================================================
# MÓDULO DE FACTURACIÓN
# ==========================================================

def listar_facturas():
    """SELECT con JOIN para mostrar el nombre y la ciudad del cliente de cada factura."""
    sql = """
        SELECT f.id_factura, f.numero, f.fecha, f.total, f.estado, f.id_cliente,
               c.nombre AS cliente, c.ciudad AS ciudad_cliente
        FROM facturas f
        LEFT JOIN clientes c ON f.id_cliente = c.id_cliente
        ORDER BY f.fecha DESC
    """
    return consultar(sql)


def obtener_factura(id_factura):
    return consultar_uno("SELECT * FROM facturas WHERE id_factura = %s", (id_factura,))


def agregar_factura(numero, fecha, id_cliente, total, estado):
    sql = """
        INSERT INTO facturas (numero, fecha, id_cliente, total, estado)
        VALUES (%s, %s, %s, %s, %s)
    """
    return ejecutar(sql, (numero, fecha, id_cliente, total, estado))


def actualizar_factura(id_factura, numero, fecha, id_cliente, total, estado):
    sql = """
        UPDATE facturas
        SET numero = %s, fecha = %s, id_cliente = %s, total = %s, estado = %s
        WHERE id_factura = %s
    """
    return ejecutar(sql, (numero, fecha, id_cliente, total, estado, id_factura))


def eliminar_factura(id_factura):
    return ejecutar("DELETE FROM facturas WHERE id_factura = %s", (id_factura,))


def totales_facturacion():
    """Suma el total facturado y el total pendiente de cobro."""
    facturado = consultar_uno("SELECT COALESCE(SUM(total), 0) AS suma FROM facturas")["suma"]
    pendiente = consultar_uno(
        "SELECT COALESCE(SUM(total), 0) AS suma FROM facturas WHERE estado = %s",
        ("Pendiente",)
    )["suma"]
    return float(facturado), float(pendiente)
