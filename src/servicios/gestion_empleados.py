from servicios.permisos import exigir_admin
from persistencia.empleado_dao import EmpleadoDAO
from dominio.empleado import Empleado

def listar_todos_los_empleados(sesion):
    """Permite al administrador listar a todo el personal."""
    exigir_admin(sesion)
    return EmpleadoDAO.listar_todos()

def registrar_nuevo_empleado(sesion, nombre, correo, departamento_id):
    """Permite al administrador dar de alta un nuevo empleado."""
    exigir_admin(sesion)
    nombre = Empleado.validar_nombre(nombre)
    correo = Empleado.validar_correo(correo)
    
    empleado = Empleado(None, nombre, correo, departamento_id)
    return EmpleadoDAO.insertar(empleado)