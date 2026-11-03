from .conexion import abrir_conexion, marcador_sql


class DepartamentoDAO:

    @staticmethod
    def insertar(nombre):
        """Inserta un nuevo departamento y devuelve su ID generado."""
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre es obligatorio.")
        
        conn = abrir_conexion()
        placeholder = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"INSERT INTO departamento (nombre) VALUES ({placeholder})",
                    (nombre,)
                )
                conn.commit()
                return cur.lastrowid
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def listar():
        """Devuelve la lista de departamentos con su conteo de empleados."""
        conn = abrir_conexion()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT d.id_depto, d.nombre, COUNT(e.id_empleado) AS empleados
                    FROM departamento d 
                    LEFT JOIN empleado e ON e.departamento_id = d.id_depto
                    GROUP BY d.id_depto 
                    ORDER BY d.id_depto
                """)
                return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def buscar_por_id(id_depto):
        """Busca un departamento por su ID."""
        conn = abrir_conexion()
        placeholder = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT * FROM departamento WHERE id_depto = {placeholder}",
                    (id_depto,)
                )
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_depto, nombre):
        """Actualiza el nombre de un departamento."""
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre es obligatorio.")
        
        conn = abrir_conexion()
        placeholder = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"UPDATE departamento SET nombre = {placeholder} WHERE id_depto = {placeholder}",
                    (nombre, id_depto)
                )
                conn.commit()
                return cur.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_depto):
        """Elimina un departamento por su ID."""
        conn = abrir_conexion()
        placeholder = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"DELETE FROM departamento WHERE id_depto = {placeholder}",
                    (id_depto,)
                )
                conn.commit()
                return cur.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()