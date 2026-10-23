from typing import Protocol
from uuid import UUID

from app.domain.entities import Room


class RoomRepository(Protocol):
    def get_by_id(self, room_id: UUID) -> Room | None: ...

    def list_all(self) -> list[Room]: ...
