"""
conexion.py - Conexión centralizada con la base de datos PostgreSQL.
Todos los módulos del proyecto usan estas funciones para conectarse,
de modo que los datos de acceso están en un solo lugar.

En Render la base entrega una sola dirección (DATABASE_URL);
en local se usan las variables DB_HOST, DB_USER, etc.
"""

import os

import psycopg2
import psycopg2.extras
from psycopg2 import Error

# Render publica la dirección completa de la base en esta variable
DATABASE_URL = os.environ.get("DATABASE_URL")

# Datos de conexión para trabajar en la computadora
CONFIGURACION = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", 5432)),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "dbname": os.environ.get("DB_NAME", "jm_ferreteria")
}


def obtener_conexion():
    """Abre y devuelve una conexión con la base de datos."""
    try:
        if DATABASE_URL:
            # En Render la conexión debe ir cifrada con SSL
            return psycopg2.connect(DATABASE_URL, sslmode="require")
        return psycopg2.connect(**CONFIGURACION)
    except Error as error:
        print(f"Error al conectar con PostgreSQL: {error}")
        raise


def consultar(sql, parametros=None):
    """Ejecuta un SELECT y devuelve todos los registros encontrados."""
    conexion = obtener_conexion()
    # RealDictCursor devuelve cada fila como un diccionario
    cursor = conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(sql, parametros or ())
    registros = cursor.fetchall()
    cursor.close()
    conexion.close()
    return [dict(fila) for fila in registros]


def consultar_uno(sql, parametros=None):
    """Ejecuta un SELECT y devuelve un solo registro."""
    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(sql, parametros or ())
    registro = cursor.fetchone()
    cursor.close()
    conexion.close()
    return dict(registro) if registro else None


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
        conexion.close()
        return True
    except Error:
        return False


def crear_tablas():
    """
    Ejecuta sql/esquema.sql al iniciar la aplicación.
    Así la base queda lista en Render sin tener que crear las tablas a mano.
    """
    ruta = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sql", "esquema.sql")

    if not os.path.exists(ruta):
        print("No se encontró el archivo sql/esquema.sql")
        return False

    with open(ruta, "r", encoding="utf-8") as archivo:
        instrucciones = archivo.read()

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(instrucciones)
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Error as error:
        print(f"Error al preparar las tablas: {error}")
        return False
