from contextlib import closing
"""DAO para la entidad Departamento.

Soporta MySQL y SQLite utilizando los marcadores de consulta dinámicos.
"""
from .conexion import abrir_conexion, marcador_sql


class DepartamentoDAO:
    @staticmethod
    def insertar(nombre: str, gerente_id: int | None = None) -> int:
        """Inserta un nuevo departamento y retorna su ID generado."""
        conn = abrir_conexion()
        p = marcador_sql()
        try:
            with closing(conn.cursor()) as cursor:
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
        """Retorna todos los departamentos usando alias para compatibilidad."""
        conn = abrir_conexion()
        try:
            with closing(conn.cursor()) as cursor:
                sql = "SELECT id_departamento AS id_depto, nombre, presupuesto, gerente_id, (SELECT COUNT(*) FROM empleado WHERE departamento_id = departamento.id_departamento) AS empleados FROM departamento"
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(id_depto: int) -> dict | None:
        """Obtiene un departamento según su id."""
        conn = abrir_conexion()
        p = marcador_sql()
        try:
            with closing(conn.cursor()) as cursor:
                sql = f"SELECT id_departamento AS id_depto, nombre, presupuesto, gerente_id FROM departamento WHERE id_departamento = {p}"
                cursor.execute(sql, (id_depto,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def asignar_gerente(id_depto: int, gerente_id: int | None) -> bool:
        """Asigna o remueve el gerente de un departamento."""
        conn = abrir_conexion()
        p = marcador_sql()
        try:
            with closing(conn.cursor()) as cursor:
                sql = f"UPDATE departamento SET gerente_id = {p} WHERE id_departamento = {p}"
                cursor.execute(sql, (gerente_id, id_depto))
                filas_afectadas = cursor.rowcount
            conn.commit()
            return filas_afectadas > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_depto: int, nombre: str, presupuesto: float | None = None, gerente_id: int | None = None) -> bool:
        """Actualiza los datos básicos de un departamento."""
        conn = abrir_conexion()
        p = marcador_sql()
        try:
            with closing(conn.cursor()) as cursor:
                sql = f"UPDATE departamento SET nombre = {p}, presupuesto = {p}, gerente_id = {p} WHERE id_departamento = {p}"
                cursor.execute(sql, (nombre.strip(), presupuesto, gerente_id, id_depto))
                filas_afectadas = cursor.rowcount
            conn.commit()
            return filas_afectadas > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_depto: int) -> bool:
        """Elimina un departamento por su id."""
        conn = abrir_conexion()
        p = marcador_sql()
        try:
            with closing(conn.cursor()) as cursor:
                sql = f"WHERE id_departamento = {p}"
                cursor.execute(f"DELETE FROM departamento {sql}", (id_depto,))
                filas_afectadas = cursor.rowcount
            conn.commit()
            return filas_afectadas > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()