from datetime import date
from .usuario import Usuario


class Empleado(Usuario):
    def __init__(
        self, username: str, password: str, id_empleado: int | None = None,
        nombre: str = "", correo: str = "", direccion: str = "",
        telefono: str = "", fecha_contrato: str | None = None,
        salario: float = 0.0, rol: str = "Empleado",
        departamento_id: int | None = None,
    ):
        super().__init__(username, password)
        self.id_empleado = id_empleado
        self.nombre = nombre.strip()
        self.correo = correo.strip()
        self.direccion = direccion.strip()
        self.telefono = telefono.strip()
        self.fecha_contrato = fecha_contrato or date.today().isoformat()
        self.salario = float(salario)
        self.rol = rol.strip() or "Empleado"
        self.departamento_id = departamento_id
        self.validar()

    def validar(self):
        if not self.nombre:
            raise ValueError("El nombre es obligatorio.")
        if "@" not in self.correo or "." not in self.correo.rsplit("@", 1)[-1]:
            raise ValueError("El correo no es válido.")
        if self.salario < 0:
            raise ValueError("El salario no puede ser negativo.")

    def obtenerSalario(self) -> float:
        return self.salario

    def actualizarPerfil(self, nombre, correo, direccion, telefono) -> bool:
        nombre, correo = nombre.strip(), correo.strip()
        if not nombre:
            return False
        if "@" not in correo or "." not in correo.rsplit("@", 1)[-1]:
            return False
        self.nombre, self.correo = nombre, correo
        self.direccion, self.telefono = direccion.strip(), telefono.strip()
        return True
