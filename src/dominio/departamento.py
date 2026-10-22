class Departamento:
    def __init__(self, id_depto=None, nombre=""):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre del departamento es obligatorio.")
        self.id_depto = id_depto
        self.nombre = nombre
        self._empleados = []
        self._gerente = None

    def gestionarDepto(self, opcion: str) -> bool:
        return opcion.strip().lower() in {"crear", "actualizar", "eliminar"}

    def asignarEmpleado(self, empleado) -> bool:
        if empleado in self._empleados:
            return False
        self._empleados.append(empleado)
        return True

    def reasignarEmpleado(self, empleado) -> bool:
        if empleado not in self._empleados:
            return False
        self._empleados.remove(empleado)
        if self._gerente is empleado:
            self._gerente = None
        return True

    def asignar_gerente(self, empleado) -> bool:
        if empleado not in self._empleados:
            return False
        self._gerente = empleado
        return True

    @property
    def empleados(self):
        return tuple(self._empleados)

    @property
    def gerente(self):
        return self._gerente

    def cantidad_empleados(self):
        return len(self._empleados)
