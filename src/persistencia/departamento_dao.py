from .conexion import abrir_conexion, marcador_sql
from dominio.departamento import Departamento


class DepartamentoDAO:
    @staticmethod
    def insertar(nombre: str, gerente_id: int | None = None) -> int:
        conn = abrir_conexion()
        p = marcador_sql()
        try:
            with conn.cursor() as cursor:
                sql = f"INSERT INTO departamento (nombre, gerente_id) VALUES ({p}, {p})"
                cursor.execute(sql, (nombre.strip(), gerente_id))
                id_generado = cursor.lastrowid
            conn.commit()
            return id_generado
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def listar() -> list[dict]:
        conn = abrir_conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_depto, nombre, gerente_id FROM departamento")
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def asignar_gerente(id_depto: int, gerente_id: int | None) -> bool:
        conn = abrir_conexion()
        p = marcador_sql()
        try:
            with conn.cursor() as cursor:
                sql = f"UPDATE departamento SET gerente_id = {p} WHERE id_depto = {p}"
                cursor.execute(sql, (gerente_id, id_depto))
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()