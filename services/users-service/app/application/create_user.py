from app.domain.entities import User
from app.domain.repositories import UserRepository
from app.domain.passwords import PasswordHasher


class CreateUser:
    """Caso de uso: aplica la regla para no registrar dos veces el mismo correo."""

    def __init__(self, repository: UserRepository, password_hasher: PasswordHasher) -> None:
        self.repository = repository
        self.password_hasher = password_hasher

    def execute(self, name: str, email: str, phone_number: str, password: str) -> User:
        normalized_email = email.strip().lower()
        if self.repository.email_exists(normalized_email):
            raise ValueError("Ya existe un usuario con ese correo")
        user = User.create(
            name=name,
            email=normalized_email,
            phone_number=phone_number,
            password_hash=self.password_hasher.hash(password),
        )
        self.repository.add(user)
        return user
