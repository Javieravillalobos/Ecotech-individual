from .conexion import abrir_conexion
from dominio.usuario import Usuario


class UsuarioDAO:

    @staticmethod
    def insertar(u):
        conn = abrir_conexion()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO usuario(username, password, id_empleado)
                VALUES (?, ?, ?)
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
        obj.password = row["password"]
        obj.id_empleado = row["id_empleado"]
        return obj

    @staticmethod
    def buscar_por_id(id_usuario):
        conn = abrir_conexion()
        try:
            row = conn.execute(
                """
                SELECT *
                FROM usuario
                WHERE id = ?
                """,
                (id_usuario,)
            ).fetchone()

            return UsuarioDAO._desde_fila(row) if row else None

        finally:
            conn.close()

    @staticmethod
    def buscar_por_username(username):
        conn = abrir_conexion()
        try:
            row = conn.execute(
                """
                SELECT *
                FROM usuario
                WHERE username = ?
                """,
                (username,)
            ).fetchone()

            return UsuarioDAO._desde_fila(row) if row else None

        finally:
            conn.close()

    @staticmethod
    def listar():
        conn = abrir_conexion()
        try:
            rows = conn.execute(
                """
                SELECT *
                FROM usuario
                ORDER BY id
                """
            ).fetchall()

            return [UsuarioDAO._desde_fila(row) for row in rows]

        finally:
            conn.close()

    @staticmethod
    def actualizar(u):
        conn = abrir_conexion()
        try:
            cur = conn.execute(
                """
                UPDATE usuario
                SET username = ?, password = ?, id_empleado = ?
                WHERE id = ?
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
        try:
            cur = conn.execute(
                """
                DELETE FROM usuario
                WHERE id = ?
                """,
                (id_usuario,)
            )

            conn.commit()
            return cur.rowcount > 0

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close(