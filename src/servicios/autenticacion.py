import bcrypt
from dominio.usuario import Usuario
from persistencia.usuario_dao import UsuarioDAO

MAX_BYTES_BCRYPT = 72


def crear_hash(clave: str) -> str:
    """Valida la contraseña y genera su hash con bcrypt."""
    if not clave:
        raise ValueError("La contraseña no puede estar vacía.")

    clave_bytes = clave.encode("utf-8")
    if len(clave_bytes) > MAX_BYTES_BCRYPT:
        raise ValueError("Máximo 72 bytes UTF-8 para bcrypt.")

    return bcrypt.hashpw(clave_bytes, bcrypt.gensalt()).decode("utf-8")


def registrar_usuario(
    empleado_id: int, nombre: str, clave: str, rol: str = "empleado"
):
    """Registra una nueva cuenta vinculada a un empleado."""
    if not nombre:
        raise ValueError("El nombre de usuario no puede estar vacío.")

    nombre_limpio = nombre.strip().lower()

    if UsuarioDAO.obtener_por_username(nombre_limpio) is not None:
        raise ValueError("El nombre de usuario ya existe.")

    # Instanciación según el modelo de dominio Usuario
    usuario = Usuario(
        username=nombre_limpio,
        password=clave,
        empleado_id=empleado_id,
        rol=rol,
    )

    return UsuarioDAO.insertar(usuario)


def autenticar(nombre: str, clave: str) -> dict | None:
    """Verifica las credenciales y devuelve los datos de la sesión si son válidos."""
    try:
        if not nombre or not clave:
            return None
        nombre_limpio = nombre.strip().lower()
    except (TypeError, ValueError, AttributeError):
        return None

    # Validar tamaño máximo para el búfer de clave
    clave_bytes = clave.encode("utf-8")
    if not (0 < len(clave_bytes) <= MAX_BYTES_BCRYPT):
        return None

    # Obtener la cuenta desde el DAO
    cuenta = UsuarioDAO.obtener_por_username(nombre_limpio)
    if cuenta is None:
        return None

    # Autenticación delegada al método nativo de la entidad Usuario
    if not cuenta.autenticar(clave):
        return None

    # Diccionario de sesión estandarizado compatible con menu_principal.py
    return {
        "id_usuario": cuenta.id,
        "username": cuenta.username,
        "nombre_usuario": cuenta.username,
        "rol": cuenta.rol,
        "empleado_id": cuenta.empleado_id,
    }