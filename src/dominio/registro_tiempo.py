from datetime import date


class RegistroTiempo:
    def __init__(self, id_registro=None, empleado_id=None, proyecto_id=None,
                 fecha=None, horas_trabajadas=0.0, descripcion_tarea=""):
        if not empleado_id or not proyecto_id:
            raise ValueError("Debe indicar un empleado y un proyecto.")
        horas = float(horas_trabajadas)
        if not 0 < horas <= 24:
            raise ValueError("Las horas deben ser mayores que 0 y hasta 24.")
        descripcion_tarea = descripcion_tarea.strip()
        if not descripcion_tarea:
            raise ValueError("La descripción de la tarea es obligatoria.")
        self.id_registro = id_registro
        self.empleado_id = int(empleado_id)
        self.proyecto_id = int(proyecto_id)
        self.fecha = (fecha or date.today().isoformat()).strip()
        self.horas_trabajadas = horas
        self.descripcion_tarea = descripcion_tarea

    def registrarHoras(self) -> bool:
        return 0 < self.horas_trabajadas <= 24

    def validarHoras(self) -> bool:
        return self.registrarHoras() and bool(self.descripcion_tarea)
