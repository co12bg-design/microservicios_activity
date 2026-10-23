from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from enum import StrEnum
from uuid import UUID, uuid4


class PaymentMethod(StrEnum):
    CARD = "CARD"
    CASH = "CASH"
    BANK_TRANSFER = "BANK_TRANSFER"


class PaymentStatus(StrEnum):
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class Payment:
    id: UUID
    booking_id: UUID
    method: PaymentMethod
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime

    @classmethod
    def simulated_success(
        cls, booking_id: UUID, method: PaymentMethod, amount: Decimal, currency: str
    ) -> "Payment":
        return cls(uuid4(), booking_id, method, amount, currency, PaymentStatus.SUCCEEDED, datetime.now(timezone.utc))
