from datetime import date
from .conexion import abrir_conexion, obtener_motor, marcador_sql
from dominio.empleado import Empleado


class EmpleadoDAO:
    @staticmethod
    def insertar(e):
        conn = abrir_conexion()
        motor = obtener_motor()
        ph = marcador_sql()
        try:
            with conn.cursor() as cur:
                # Desactivamos temporalmente las restricciones de claves foráneas según el motor
                if motor == "sqlite":
                    cur.execute("PRAGMA foreign_keys = OFF;")
                else:
                    cur.execute("SET foreign_key_checks = 0;")
                
                # 1. Insertamos el empleado
                cur.execute(
                    f"""
                    INSERT INTO empleado(departamento_id, nombre, correo,
                        direccion, telefono, fecha_contrato, salario, rol)
                    VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph})
                    """,
                    (e.departamento_id, e.nombre, e.correo,
                     e.direccion, e.telefono, e.fecha_contrato, e.salario, e.rol)
                )
                e.id_empleado = cur.lastrowid
                
                # 2. Insertamos el usuario vinculándolo al empleado_id
                cur.execute(
                    f"INSERT INTO usuario(username, password_hash, empleado_id) VALUES ({ph}, {ph}, {ph})",
                    (e.username, e._hash_para_persistencia(), e.id_empleado)
                )
                uid = cur.lastrowid
                
                # 3. Actualizamos el empleado con el usuario_id correspondiente
                try:
                    cur.execute(
                        f"UPDATE empleado SET usuario_id = {ph} WHERE id_empleado = {ph}",
                        (uid, e.id_empleado)
                    )
                except Exception:
                    pass
                
                # Reactivamos las restricciones según el motor
                if motor == "sqlite":
                    cur.execute("PRAGMA foreign_keys = ON;")
                else:
                    cur.execute("SET foreign_key_checks = 1;")
                    
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
        ph = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(f"""
                    SELECT e.*, u.username, u.password_hash
                    FROM empleado e JOIN usuario u ON u.id = e.usuario_id
                    WHERE e.id_empleado = {ph}
                """, (id_empleado,))
                row = cur.fetchone()
                return EmpleadoDAO._desde_fila(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def listar():
        conn = abrir_conexion()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT e.*, u.username, u.password_hash
                    FROM empleado e JOIN usuario u ON u.id = e.usuario_id
                    ORDER BY e.id_empleado
                """)
                rows = cur.fetchall()
                return [EmpleadoDAO._desde_fila(row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def actualizar(e):
        e.validar()
        conn = abrir_conexion()
        ph = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(f"""
                    UPDATE empleado SET departamento_id={ph}, nombre={ph}, correo={ph},
                        direccion={ph}, telefono={ph}, fecha_contrato={ph}, salario={ph}, rol={ph}
                    WHERE id_empleado={ph}
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
        ph = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT usuario_id FROM empleado WHERE id_empleado={ph}",
                    (id_empleado,)
                )
                row = cur.fetchone()
                if row is None:
                    return False
                cur.execute(f"DELETE FROM empleado WHERE id_empleado={ph}", (id_empleado,))
                cur.execute(f"DELETE FROM usuario WHERE id={ph}", (row["usuario_id"],))
                conn.commit()
                return True
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()