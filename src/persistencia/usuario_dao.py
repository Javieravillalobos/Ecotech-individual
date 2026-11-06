from contextlib import closing
"""DAO para la entidad Usuario con mapeo seguro de roles y contraseñas."""
import pymysql
from .conexion import abrir_conexion, marcador_sql
from dominio.usuario import Usuario


class UsuarioDAO:
    @classmethod
    def _obtener_hash(cls, usuario: Usuario) -> str:
        """Obtiene el hash de la contraseña independientemente del nombre del atributo/propiedad."""
        if hasattr(usuario, "password_hash"):
            return usuario.password_hash
        if hasattr(usuario, "_password_hash"):
            return usuario._password_hash
        if hasattr(usuario, "password"):
            return usuario.password
        raise AttributeError("El objeto Usuario no tiene un atributo de contraseña reconocible.")

    @classmethod
    def insertar(cls, usuario: Usuario) -> int:
        """Inserta un usuario convirtiendo el rol de minúsculas al ENUM de la BD."""
        conn = abrir_conexion()
        p = marcador_sql()
        
        # Mapear rol 'admin'/'empleado' a 'Administrador'/'Empleado' para MySQL
        rol_enum = "Administrador" if usuario.rol == "admin" else "Empleado"
        pwd_hash = cls._obtener_hash(usuario)
        
        try:
            with closing(conn.cursor()) as cursor:
                sql = f"""
                    INSERT INTO usuario (empleado_id, username, password_hash, rol)
                    VALUES ({p}, {p}, {p}, {p})
                """
                cursor.execute(
                    sql,
                    (usuario.empleado_id, usuario.username, pwd_hash, rol_enum)
                )
                id_generado = cursor.lastrowid
            conn.commit()
            return id_generado
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @classmethod
    def obtener_por_username(cls, username: str) -> Usuario | None:
        """Busca un usuario por username y mapea el rol a minúsculas ('admin'/'empleado')."""
        conn = abrir_conexion()
        p = marcador_sql()
        try:
            with closing(conn.cursor()) as cursor:
                sql = f"""
                    SELECT id_usuario AS id, empleado_id, username, password_hash, rol 
                    FROM usuario 
                    WHERE username = {p}
                """
                cursor.execute(sql, (username.strip(),))
                fila = cursor.fetchone()
                if not fila:
                    return None

                # Normalizar rol para el dominio Usuario ('Administrador' -> 'admin')
                rol_str = str(fila["rol"]).lower()
                if rol_str == "administrador":
                    rol_str = "admin"

                return Usuario.desde_hash(
                    username=fila["username"],
                    password_hash=fila["password_hash"],
                    empleado_id=fila["empleado_id"],
                    rol=rol_str,
                    id_usuario=fila["id"]
                )
        finally:
            conn.close()

    @classmethod
    def obtener_por_id(cls, id_usuario: int) -> Usuario | None:
        """Obtiene un usuario por su ID de usuario."""
        conn = abrir_conexion()
        p = marcador_sql()
        try:
            with closing(conn.cursor()) as cursor:
                sql = f"""
                    SELECT id_usuario AS id, empleado_id, username, password_hash, rol 
                    FROM usuario 
                    WHERE id_usuario = {p}
                """
                cursor.execute(sql, (id_usuario,))
                fila = cursor.fetchone()
                if not fila:
                    return None

                rol_str = str(fila["rol"]).lower()
                if rol_str == "administrador":
                    rol_str = "admin"

                return Usuario.desde_hash(
                    username=fila["username"],
                    password_hash=fila["password_hash"],
                    empleado_id=fila["empleado_id"],
                    rol=rol_str,
                    id_usuario=fila["id"]
                )
        finally:
            conn.close()

    @classmethod
    def listar(cls) -> list[dict]:
        """Lista todos los usuarios registrando sus roles normalizados."""
        conn = abrir_conexion()
        try:
            with closing(conn.cursor()) as cursor:
                sql = "SELECT id_usuario AS id, empleado_id, username, rol FROM usuario"
                cursor.execute(sql)
                filas = cursor.fetchall()
                for fila in filas:
                    rol_str = str(fila["rol"]).lower()
                    fila["rol"] = "admin" if rol_str == "administrador" else "empleado"
                return filas
        finally:
            conn.close()