"""Módulo de control de acceso y permisos por rol para EcoTech."""


def exigir_sesion(sesion):
    """Exige que exista una sesión activa y válida."""
    if not isinstance(sesion, dict):
        raise PermissionError("Debe iniciar sesión para realizar esta acción.")

    if sesion.get("rol") not in ("admin", "empleado"):
        raise PermissionError("Acceso no permitido.")

    empleado_id = sesion.get("empleado_id")
    if type(empleado_id) is not int or empleado_id <= 0:
        raise PermissionError("Sesión inválida o ID de empleado no válido.")


def exigir_admin(sesion):
    """Exige que la sesión activa pertenezca a un administrador."""
    exigir_sesion(sesion)
    if sesion.get("rol") != "admin":
        raise PermissionError("Acción exclusiva para administradores.")