"""
conexion.py - Conexión centralizada con la base de datos MySQL.
Todos los módulos del proyecto usan estas funciones para
conectarse, de modo que los datos de acceso están en un solo lugar.
"""

import os
import mysql.connector
from mysql.connector import Error

# Datos de conexión.
# Se leen de variables de entorno para no dejar la contraseña
# escrita en el código que se sube a GitHub.
CONFIGURACION = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", 3306)),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "jm_ferreteria"),
    # utf8mb4 permite guardar tildes y la letra ñ correctamente
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci"
}


def obtener_conexion():
    """Abre y devuelve una conexión con la base de datos."""
    try:
        conexion = mysql.connector.connect(**CONFIGURACION)
        return conexion
    except Error as error:
        print(f"Error al conectar con MySQL: {error}")
        raise


def consultar(sql, parametros=None):
    """Ejecuta un SELECT y devuelve todos los registros encontrados."""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)  # dictionary=True devuelve diccionarios
    cursor.execute(sql, parametros or ())
    registros = cursor.fetchall()
    cursor.close()
    conexion.close()
    return registros


def consultar_uno(sql, parametros=None):
    """Ejecuta un SELECT y devuelve un solo registro."""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, parametros or ())
    registro = cursor.fetchone()
    cursor.close()
    conexion.close()
    return registro


def ejecutar(sql, parametros=None):
    """Ejecuta INSERT, UPDATE o DELETE y confirma los cambios."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(sql, parametros or ())
    conexion.commit()  # sin commit los cambios no se guardan
    filas_afectadas = cursor.rowcount
    cursor.close()
    conexion.close()
    return filas_afectadas


def probar_conexion():
    """Comprueba que la base de datos responda. Se usa al iniciar la aplicación."""
    try:
        conexion = obtener_conexion()
        if conexion.is_connected():
            conexion.close()
            return True
    except Error:
        return False
    return False
