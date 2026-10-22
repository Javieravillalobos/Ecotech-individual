"""Operaciones de dominio relacionadas con Empleado, separadas del menú de consola."""

from dominio.empleado import Empleado


def crear_empleado_desde_datos(datos):
    """Construye y valida un Empleado desde un diccionario de datos."""
    return Empleado(
        username=datos["username"],
        password=datos["password"],
        nombre=datos["nombre"],
        correo=datos["correo"],
        direccion=datos.get("direccion", ""),
        telefono=datos.get("telefono", ""),
        salario=datos.get("salario", 0),
        rol=datos.get("rol", "Empleado"),
        departamento_id=datos.get("departamento_id"),
    )
