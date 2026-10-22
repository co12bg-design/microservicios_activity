from uuid import UUID

from app.domain.entities import Booking, BookingStatus


class MemoryBookingRepository:
    """Adaptador inicial: las reservas desaparecen cuando se detiene el servicio."""

    def __init__(self) -> None:
        self._bookings: dict[UUID, Booking] = {}

    def add(self, booking: Booking) -> None:
        self._bookings[booking.id] = booking

    def get_by_id(self, booking_id: UUID) -> Booking | None:
        return self._bookings.get(booking_id)

    def find_overlapping(self, booking: Booking) -> Booking | None:
        for existing in self._bookings.values():
            if existing.status == BookingStatus.CANCELLED:
                continue
            if booking.overlaps(existing):
                return existing
        return None
