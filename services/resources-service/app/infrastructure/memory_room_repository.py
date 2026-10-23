from decimal import Decimal
from uuid import UUID

from app.domain.entities import Room


class MemoryRoomRepository:
    """Habitaciones de demostración; se reemplazarán por una base de datos."""

    def __init__(self) -> None:
        samples = [
            Room(UUID("11111111-1111-4111-8111-111111111111"), "Hotel Demo", "Habitación estándar", Decimal("180000")),
            Room(UUID("22222222-2222-4222-8222-222222222222"), "Hotel Demo", "Habitación familiar", Decimal("250000")),
        ]
        self._rooms = {room.id: room for room in samples}

    def get_by_id(self, room_id: UUID) -> Room | None:
        return self._rooms.get(room_id)

    def list_all(self) -> list[Room]:
        return list(self._rooms.values())
