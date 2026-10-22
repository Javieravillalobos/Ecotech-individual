import hashlib
import hmac
import os


class Usuario:
    """Usuario del sistema; guarda un hash PBKDF2, nunca la contraseña original."""

    def __init__(self, username: str, password: str):
        username = username.strip()
        if not username:
            raise ValueError("El nombre de usuario es obligatorio.")
        if not password:
            raise ValueError("La contraseña es obligatoria.")
        self.username = username
        self._password_hash = self._crear_hash(password)

    @staticmethod
    def _crear_hash(password: str, salt: bytes | None = None) -> str:
        salt = salt or os.urandom(16)
        derived = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, 200_000
        )
        return f"{salt.hex()}${derived.hex()}"

    @classmethod
    def desde_hash(cls, username: str, password_hash: str):
        """Reconstruye el objeto desde la base sin tratar el hash como contraseña."""
        obj = cls.__new__(cls)
        obj.username = username
        obj._password_hash = password_hash
        return obj

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
        """Uso interno de persistencia; no imprime ni expone el hash en el menú."""
        return self._password_hash

    def exportarReporte(self, tipo: str, formato: str) -> bool:
        return bool(tipo.strip() and formato.strip())
