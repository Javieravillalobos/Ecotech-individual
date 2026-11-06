"""
DAO para la entidad Proyecto y sus relaciones."""
from contextlib import closing

from .conexion import abrir_conexion, marcador_sql


class ProyectoDAO:
    @staticmethod
    def insertar(nombre: str, descripcion: str, fecha_inicio: str, fecha_fin: str | None = None) -> int:
        """Inserta un proyecto y retorna su ID."""
        conn = abrir_conexion()
        p = marcador_sql()
        try:
            with closing(conn.cursor()) as cursor:
                sql = f"""
                    INSERT INTO proyecto (nombre, descripcion, fecha_inicio, fecha_fin)
                    VALUES ({p}, {p}, {p}, {p})
                """
                cursor.execute(sql, (nombre.strip(), descripcion, fecha_inicio, fecha_fin))
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
        """Lista todos los proyectos."""
        conn = abrir_conexion()
        try:
            with closing(conn.cursor()) as cursor:
                cursor.execute("SELECT id_proyecto, nombre, descripcion, fecha_inicio, fecha_fin FROM proyecto")
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(id_proyecto: int) -> dict | None:
        """Obtiene un proyecto por su ID."""
        conn = abrir_conexion()
        p = marcador_sql()
        try:
            with closing(conn.cursor()) as cursor:
                sql = f"SELECT id_proyecto, nombre, descripcion, fecha_inicio, fecha_fin FROM proyecto WHERE id_proyecto = {p}"
                cursor.execute(sql, (id_proyecto,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def asignar_empleado(proyecto_id: int, empleado_id: int) -> bool:
        """Asigna un empleado a un proyecto en la tabla de relación."""
        conn = abrir_conexion()
        p = marcador_sql()
        try:
            with closing(conn.cursor()) as cursor:
                sql = f"INSERT INTO proyecto_empleado (proyecto_id, empleado_id) VALUES ({p}, {p})"
                cursor.execute(sql, (proyecto_id, empleado_id))
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_proyecto: int, nombre: str, descripcion: str, fecha_inicio: str, fecha_fin: str | None = None) -> bool:
        conn = abrir_conexion()
        p = marcador_sql()
        try:
            with closing(conn.cursor()) as cursor:
                cursor.execute(f"UPDATE proyecto SET nombre={p}, descripcion={p}, fecha_inicio={p}, fecha_fin={p} WHERE id_proyecto={p}", (nombre, descripcion, fecha_inicio, fecha_fin, id_proyecto))
                cambiado = cursor.rowcount > 0
            conn.commit()
            return cambiado
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_proyecto: int) -> bool:
        conn = abrir_conexion()
        p = marcador_sql()
        try:
            with closing(conn.cursor()) as cursor:
                cursor.execute(f"DELETE FROM proyecto WHERE id_proyecto={p}", (id_proyecto,))
                cambiado = cursor.rowcount > 0
            conn.commit()
            return cambiado
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
