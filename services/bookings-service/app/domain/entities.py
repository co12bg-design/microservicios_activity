from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal
from enum import StrEnum
from uuid import UUID, uuid4


class BookingStatus(StrEnum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    CANCELLED = "CANCELLED"


class PaymentMethod(StrEnum):
    CARD = "CARD"
    CASH = "CASH"
    BANK_TRANSFER = "BANK_TRANSFER"


@dataclass(frozen=True)
class Booking:
    """Reserva y regla de fechas, sin depender de HTTP ni de la base de datos."""

    id: UUID
    user_id: UUID
    room_id: UUID
    start_date: date
    end_date: date
    payment_method: PaymentMethod
    total_amount: Decimal
    currency: str
    payment_id: UUID | None
    status: BookingStatus
    created_at: datetime

    @classmethod
    def create(
        cls,
        user_id: UUID,
        room_id: UUID,
        start_date: date,
        end_date: date,
        payment_method: PaymentMethod,
        total_amount: Decimal,
        currency: str,
    ) -> "Booking":
        if start_date >= end_date:
            raise ValueError("La fecha de salida debe ser posterior a la fecha de llegada")
        if total_amount <= Decimal("0"):
            raise ValueError("El valor de la reserva debe ser mayor que cero")
        return cls(
            id=uuid4(),
            user_id=user_id,
            room_id=room_id,
            start_date=start_date,
            end_date=end_date,
            payment_method=payment_method,
            total_amount=total_amount,
            currency=currency,
            payment_id=None,
            status=BookingStatus.PENDING,
            created_at=datetime.now(timezone.utc),
        )

    def overlaps(self, other: "Booking") -> bool:
        """Indica si esta reserva se cruza con otra para la misma habitación."""
        same_room = self.room_id == other.room_id
        date_ranges_overlap = self.start_date < other.end_date and self.end_date > other.start_date
        return same_room and date_ranges_overlap
