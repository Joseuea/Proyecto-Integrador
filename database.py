"""
database.py - Consultas SQL de cada módulo del sistema.
Usa las funciones del paquete conexion para hablar con MySQL.
"""

from conexion import consultar, consultar_uno, ejecutar


# ----------------------------------------------------------
# Módulo de productos (listar, agregar, modificar, eliminar)
# ----------------------------------------------------------

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
    sql = "SELECT * FROM productos WHERE id_producto = %s"
    return consultar_uno(sql, (id_producto,))


def existe_codigo(codigo, id_excluir=None):
    """Comprueba con WHERE si un código ya está registrado."""
    if id_excluir is None:
        sql = "SELECT COUNT(*) AS total FROM productos WHERE codigo = %s"
        resultado = consultar_uno(sql, (codigo,))
    else:
        sql = "SELECT COUNT(*) AS total FROM productos WHERE codigo = %s AND id_producto != %s"
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
    sql = "DELETE FROM productos WHERE id_producto = %s"
    return ejecutar(sql, (id_producto,))


def contar_agotados():
    """Cuenta los productos sin stock usando WHERE."""
    sql = "SELECT COUNT(*) AS total FROM productos WHERE stock = 0"
    return consultar_uno(sql)["total"]


# ----------------------------------------------------------
# Módulo de clientes
# ----------------------------------------------------------

def listar_clientes():
    return consultar("SELECT * FROM clientes ORDER BY nombre")


def agregar_cliente(cedula, nombre, telefono, correo, ciudad, tipo, activo):
    sql = """
        INSERT INTO clientes (cedula, nombre, telefono, correo, ciudad, tipo, activo)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    return ejecutar(sql, (cedula, nombre, telefono, correo, ciudad, tipo, activo))


# ----------------------------------------------------------
# Módulo de proveedores
# ----------------------------------------------------------

def listar_proveedores():
    return consultar("SELECT * FROM proveedores ORDER BY empresa")


def agregar_proveedor(ruc, empresa, producto, contacto, telefono, correo, convenio):
    sql = """
        INSERT INTO proveedores (ruc, empresa, producto, contacto, telefono, correo, convenio)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    return ejecutar(sql, (ruc, empresa, producto, contacto, telefono, correo, convenio))


# ----------------------------------------------------------
# Módulo de facturación
# ----------------------------------------------------------

def listar_facturas():
    """SELECT con JOIN para mostrar el nombre del cliente de cada factura."""
    sql = """
        SELECT f.id_factura, f.numero, f.fecha, f.total, f.estado,
               c.nombre AS cliente
        FROM facturas f
        LEFT JOIN clientes c ON f.id_cliente = c.id_cliente
        ORDER BY f.fecha DESC
    """
    return consultar(sql)


def agregar_factura(numero, fecha, id_cliente, total, estado):
    sql = """
        INSERT INTO facturas (numero, fecha, id_cliente, total, estado)
        VALUES (%s, %s, %s, %s, %s)
    """
    return ejecutar(sql, (numero, fecha, id_cliente, total, estado))


def totales_facturacion():
    """Suma el total facturado y el total pendiente de cobro."""
    facturado = consultar_uno("SELECT COALESCE(SUM(total), 0) AS suma FROM facturas")["suma"]
    pendiente = consultar_uno(
        "SELECT COALESCE(SUM(total), 0) AS suma FROM facturas WHERE estado = %s",
        ("Pendiente",)
    )["suma"]
    return float(facturado), float(pendiente)
