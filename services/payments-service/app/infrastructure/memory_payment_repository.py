from uuid import UUID

from app.domain.entities import Payment


class MemoryPaymentRepository:
    def __init__(self) -> None:
        self._payments: dict[UUID, Payment] = {}

    def add(self, payment: Payment) -> None:
        self._payments[payment.booking_id] = payment

    def get_by_booking(self, booking_id: UUID) -> Payment | None:
        return self._payments.get(booking_id)

    def list_all(self) -> list[Payment]:
        return list(self._payments.values())
