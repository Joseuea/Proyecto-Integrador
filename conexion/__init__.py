"""
Paquete conexion: centraliza el acceso a la base de datos MySQL.
"""

from conexion.conexion import (
    obtener_conexion,
    consultar,
    consultar_uno,
    ejecutar,
    probar_conexion
)

__all__ = ["obtener_conexion", "consultar", "consultar_uno", "ejecutar", "probar_conexion"]
