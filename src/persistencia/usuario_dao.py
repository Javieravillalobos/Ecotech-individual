from .conexion import abrir_conexion, marcador_sql
from dominio.usuario import Usuario


class UsuarioDAO:

    @staticmethod
    def insertar(u):
        conn = abrir_conexion()
        ph = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    INSERT INTO usuario(username, password_hash, empleado_id)
                    VALUES ({ph}, {ph}, {ph})
                    """,
                    (u.username, u.password, u.id_empleado)
                )
                u.id = cur.lastrowid
                conn.commit()
                return u
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def _desde_fila(row):
        obj = Usuario.__new__(Usuario)
        obj.id = row["id"]
        obj.username = row["username"]
        obj.password = row["password_hash"]
        obj.id_empleado = row["empleado_id"]
        return obj

    @staticmethod
    def buscar_por_id(id_usuario):
        conn = abrir_conexion()
        ph = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT *
                    FROM usuario
                    WHERE id = {ph}
                    """,
                    (id_usuario,)
                )
                row = cur.fetchone()
                return UsuarioDAO._desde_fila(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def buscar_por_username(username):
        conn = abrir_conexion()
        ph = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT *
                    FROM usuario
                    WHERE username = {ph}
                    """,
                    (username,)
                )
                row = cur.fetchone()
                return UsuarioDAO._desde_fila(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def listar():
        conn = abrir_conexion()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM usuario
                    ORDER BY id
                    """
                )
                rows = cur.fetchall()
                return [UsuarioDAO._desde_fila(row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def actualizar(u):
        conn = abrir_conexion()
        ph = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    UPDATE usuario
                    SET username = {ph}, password_hash = {ph}, empleado_id = {ph}
                    WHERE id = {ph}
                    """,
                    (
                        u.username,
                        u.password,
                        u.id_empleado,
                        u.id
                    )
                )
                conn.commit()
                return cur.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_usuario):
        conn = abrir_conexion()
        ph = marcador_sql()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    DELETE FROM usuario
                    WHERE id = {ph}
                    """,
                    (id_usuario,)
                )
                conn.commit()
                return cur.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()