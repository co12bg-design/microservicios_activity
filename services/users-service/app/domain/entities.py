from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class User:
    """Usuario sencillo: el dominio no depende de FastAPI ni de una base de datos."""

    id: str
    name: str
    email: str
    phone_number: str
    password_hash: str

    @classmethod
    def create(
        cls, name: str, email: str, phone_number: str, password_hash: str
    ) -> "User":
        clean_name = name.strip()
        clean_email = email.strip().lower()
        if not clean_name:
            raise ValueError("El nombre no puede estar vacío")
        if not clean_email:
            raise ValueError("El correo no puede estar vacío")
        return cls(
            id=str(uuid4()),
            name=clean_name,
            email=clean_email,
            phone_number=phone_number.strip(),
            password_hash=password_hash,
        )
