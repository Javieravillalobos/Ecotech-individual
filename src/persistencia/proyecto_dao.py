from .conexion import abrir_conexion, marcador_sql


class ProyectoDAO:
    @staticmethod
    def insertar(nombre, descripcion="", fecha_inicio="", fecha_fin=""):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre es obligatorio.")
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise ValueError("La fecha final no puede ser anterior a la inicial.")
        
        conn = abrir_conexion()
        ph = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(f"""
                    INSERT INTO proyecto(nombre, descripcion, fecha_inicio, fecha_fin)
                    VALUES ({ph}, {ph}, {ph}, {ph})
                """, (nombre, descripcion.strip(), fecha_inicio.strip(), fecha_fin.strip()))
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
                cur.execute("SELECT * FROM proyecto ORDER BY id_proyecto")
                return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def buscar_por_id(id_proyecto):
        conn = abrir_conexion()
        ph = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM proyecto WHERE id_proyecto={ph}", (id_proyecto,))
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_proyecto, nombre, descripcion, fecha_inicio, fecha_fin):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre es obligatorio.")
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise ValueError("La fecha final no puede ser anterior a la inicial.")
        
        conn = abrir_conexion()
        ph = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(f"""
                    UPDATE proyecto SET nombre={ph}, descripcion={ph}, fecha_inicio={ph}, fecha_fin={ph}
                    WHERE id_proyecto={ph}
                """, (nombre, descripcion.strip(), fecha_inicio.strip(), fecha_fin.strip(), id_proyecto))
                conn.commit()
                return cur.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_proyecto):
        conn = abrir_conexion()
        ph = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM proyecto WHERE id_proyecto={ph}", (id_proyecto,))
                conn.commit()
                return cur.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def asignar_empleado(id_proyecto, id_empleado):
        conn = abrir_conexion()
        ph = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(f"INSERT INTO proyecto_empleado(proyecto_id, empleado_id) VALUES ({ph}, {ph})",
                             (id_proyecto, id_empleado))
                conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()