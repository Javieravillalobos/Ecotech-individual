# persistencia/conexion.py
import os
import sqlite3
import pymysql
from dotenv import load_dotenv

load_dotenv()

def obtener_motor():
    return os.getenv("DB_ENGINE", "sqlite").lower()

def motor_actual():
    return os.getenv("DB_ENGINE", "sqlite").lower()

def abrir_conexion():
    motor = obtener_motor()
    if motor == "sqlite":
        conn = sqlite3.connect(os.getenv("DB_NAME", "ecotech.db"))
        # Esto hace que SQLite devuelva las filas como diccionarios (igual que PyMySQL)
        conn.row_factory = sqlite3.Row
        return conn
    if motor == "mysql":
        return pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

    raise ValueError(f"Motor no soportado: {motor}")


def marcador_sql():
    if obtener_motor() == "sqlite":
        return "?"
    return "%s"