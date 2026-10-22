from .conexion import abrir_conexion


class RegistroTiempoDAO:
    @staticmethod
    def insertar(empleado_id, proyecto_id, fecha, horas, descripcion):
        horas = float(horas)
        if not 0 < horas <= 24:
            raise ValueError("Las horas deben ser mayores que 0 y hasta 24.")
        if not descripcion.strip():
            raise ValueError("La descripción es obligatoria.")
        conn = abrir_conexion()
        try:
            cur = conn.execute("""
                INSERT INTO registro_tiempo
                (empleado_id, proyecto_id, fecha, horas_trabajadas, descripcion_tarea)
                VALUES (?, ?, ?, ?, ?)
            """, (empleado_id, proyecto_id, fecha.strip(), horas, descripcion.strip()))
            conn.commit()
            return cur.lastrowid
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def listar():
        conn = abrir_conexion()
        try:
            return conn.execute("""
                SELECT r.*, e.nombre AS empleado, p.nombre AS proyecto
                FROM registro_tiempo r
                JOIN empleado e ON e.id_empleado=r.empleado_id
                JOIN proyecto p ON p.id_proyecto=r.proyecto_id
                ORDER BY r.id_registro
            """).fetchall()
        finally:
            conn.close()

    @staticmethod
    def buscar_por_id(id_registro):
        conn = abrir_conexion()
        try:
            return conn.execute("SELECT * FROM registro_tiempo WHERE id_registro=?",
                                (id_registro,)).fetchone()
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_registro, empleado_id, proyecto_id, fecha, horas, descripcion):
        horas = float(horas)
        if not 0 < horas <= 24:
            raise ValueError("Las horas deben ser mayores que 0 y hasta 24.")
        if not descripcion.strip():
            raise ValueError("La descripción es obligatoria.")
        conn = abrir_conexion()
        try:
            cur = conn.execute("""
                UPDATE registro_tiempo SET empleado_id=?, proyecto_id=?, fecha=?,
                    horas_trabajadas=?, descripcion_tarea=? WHERE id_registro=?
            """, (empleado_id, proyecto_id, fecha.strip(), horas,
                  descripcion.strip(), id_registro))
            conn.commit()
            return cur.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_registro):
        conn = abrir_conexion()
        try:
            cur = conn.execute("DELETE FROM registro_tiempo WHERE id_registro=?", (id_registro,))
            conn.commit()
            return cur.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
