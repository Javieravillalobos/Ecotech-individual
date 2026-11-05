from servicios.permisos import exigir_sesion
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from dominio.empleado import Empleado

def mis_registros(sesion):
    """Devuelve los registros de tiempo propios usando el empleado_id de la sesión."""
    exigir_sesion(sesion)
    # Nota: Asegúrate de que tu RegistroTiempoDAO tenga el método listar_por_empleado
    return RegistroTiempoDAO.listar_por_empleado(sesion["empleado_id"])

def actualizar_mis_datos(sesion, nombre, correo):
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