from .conexion import abrir_conexion, marcador_sql


class RegistroTiempoDAO:
    @staticmethod
    def insertar(empleado_id, proyecto_id, fecha, horas, descripcion):
        horas = float(horas)
        if not 0 < horas <= 24:
            raise ValueError("Las horas deben ser mayores que 0 y hasta 24.")
        if not descripcion.strip():
            raise ValueError("La descripción es obligatoria.")
        
        conn = abrir_conexion()
        ph = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(f"""
                    INSERT INTO registro_tiempo
                    (empleado_id, proyecto_id, fecha, horas_trabajadas, descripcion_tarea)
                    VALUES ({ph}, {ph}, {ph}, {ph}, {ph})
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
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT r.*, e.nombre AS empleado, p.nombre AS proyecto
                    FROM registro_tiempo r
                    JOIN empleado e ON e.id_empleado=r.empleado_id
                    JOIN proyecto p ON p.id_proyecto=r.proyecto_id
                    ORDER BY r.id_registro
                """)
                return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def buscar_por_id(id_registro):
        conn = abrir_conexion()
        ph = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM registro_tiempo WHERE id_registro={ph}",
                            (id_registro,))
                return cur.fetchone()
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
        ph = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(f"""
                    UPDATE registro_tiempo SET empleado_id={ph}, proyecto_id={ph}, fecha={ph},
                        horas_trabajadas={ph}, descripcion_tarea={ph} WHERE id_registro={ph}
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
        ph = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM registro_tiempo WHERE id_registro={ph}", (id_registro,))
                conn.commit()
                return cur.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()