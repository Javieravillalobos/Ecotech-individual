from .conexion import abrir_conexion, marcador_sql
from dominio.usuario import Usuario


class UsuarioDAO:
    @staticmethod
    def insertar(usuario: Usuario) -> int:
        if not usuario.empleado_id:
            raise ValueError("No se puede crear un usuario sin asociar un empleado_id.")

        conn = abrir_conexion()
        p = marcador_sql()
        try:
            with conn.cursor() as cursor:
                sql = f"""
                    INSERT INTO usuario (empleado_id, username, password_hash, rol)
                    VALUES ({p}, {p}, {p}, {p})
                """
                cursor.execute(
                    sql,
                    (
                        usuario.empleado_id,
                        usuario.username,
                        usuario._hash_para_persistencia(),
                        usuario.rol,
                    ),
                )
                id_generado = cursor.lastrowid
                usuario.id = id_generado
            conn.commit()
            return id_generado
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def obtener_por_username(username: str) -> Usuario | None:
        conn = abrir_conexion()
        p = marcador_sql()
        try:
            with conn.cursor() as cursor:
                sql = f"""
                    SELECT id, empleado_id, username, password_hash, rol 
                    FROM usuario WHERE username = {p}
                """
                cursor.execute(sql, (username.strip(),))
                f = cursor.fetchone()
                if not f:
                    return None
                return Usuario.desde_hash(
                    id_usuario=f["id"],
                    username=f["username"],
                    password_hash=f["password_hash"],
                    empleado_id=f["empleado_id"],
                    rol=f["rol"],
                )
        finally:
            conn.close()