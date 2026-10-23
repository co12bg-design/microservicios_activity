import calendar
from dataclasses import replace
from datetime import date
from uuid import UUID

from app.application.ports import (
    BookingNotifier,
    PaymentGateway,
    RoomCatalog,
    UpstreamServiceError,
    UserDirectory,
)
from app.domain.entities import Booking, BookingStatus, PaymentMethod
from app.domain.repositories import BookingRepository


class OverlappingBookingError(Exception):
    """Se intenta reservar fechas ocupadas para la misma habitación."""


class UserNotFoundError(Exception):
    """El identificador no corresponde a una persona registrada."""


class RoomNotFoundError(Exception):
    """La habitación no existe o no está activa."""


class CreateBooking:
    """Caso de uso: valida fechas, evita cruces y guarda la nueva reserva."""

    def __init__(
        self,
        repository: BookingRepository,
        users: UserDirectory,
        rooms: RoomCatalog,
        payments: PaymentGateway,
        notifications: BookingNotifier,
    ) -> None:
        self.repository = repository
        self.users = users
        self.rooms = rooms
        self.payments = payments
        self.notifications = notifications

    def execute(
        self,
        user_id: UUID,
        room_id: UUID,
        start_date: date,
        end_date: date,
        payment_method: PaymentMethod,
    ) -> Booking:
        contact = self.users.get_contact(user_id)
        if contact is None:
            raise UserNotFoundError("La persona debe estar registrada antes de reservar")
        room_quote = self.rooms.get_quote(room_id)
        if room_quote is None:
            raise RoomNotFoundError("La habitación no existe o no está disponible")
        today = date.today()
        if start_date < today:
            raise ValueError("La fecha de llegada no puede estar en el pasado")
        if start_date > add_months(today, 6):
            raise ValueError("Solo se puede reservar con hasta seis meses de anticipación")
        total_amount = room_quote.nightly_rate * (end_date - start_date).days
        booking = Booking.create(
            user_id=user_id,
            room_id=room_id,
            start_date=start_date,
            end_date=end_date,
            payment_method=payment_method,
            total_amount=total_amount,
            currency=room_quote.currency,
        )
        conflict = self.repository.find_overlapping(booking)
        if conflict is not None:
            raise OverlappingBookingError("La habitación ya tiene una reserva en esas fechas")
        self.repository.add(booking)
        try:
            payment = self.payments.process(booking)
            if payment.status != "SUCCEEDED":
                updated = replace(booking, status=BookingStatus.PAYMENT_FAILED)
                self.repository.update(updated)
                self.notifications.send_update(updated, contact, "El pago no fue exitoso")
                return updated
            confirmed = replace(
                booking,
                status=BookingStatus.CONFIRMED,
                payment_id=payment.payment_id,
            )
            self.repository.update(confirmed)
            self.notifications.send_update(
                confirmed,
                contact,
                "Pago exitoso y reserva confirmada",
            )
            return confirmed
        except UpstreamServiceError:
            raise


def add_months(day: date, months: int) -> date:
    """Suma meses calendario y ajusta el día si el mes destino es más corto."""
    month_index = day.month - 1 + months
    year = day.year + month_index // 12
    month = month_index % 12 + 1
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(day.day, last_day))
