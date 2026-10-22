from typing import Protocol

from app.domain.entities import User


class UserRepository(Protocol):
    """Contrato: cualquier forma de guardar usuarios debe ofrecer estas operaciones."""

    def add(self, user: User) -> None: ...

    def get_by_id(self, user_id: str) -> User | None: ...

    def email_exists(self, email: str) -> bool: ...
