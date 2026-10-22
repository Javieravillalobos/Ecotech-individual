"""Conexión configurable a SQLite o MariaDB/MySQL."""
import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _cargar_env():
    """Carga las variables del archivo .env."""
    env_path = ROOT / ".env"

    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()

            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(
                    key.strip(),
                    value.strip().strip('"').strip("'")
                )


_cargar_env()


def motor_actual():
    return os.getenv("DB_ENGINE", "sqlite").strip().lower()


class CursorMySQL:
    """Adapta el cursor de MySQL al estilo utilizado por los DAO."""

    def __init__(self, cursor):
        self._cursor = cursor

    def execute(self, sql, parametros=()):
        self._cursor.execute(ConexionMySQL._sql(sql), parametros)
        return self

    def __getattr__(self, nombre):
        return getattr(self._cursor, nombre)


class ConexionMySQL:
    """Conexión compatible con consultas escritas para SQLite."""

    def __init__(self, conexion):
        self._conexion = conexion

    @staticmethod
    def _sql(sql):
        # Convierte los parámetros '?' a '%s' para mysql.connector.
        return sql.replace("?", "%s")

    def execute(self, sql, parametros=()):
        cursor = self._conexion.cursor(dictionary=True)
        cursor.execute(self._sql(sql), parametros)
        return cursor

    def cursor(self):
        return CursorMySQL(
            self._conexion.cursor(dictionary=True)
        )

    def executescript(self, script):
        cursor = self._conexion.cursor()

        try:
            for sentencia in script.split(";"):
                sentencia = sentencia.strip()

                if sentencia:
                    cursor.execute(sentencia)
        finally:
            cursor.close()

    def commit(self):
        self._conexion.commit()

    def rollback(self):
        self._conexion.rollback()

    def close(self):
        self._conexion.close()


def abrir_conexion():
    """Abre una conexión SQLite o MariaDB/MySQL según el archivo .env."""
    motor = motor_actual()

    # ---------------- SQLITE ----------------
    if motor == "sqlite":
        db_name = os.getenv("DB_NAME", "ecotech.db")
        path = (ROOT / db_name).resolve()

        if ROOT.resolve() not in path.parents and path != ROOT.resolve():
            raise ValueError(
                "La ruta de la base de datos no es válida."
            )

        conn = sqlite3.connect(path, timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")

        return conn

    # ------------- MARIADB / MYSQL -------------
    if motor in ("mysql", "mariadb"):
        try:
            import mysql.connector
        except ImportError as exc:
            raise RuntimeError(
                "Falta el conector de MySQL/MariaDB. "
                "Instálalo con: py -m pip install mysql-connector-python"
            ) from exc

        # La contraseña puede estar vacía, pero la variable debe existir.
        requeridas = ("DB_HOST", "DB_NAME", "DB_USER")
        faltantes = [
            nombre
            for nombre in requeridas
            if not os.getenv(nombre, "").strip()
        ]

        if os.getenv("DB_PASSWORD") is None:
            faltantes.append("DB_PASSWORD")

        if faltantes:
            raise ValueError(
                "Faltan variables en .env: "
                + ", ".join(faltantes)
            )

        try:
            conexion = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=int(os.getenv("DB_PORT", "3306")),
                database=os.getenv("DB_NAME", "ecotech"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", ""),
                connection_timeout=10,
                charset="utf8mb4",
                use_unicode=True,
            )

            return ConexionMySQL(conexion)

        except mysql.connector.Error as exc:
            raise RuntimeError(
                "No se pudo conectar a MariaDB/MySQL. "
                "Comprueba que WampServer esté iniciado, "
                "que el puerto sea correcto, que la base de datos "
                "exista y que el usuario y la contraseña sean válidos. "
                f"Detalle: {exc}"
            ) from exc

    raise ValueError(
        "DB_ENGINE debe ser 'sqlite', 'mysql' o 'mariadb'.")