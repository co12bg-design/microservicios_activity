from app.domain.entities import Notification


class MemoryNotificationRepository:
    """Registra avisos simulados para que se puedan revisar durante la práctica."""

    def __init__(self) -> None:
        self._notifications: list[Notification] = []

    def add(self, notification: Notification) -> None:
        self._notifications.append(notification)

    def list_all(self) -> list[Notification]:
        return list(self._notifications)
