"""Servicio para la consulta y actualización de datos propios del usuario en sesión."""
from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from servicios.permisos import exigir_sesion


def ver_mi_ficha(sesion: dict) -> Empleado:
    """Devuelve la entidad Empleado del usuario en sesión."""
    exigir_sesion(sesion)
    empleado = EmpleadoDAO.obtener_por_id(sesion["empleado_id"])
    if empleado is None:
        raise ValueError("Empleado no encontrado.")
    return empleado


def mis_registros_de_tiempo(sesion: dict) -> list:
    """Devuelve los registros de tiempo propios usando el empleado_id de la sesión."""
    exigir_sesion(sesion)
    return RegistroTiempoDAO.listar_por_empleado(sesion["empleado_id"])


def mis_registros(sesion: dict) -> list:
    """Alias de compatibilidad para mis_registros_de_tiempo."""
    return mis_registros_de_tiempo(sesion)


def actualizar_mis_datos(sesion: dict, nombre: str, correo: str) -> bool:
    """Permite actualizar solo el nombre y correo del empleado conectado."""
    exigir_sesion(sesion)
    nombre = Empleado.validar_nombre(nombre)
    correo = Empleado.validar_correo(correo)

    empleado = EmpleadoDAO.obtener_por_id(sesion["empleado_id"])
    if empleado is None:
        raise ValueError("Empleado no encontrado.")

    empleado.nombre = nombre
    empleado.correo = correo
    return EmpleadoDAO.actualizar(empleado)


def registrar_mi_tiempo(sesion: dict, proyecto_id: int, fecha: str, horas: float, descripcion: str) -> int:
    """Guarda horas para el empleado autenticado, nunca para otro empleado."""
    from datetime import date
    from math import isfinite
    from persistencia.proyecto_dao import ProyectoDAO
    exigir_sesion(sesion)
    empleado_id = sesion.get("empleado_id")
    if not isinstance(empleado_id, int) or empleado_id <= 0:
        raise ValueError("La sesión no tiene un empleado asociado.")
    if EmpleadoDAO.obtener_por_id(empleado_id) is None:
        raise ValueError("El empleado no existe.")
    if ProyectoDAO.obtener_por_id(proyecto_id) is None:
        raise ValueError("El proyecto no existe.")
    try:
        date.fromisoformat(fecha)
    except (TypeError, ValueError):
        raise ValueError("Fecha inválida. Use AAAA-MM-DD.")
    if not isinstance(horas, (int, float)) or not isfinite(horas) or not 0 < horas <= 24:
        raise ValueError("Las horas deben ser mayores que 0 y hasta 24.")
    if not isinstance(descripcion, str) or not descripcion.strip():
        raise ValueError("La descripción es obligatoria.")
    return RegistroTiempoDAO.insertar(empleado_id, proyecto_id, fecha, horas, descripcion.strip())
