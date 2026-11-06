"""Entidad de dominio Proyecto."""


class Proyecto:
    """Representa un proyecto dentro del sistema EcoTech."""

    def __init__(
        self,
        id_proyecto: int = None,
        nombre: str = "",
        descripcion: str = "",
        fecha_inicio: str = "",
        fecha_fin: str = None,
        estado: str = "En progreso",
        **kwargs,
    ):
        self.id_proyecto = id_proyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado

    def __getitem__(self, item):
        """Permite acceso tipo diccionario (ej. proyecto['id_proyecto'])."""
        return getattr(self, item, None)

    def __str__(self) -> str:
        f_fin = self.fecha_fin if self.fecha_fin else "En desarrollo"
        return (
            f"\nID Proyecto  : {self.id_proyecto}\n"
            f"Nombre       : {self.nombre}\n"
            f"Descripción  : {self.descripcion}\n"
            f"Fecha Inicio : {self.fecha_inicio}\n"
            f"Fecha Fin    : {f_fin}\n"
            f"Estado       : {self.estado}"
        )

    def __repr__(self) -> str:
        return self.__str__()