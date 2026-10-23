from typing import Protocol
from uuid import UUID

from app.domain.entities import Booking


class BookingRepository(Protocol):
    """Contrato que deben cumplir los adaptadores de almacenamiento de reservas."""

    def add(self, booking: Booking) -> None: ...

    def update(self, booking: Booking) -> None: ...

    def get_by_id(self, booking_id: UUID) -> Booking | None: ...

    def find_overlapping(self, booking: Booking) -> Booking | None: ...
