import hashlib
import secrets


class ScryptPasswordHasher:
    """Adaptador con hash lento y sal aleatoria usando la biblioteca estándar."""

    def hash(self, password: str) -> str:
        salt = secrets.token_bytes(16)
        derived_key = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
        return f"scrypt${salt.hex()}${derived_key.hex()}"
