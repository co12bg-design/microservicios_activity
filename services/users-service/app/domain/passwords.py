from typing import Protocol


class PasswordHasher(Protocol):
    """Contrato para guardar contraseñas como hashes, nunca como texto legible."""

    def hash(self, password: str) -> str: ...
