import httpx
from decimal import Decimal
from uuid import UUID

from app.application.ports import (
    PaymentReceipt,
    RoomQuote,
    UpstreamServiceError,
    UserContact,
)
from app.domain.entities import Booking


class UserServiceClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def get_contact(self, user_id: UUID) -> UserContact | None:
        try:
            response = httpx.get(f"{self.base_url}/users/{user_id}", timeout=3.0)
        except httpx.RequestError as error:
            raise UpstreamServiceError("users-service no respondió") from error
        if response.status_code == 404:
            return None
        if response.status_code != 200:
            raise UpstreamServiceError("users-service devolvió un error")
        data = response.json()
        return UserContact(email=data["email"], phone_number=data["phone_number"])


class ResourcesServiceClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def get_quote(self, room_id: UUID) -> RoomQuote | None:
        try:
            response = httpx.get(f"{self.base_url}/rooms/{room_id}", timeout=3.0)
        except httpx.RequestError as error:
            raise UpstreamServiceError("resources-service no respondió") from error
        if response.status_code == 404:
            return None
        if response.status_code != 200:
            raise UpstreamServiceError("resources-service devolvió un error")
        data = response.json()
        return RoomQuote(nightly_rate=Decimal(data["nightly_rate"]), currency=data["currency"])


class PaymentsServiceClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def process(self, booking: Booking) -> PaymentReceipt:
        body = {
            "booking_id": str(booking.id),
            "method": booking.payment_method.value,
            "amount": str(booking.total_amount),
            "currency": booking.currency,
        }
        try:
            response = httpx.post(f"{self.base_url}/payments", json=body, timeout=3.0)
            response.raise_for_status()
        except httpx.HTTPError as error:
            raise UpstreamServiceError("payments-service no pudo procesar el pago") from error
        data = response.json()
        return PaymentReceipt(payment_id=UUID(data["id"]), status=data["status"])


class NotificationsServiceClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def send_update(self, booking: Booking, contact: UserContact, description: str) -> None:
        body = {
            "booking_id": str(booking.id),
            "email": contact.email,
            "phone_number": contact.phone_number,
            "check_in": booking.start_date.isoformat(),
            "booking_status": booking.status.value,
            "update_description": description,
        }
        try:
            response = httpx.post(f"{self.base_url}/notifications", json=body, timeout=3.0)
            response.raise_for_status()
        except httpx.HTTPError as error:
            raise UpstreamServiceError("notifications-service no pudo registrar los avisos") from error
