"""Entidad de dominio RegistroTiempo."""


class RegistroTiempo:
    """Representa un registro de horas trabajadas por un empleado en un proyecto."""

    def __init__(
        self,
        id_registro: int = None,
        empleado_id: int = None,
        proyecto_id: int = None,
        fecha: str = "",
        horas_trabajadas: float = 0.0,
        descripcion_tarea: str = "",
        empleado: str = None,
        proyecto: str = None,
    ):
        self.id_registro = id_registro
        self.empleado_id = empleado_id
        self.proyecto_id = proyecto_id
        self.fecha = fecha
        self.horas_trabajadas = horas_trabajadas
        self.descripcion_tarea = descripcion_tarea
        self._empleado = empleado
        self._proyecto = proyecto

    @property
    def empleado(self) -> str:
        """Propiedad de compatibilidad para vistas que solicitan .empleado."""
        if self._empleado:
            return self._empleado
        return f"Empleado #{self.empleado_id}" if self.empleado_id else "N/A"

    @property
    def proyecto(self) -> str:
        """Propiedad de compatibilidad para vistas que solicitan .proyecto."""
        if self._proyecto:
            return self._proyecto
        return f"Proyecto #{self.proyecto_id}" if self.proyecto_id else "N/A"

    def __getitem__(self, item):
        """Permite acceso por clave para compatibilidad con diccionarios."""
        return getattr(self, item, None)

    def __str__(self) -> str:
        """Representación legible en texto para la consola."""
        return (
            f"ID: {self.id_registro} | Fecha: {self.fecha} | "
            f"Proyecto: {self.proyecto} | Horas: {self.horas_trabajadas}h | "
            f"Tarea: {self.descripcion_tarea}"
        )

    def __repr__(self) -> str:
        return self.__str__()