from uuid import UUID

from app.domain.entities import Room
from app.domain.repositories import RoomRepository


class GetRooms:
    def __init__(self, repository: RoomRepository) -> None:
        self.repository = repository

    def list(self) -> list[Room]:
        return self.repository.list_all()

    def get(self, room_id: UUID) -> Room | None:
        return self.repository.get_by_id(room_id)
