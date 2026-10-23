from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4


class NotificationChannel(StrEnum):
    EMAIL = "EMAIL"
    SMS = "SMS"


@dataclass(frozen=True)
class Notification:
    id: UUID
    booking_id: UUID
    channel: NotificationChannel
    recipient: str
    message: str
    created_at: datetime
    delivery_status: str = "SIMULATED"

    @classmethod
    def create(
        cls, booking_id: UUID, channel: NotificationChannel, recipient: str, message: str
    ) -> "Notification":
        return cls(uuid4(), booking_id, channel, recipient, message, datetime.now(timezone.utc))
