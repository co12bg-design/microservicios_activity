from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol
from uuid import UUID

from app.domain.entities import Booking, PaymentMethod


@dataclass(frozen=True)
class UserContact:
    email: str
    phone_number: str


@dataclass(frozen=True)
class RoomQuote:
    nightly_rate: Decimal
    currency: str


@dataclass(frozen=True)
class PaymentReceipt:
    payment_id: UUID
    status: str


class UserDirectory(Protocol):
    def get_contact(self, user_id: UUID) -> UserContact | None: ...


class RoomCatalog(Protocol):
    def get_quote(self, room_id: UUID) -> RoomQuote | None: ...


class PaymentGateway(Protocol):
    def process(self, booking: Booking) -> PaymentReceipt: ...


class BookingNotifier(Protocol):
    def send_update(self, booking: Booking, contact: UserContact, description: str) -> None: ...


class UpstreamServiceError(Exception):
    """Un servicio necesario para crear la reserva no respondió correctamente."""
