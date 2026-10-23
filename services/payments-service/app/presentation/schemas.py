from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities import PaymentMethod, PaymentStatus


class ProcessPaymentRequest(BaseModel):
    booking_id: UUID
    method: PaymentMethod
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    currency: str = "COP"


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    booking_id: UUID
    method: PaymentMethod
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime
