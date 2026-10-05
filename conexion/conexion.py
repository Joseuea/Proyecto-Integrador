"""
conexion.py - Conexión centralizada con la base de datos.

El proyecto puede trabajar con dos motores:

  * PostgreSQL : se usa cuando hay una dirección DATABASE_URL (Render)
                 o cuando DB_ENGINE vale "postgres".
  * SQLite     : es el modo por defecto. No necesita instalar ningún
                 servidor porque viene incluido con Python, y guarda
                 todo en el archivo data/ferreteria.db

El resto del proyecto no cambia: siempre llama a consultar(), ejecutar(),
etc., y este archivo se encarga de hablar con el motor que corresponda.
"""

import os
import sqlite3

# La dirección que entrega Render al crear una base PostgreSQL
DATABASE_URL = os.environ.get("DATABASE_URL")

# Motor elegido: "postgres" o "sqlite"
MOTOR = os.environ.get("DB_ENGINE", "postgres" if DATABASE_URL else "sqlite").lower()

# Datos de conexión de PostgreSQL para trabajar en la computadora
CONFIGURACION = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", 5432)),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "dbname": os.environ.get("DB_NAME", "jm_ferreteria")
}

# Carpeta y archivo donde SQLite guarda la base
CARPETA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_DATOS = os.path.join(CARPETA_PROYECTO, "data")
RUTA_SQLITE = os.environ.get("SQLITE_PATH", os.path.join(CARPETA_DATOS, "ferreteria.db"))


def usando_postgres():
    """Indica si la aplicación está trabajando con PostgreSQL."""
    return MOTOR == "postgres"


def obtener_conexion():
    """Abre y devuelve una conexión con la base de datos."""
    if usando_postgres():
        import psycopg2
        if DATABASE_URL:
            # En Render la conexión debe ir cifrada con SSL
            return psycopg2.connect(DATABASE_URL, sslmode="require")
        return psycopg2.connect(**CONFIGURACION)

    # Modo SQLite: si la carpeta data no existe, la creo
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    conexion = sqlite3.connect(RUTA_SQLITE)
    # Con esto puedo leer los campos por su nombre y no por su posición
    conexion.row_factory = sqlite3.Row
    # SQLite no respeta las claves foráneas si no se activan
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def _adaptar(sql):
    """
    Las consultas del proyecto están escritas con %s.
    SQLite usa ? como marcador, así que lo cambio solo en ese caso.
    """
    return sql if usando_postgres() else sql.replace("%s", "?")


def _cursor_diccionario(conexion):
    """Devuelve un cursor que entrega las filas como diccionarios."""
    if usando_postgres():
        import psycopg2.extras
        return conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return conexion.cursor()


def consultar(sql, parametros=None):
    """Ejecuta un SELECT y devuelve todos los registros encontrados."""
    conexion = obtener_conexion()
    cursor = _cursor_diccionario(conexion)
    cursor.execute(_adaptar(sql), parametros or ())
    registros = cursor.fetchall()
    cursor.close()
    conexion.close()
    return [dict(fila) for fila in registros]


def consultar_uno(sql, parametros=None):
    """Ejecuta un SELECT y devuelve un solo registro."""
    conexion = obtener_conexion()
    cursor = _cursor_diccionario(conexion)
    cursor.execute(_adaptar(sql), parametros or ())
    registro = cursor.fetchone()
    cursor.close()
    conexion.close()
    return dict(registro) if registro else None


def ejecutar(sql, parametros=None):
    """Ejecuta INSERT, UPDATE o DELETE y confirma los cambios."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(_adaptar(sql), parametros or ())
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
    except Exception as error:
        print(f"Error al conectar con la base de datos: {error}")
        return False


def crear_tablas():
    """
    Ejecuta el archivo de esquema que corresponde al motor en uso,
    para que las tablas queden listas sin tener que crearlas a mano.
    """
    archivo = "esquema.sql" if usando_postgres() else "esquema_sqlite.sql"
    ruta = os.path.join(CARPETA_PROYECTO, "sql", archivo)

    if not os.path.exists(ruta):
        print(f"No se encontró el archivo sql/{archivo}")
        return False

    with open(ruta, "r", encoding="utf-8") as f:
        instrucciones = f.read()

    try:
        conexion = obtener_conexion()
        if usando_postgres():
            cursor = conexion.cursor()
            cursor.execute(instrucciones)
            cursor.close()
        else:
            # executescript permite ejecutar varias instrucciones seguidas
            conexion.executescript(instrucciones)
        conexion.commit()
        conexion.close()
        return True
    except Exception as error:
        print(f"Error al preparar las tablas: {error}")
        return False


def nombre_motor():
    """Devuelve el nombre del motor en uso, para mostrarlo al iniciar."""
    return "PostgreSQL" if usando_postgres() else "SQLite"
