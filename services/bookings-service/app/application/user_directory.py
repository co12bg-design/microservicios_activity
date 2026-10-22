from typing import Protocol
from uuid import UUID


class RegisteredUserChecker(Protocol):
    """Puerto para comprobar que la persona existe en users-service."""

    def exists(self, user_id: UUID) -> bool: ...
