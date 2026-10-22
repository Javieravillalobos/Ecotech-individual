from datetime import date
from .conexion import abrir_conexion
from dominio.empleado import Empleado


class EmpleadoDAO:
    @staticmethod
    def insertar(e):
        conn = abrir_conexion()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO usuario(username, password_hash) VALUES (?, ?)",
                (e.username, e._hash_para_persistencia())
            )
            uid = cur.lastrowid
            cur.execute("""
                INSERT INTO empleado(usuario_id, departamento_id, nombre, correo,
                    direccion, telefono, fecha_contrato, salario, rol)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (uid, e.departamento_id, e.nombre, e.correo, e.direccion,
                  e.telefono, e.fecha_contrato, e.salario, e.rol))
            e.id_empleado = cur.lastrowid
            conn.commit()
            return e
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def _desde_fila(row):
        obj = Empleado.__new__(Empleado)
        obj.username = row["username"]
        obj._password_hash = row["password_hash"]
        obj.id_empleado = row["id_empleado"]
        obj.nombre = row["nombre"]
        obj.correo = row["correo"]
        obj.direccion = row["direccion"]
        obj.telefono = row["telefono"]
        obj.fecha_contrato = row["fecha_contrato"]
        obj.salario = row["salario"]
        obj.rol = row["rol"]
        obj.departamento_id = row["departamento_id"]
        return obj

    @staticmethod
    def buscar_por_id(id_empleado):
        conn = abrir_conexion()
        try:
            row = conn.execute("""
                SELECT e.*, u.username, u.password_hash
                FROM empleado e JOIN usuario u ON u.id = e.usuario_id
                WHERE e.id_empleado = ?
            """, (id_empleado,)).fetchone()
            return EmpleadoDAO._desde_fila(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def listar():
        conn = abrir_conexion()
        try:
            rows = conn.execute("""
                SELECT e.*, u.username, u.password_hash
                FROM empleado e JOIN usuario u ON u.id = e.usuario_id
                ORDER BY e.id_empleado
            """).fetchall()
            return [EmpleadoDAO._desde_fila(row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def actualizar(e):
        e.validar()
        conn = abrir_conexion()
        try:
            cur = conn.execute("""
                UPDATE empleado SET departamento_id=?, nombre=?, correo=?,
                    direccion=?, telefono=?, fecha_contrato=?, salario=?, rol=?
                WHERE id_empleado=?
            """, (e.departamento_id, e.nombre, e.correo, e.direccion,
                  e.telefono, e.fecha_contrato, e.salario, e.rol, e.id_empleado))
            conn.commit()
            return cur.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_empleado):
        conn = abrir_conexion()
        try:
            row = conn.execute(
                "SELECT usuario_id FROM empleado WHERE id_empleado=?",
                (id_empleado,)
            ).fetchone()
            if row is None:
                return False
            conn.execute("DELETE FROM empleado WHERE id_empleado=?", (id_empleado,))
            conn.execute("DELETE FROM usuario WHERE id=?", (row["usuario_id"],))
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
