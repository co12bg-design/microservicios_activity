from typing import Protocol

from app.domain.entities import Notification


class NotificationRepository(Protocol):
    def add(self, notification: Notification) -> None: ...

    def list_all(self) -> list[Notification]: ...
