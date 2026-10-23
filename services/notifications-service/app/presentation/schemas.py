from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.domain.entities import NotificationChannel


class BookingUpdateRequest(BaseModel):
    booking_id: UUID
    email: EmailStr
    phone_number: str = Field(pattern=r"^\+[1-9]\d{7,14}$")
    check_in: date
    booking_status: str
    update_description: str


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    booking_id: UUID
    channel: NotificationChannel
    recipient: str
    message: str
    created_at: datetime
    delivery_status: str
