"""Servicio para la consulta y actualización de datos propios del usuario en sesión."""
from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from servicios.permisos import exigir_sesion


def ver_mi_ficha(sesion: dict) -> Empleado:
    """Devuelve la entidad Empleado del usuario en sesión."""
    exigir_sesion(sesion)
    empleado = EmpleadoDAO.buscar_por_id(sesion["empleado_id"])
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

    empleado = EmpleadoDAO.buscar_por_id(sesion["empleado_id"])
    if empleado is None:
        raise ValueError("Empleado no encontrado.")

    empleado.nombre = nombre
    empleado.correo = correo
    return EmpleadoDAO.actualizar(empleado)