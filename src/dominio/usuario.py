import hashlib
import hmac
import os


class Usuario:
    """Usuario del sistema; vincula a un empleado y gestiona el hash PBKDF2 y roles."""

    ROLES_PERMITIDOS = {"admin", "empleado"}

    def __init__(
        self,
        username: str,
        password: str | None = None,
        empleado_id: int | None = None,
        rol: str = "empleado",
        id_usuario: int | None = None,
        password_hash: str | None = None,
    ):
        username = username.strip()
        if not username:
            raise ValueError("El nombre de usuario es obligatorio.")
        
        rol_clean = rol.strip().lower()
        if rol_clean not in self.ROLES_PERMITIDOS:
            raise ValueError(f"Rol no válido. Debe ser uno de: {self.ROLES_PERMITIDOS}")

        self.id = id_usuario
        self.empleado_id = empleado_id
        self.username = username
        self.rol = rol_clean

        if password_hash:
            self._password_hash = password_hash
        elif password:
            self._password_hash = self._crear_hash(password)
        else:
            raise ValueError("Debe proporcionar una contraseña o un hash existente.")

    @staticmethod
    def _crear_hash(password: str, salt: bytes | None = None) -> str:
        salt = salt or os.urandom(16)
        derived = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, 200_000
        )
        return f"{salt.hex()}${derived.hex()}"

    @classmethod
    def desde_hash(cls, username: str, password_hash: str, empleado_id: int | None = None, rol: str = "empleado", id_usuario: int | None = None):
        """Reconstruye el objeto desde la base de datos sin tratar el hash como contraseña."""
        return cls(
            username=username,
            password=None,
            empleado_id=empleado_id,
            rol=rol,
            id_usuario=id_usuario,
            password_hash=password_hash,
        )

    def autenticar(self, password: str) -> bool:
        try:
            salt_hex, expected_hex = self._password_hash.split("$", 1)
            candidate = self._crear_hash(password, bytes.fromhex(salt_hex))
            _, candidate_hex = candidate.split("$", 1)
            return hmac.compare_digest(expected_hex, candidate_hex)
        except (ValueError, TypeError):
            return False

    def encriptarPassword(self, password: str) -> bool:
        if not password:
            return False
        self._password_hash = self._crear_hash(password)
        return True

    def _hash_para_persistencia(self) -> str:
        return self._password_hash