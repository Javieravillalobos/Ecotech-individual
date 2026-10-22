class Proyecto:
    def __init__(self, id_proyecto=None, nombre="", descripcion="",
                 fecha_inicio="", fecha_fin=""):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre del proyecto es obligatorio.")
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise ValueError("La fecha final no puede ser anterior a la inicial.")
        self.id_proyecto = id_proyecto
        self.nombre = nombre
        self.descripcion = descripcion.strip()
        self.fecha_inicio = fecha_inicio.strip()
        self.fecha_fin = fecha_fin.strip()
        self._empleados = []

    def gestionarProyecto(self, opcion: str) -> bool:
        return opcion.strip().lower() in {"crear", "actualizar", "eliminar"}

    def asignarEmpleado(self, empleado) -> bool:
        if empleado in self._empleados:
            return False
        self._empleados.append(empleado)
        return True

    def desasignarEmpleado(self, empleado) -> bool:
        if empleado not in self._empleados:
            return False
        self._empleados.remove(empleado)
        return True

    @property
    def empleados(self):
        return tuple(self._empleados)
