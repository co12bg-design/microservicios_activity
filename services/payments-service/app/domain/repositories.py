from typing import Protocol
from uuid import UUID

from app.domain.entities import Payment


class PaymentRepository(Protocol):
    def add(self, payment: Payment) -> None: ...

    def get_by_booking(self, booking_id: UUID) -> Payment | None: ...

    def list_all(self) -> list[Payment]: ...
