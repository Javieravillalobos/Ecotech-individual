import bcrypt
from dominio.usuario import Usuario
from persistencia.usuario_dao import UsuarioDAO

MAX_BYTES_BCRYPT = 72

def crear_hash(clave):
    """Valida la contraseña y genera su hash con bcrypt."""
    clave = Usuario.validar_clave(clave)
    clave_bytes = clave.encode("utf-8")
    if len(clave_bytes) > MAX_BYTES_BCRYPT:
        raise ValueError("Máximo 72 bytes UTF-8 para bcrypt.")
    return bcrypt.hashpw(clave_bytes, bcrypt.gensalt()).decode("utf-8")

def registrar_usuario(empleado_id, nombre, clave):
    """Registra una nueva cuenta vinculada a un empleado."""
    nombre = Usuario.normalizar_usuario(nombre)
    if UsuarioDAO.buscar_por_username(nombre) is not None:
        raise ValueError("El nombre de usuario ya existe.")
    
    hash_guardado = crear_hash(clave)
    usuario = Usuario(nombre, hash_guardado, empleado_id)
    return UsuarioDAO.insertar(usuario)

def autenticar(nombre, clave):
    """Verifica las credenciales y devuelve los datos de la sesión si son válidos."""
    try:
        nombre = Usuario.normalizar_usuario(nombre)
    except (TypeError, ValueError):
        return None

    if not isinstance(clave, str):
        return None

    datos = clave.encode("utf-8")
    if not (0 < len(datos) <= MAX_BYTES_BCRYPT):
        return None

    cuenta = UsuarioDAO.buscar_por_username(nombre)
    if cuenta is None:
        return None

    if not bcrypt.checkpw(datos, cuenta.password.encode("utf-8")):
        return None

    # Devuelve el diccionario de sesión con los datos requeridos por las diapos
    return {
        "id": cuenta.id,
        "empleado_id": cuenta.id_empleado,
        "nombre_usuario": cuenta.username,
        "rol": getattr(cuenta, "rol", "empleado")
    }