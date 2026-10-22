from .conexion import abrir_conexion


class DepartamentoDAO:
    @staticmethod
    def insertar(nombre):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre es obligatorio.")
        conn = abrir_conexion()
        try:
            cur = conn.execute("INSERT INTO departamento(nombre) VALUES (?)", (nombre,))
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
                SELECT d.id_depto, d.nombre, COUNT(e.id_empleado) AS empleados
                FROM departamento d LEFT JOIN empleado e ON e.departamento_id=d.id_depto
                GROUP BY d.id_depto ORDER BY d.id_depto
            """).fetchall()
        finally:
            conn.close()

    @staticmethod
    def buscar_por_id(id_depto):
        conn = abrir_conexion()
        try:
            return conn.execute("SELECT * FROM departamento WHERE id_depto=?", (id_depto,)).fetchone()
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_depto, nombre):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre es obligatorio.")
        conn = abrir_conexion()
        try:
            cur = conn.execute("UPDATE departamento SET nombre=? WHERE id_depto=?",
                               (nombre, id_depto))
            conn.commit()
            return cur.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_depto):
        conn = abrir_conexion()
        try:
            cur = conn.execute("DELETE FROM departamento WHERE id_depto=?", (id_depto,))
            conn.commit()
            return cur.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
