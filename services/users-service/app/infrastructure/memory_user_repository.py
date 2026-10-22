from app.domain.entities import User


class MemoryUserRepository:
    """Adaptador inicial: guarda datos en memoria mientras el proceso está activo."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def add(self, user: User) -> None:
        self._users[user.id] = user

    def get_by_id(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    def email_exists(self, email: str) -> bool:
        return any(user.email == email for user in self._users.values())
