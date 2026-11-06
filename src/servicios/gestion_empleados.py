"""Servicio para la gestión de empleados (exclusivo Administrador)."""
from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO
from servicios.permisos import exigir_admin


def listar_todos_los_empleados(sesion):
    """Permite al administrador listar a todo el personal."""
    exigir_admin(sesion)
    return EmpleadoDAO.listar()


def registrar_nuevo_empleado(sesion, nombre, correo, departamento_id=None):
    """Permite al administrador dar de alta un nuevo empleado."""
    exigir_admin(sesion)

    # Validar reglas de dominio antes de la persistencia
    nombre = Empleado.validar_nombre(nombre)
    correo = Empleado.validar_correo(correo)

    # Construir entidad validada
    empleado = Empleado(nombre=nombre, correo=correo, departamento_id=departamento_id)
    
    # Persistir en la base de datos
    return EmpleadoDAO.insertar(empleado)