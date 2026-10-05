"""
Paquete conexion: centraliza el acceso a la base de datos PostgreSQL.
"""

from conexion.conexion import (
    obtener_conexion,
    consultar,
    consultar_uno,
    ejecutar,
    probar_conexion,
    crear_tablas,
    nombre_motor,
    usando_postgres
)

__all__ = [
    "obtener_conexion", "consultar", "consultar_uno",
    "ejecutar", "probar_conexion", "crear_tablas",
    "nombre_motor", "usando_postgres"
]
