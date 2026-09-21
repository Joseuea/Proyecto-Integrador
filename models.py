"""
models.py - Modelo de usuario para el sistema de login.
Flask-Login necesita una clase de usuario con ciertos métodos;
por eso hereda de UserMixin, que ya los incluye.
"""

from flask_login import UserMixin

from conexion import consultar_uno, ejecutar


class Usuario(UserMixin):
    """Representa a un usuario que puede ingresar al sistema."""

    def __init__(self, id, usuario, nombre, password):
        self.id = id
        self.usuario = usuario
        self.nombre = nombre
        self.password = password  # aquí se guarda el hash, nunca la contraseña real


def buscar_por_id(id_usuario):
    """Busca un usuario por su id. Flask-Login la usa para recuperar la sesión."""
    fila = consultar_uno("SELECT * FROM usuarios WHERE id = %s", (id_usuario,))

    if fila is None:
        return None

    return Usuario(fila["id"], fila["usuario"], fila["nombre"], fila["password"])


def buscar_por_usuario(nombre_usuario):
    """Busca un usuario por su nombre de usuario. Se usa al iniciar sesión."""
    fila = consultar_uno("SELECT * FROM usuarios WHERE usuario = %s", (nombre_usuario,))

    if fila is None:
        return None

    return Usuario(fila["id"], fila["usuario"], fila["nombre"], fila["password"])


def existe_usuario(nombre_usuario):
    """Comprueba si un nombre de usuario ya está registrado."""
    resultado = consultar_uno(
        "SELECT COUNT(*) AS total FROM usuarios WHERE usuario = %s",
        (nombre_usuario,)
    )
    return resultado["total"] > 0


def crear_usuario(nombre_usuario, nombre, password_hash):
    """Guarda un usuario nuevo. La contraseña llega ya convertida en hash."""
    sql = "INSERT INTO usuarios (usuario, nombre, password) VALUES (%s, %s, %s)"
    return ejecutar(sql, (nombre_usuario, nombre, password_hash))


def contar_usuarios():
    """Cuenta cuántos usuarios hay registrados."""
    return consultar_uno("SELECT COUNT(*) AS total FROM usuarios")["total"]
