from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domain.entities import BookingStatus, PaymentMethod


class CreateBookingRequest(BaseModel):
    user_id: UUID
    room_id: UUID
    start_date: date
    end_date: date
    payment_method: PaymentMethod
    total_amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)

    @model_validator(mode="after")
    def dates_must_be_in_order(self) -> "CreateBookingRequest":
        if self.start_date >= self.end_date:
            raise ValueError("La fecha de salida debe ser posterior a la fecha de llegada")
        return self


class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    room_id: UUID
    start_date: date
    end_date: date
    payment_method: PaymentMethod
    total_amount: Decimal
    status: BookingStatus
    created_at: datetime
