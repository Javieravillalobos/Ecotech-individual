"""Entidad de dominio Empleado con validación estricta de roles."""

ROLES_PERMITIDOS = ["Empleado", "Administrador"]


class Empleado:
    """Representa a un empleado dentro de la organización."""

    def __init__(
        self,
        id_empleado: int = None,
        departamento_id: int = None,
        nombre: str = "",
        correo: str = "",
        direccion: str = "",
        telefono: str = "",
        fecha_contrato: str = "",
        salario: float = 0.0,
        rol: str = "Empleado",
        username: str = "",
        **kwargs,
    ):
        self.id_empleado = id_empleado
        self.departamento_id = departamento_id
        self.nombre = nombre
        self.correo = correo
        self.direccion = direccion
        self.telefono = telefono
        self.fecha_contrato = fecha_contrato
        self.salario = salario
        self.username = username
        self.rol = self._validar_rol(rol)

    def _validar_rol(self, rol: str) -> str:
        """Verifica que el rol ingresado pertenezca a la lista de roles permitidos."""
        if not rol or not str(rol).strip():
            return "Empleado"

        rol_formateado = str(rol).strip().capitalize()
        if rol_formateado not in ROLES_PERMITIDOS:
            raise ValueError(
                f"Rol inválido '{rol}'. Los roles permitidos son exclusivamente: {', '.join(ROLES_PERMITIDOS)}"
            )
        return rol_formateado

    def actualizarPerfil(
        self,
        nombre: str = None,
        correo: str = None,
        direccion: str = None,
        telefono: str = None,
        salario: float = None,
        rol: str = None,
        **kwargs,
    ):
        """Actualiza los atributos del perfil del empleado."""
        if nombre is not None and nombre.strip():
            self.nombre = nombre.strip()
        if correo is not None and correo.strip():
            self.correo = correo.strip()
        if direccion is not None:
            self.direccion = direccion.strip()
        if telefono is not None:
            self.telefono = telefono.strip()
        if salario is not None:
            self.salario = float(salario)
        if rol is not None and rol.strip():
            self.rol = self._validar_rol(rol)

    def __getitem__(self, item):
        """Permite acceso por clave para compatibilidad con diccionarios."""
        return getattr(self, item, None)

    def __str__(self) -> str:
        """Representación legible en texto para la consola."""
        depto = self.departamento_id if self.departamento_id else "Sin asignar"
        return (
            f"\nID Empleado : {self.id_empleado}\n"
            f"Nombre      : {self.nombre}\n"
            f"Correo      : {self.correo}\n"
            f"Rol         : {self.rol}\n"
            f"Teléfono    : {self.telefono}\n"
            f"Dirección   : {self.direccion}\n"
            f"Contrato    : {self.fecha_contrato}\n"
            f"Salario     : ${self.salario:,.2f}\n"
            f"Depto ID    : {depto}"
        )

    def __repr__(self) -> str:
        return self.__str__()