import calendar
from datetime import date
from decimal import Decimal
from uuid import UUID

from app.domain.entities import Booking, PaymentMethod
from app.domain.repositories import BookingRepository
from app.application.user_directory import RegisteredUserChecker


class OverlappingBookingError(Exception):
    """Se intenta reservar fechas ocupadas para la misma habitación."""


class UserNotFoundError(Exception):
    """El identificador no corresponde a una persona registrada."""


class CreateBooking:
    """Caso de uso: valida fechas, evita cruces y guarda la nueva reserva."""

    def __init__(self, repository: BookingRepository, user_checker: RegisteredUserChecker) -> None:
        self.repository = repository
        self.user_checker = user_checker

    def execute(
        self,
        user_id: UUID,
        room_id: UUID,
        start_date: date,
        end_date: date,
        payment_method: PaymentMethod,
        total_amount: Decimal,
    ) -> Booking:
        if not self.user_checker.exists(user_id):
            raise UserNotFoundError("La persona debe estar registrada antes de reservar")
        today = date.today()
        if start_date < today:
            raise ValueError("La fecha de llegada no puede estar en el pasado")
        if start_date > add_months(today, 6):
            raise ValueError("Solo se puede reservar con hasta seis meses de anticipación")
        booking = Booking.create(
            user_id=user_id,
            room_id=room_id,
            start_date=start_date,
            end_date=end_date,
            payment_method=payment_method,
            total_amount=total_amount,
        )
        conflict = self.repository.find_overlapping(booking)
        if conflict is not None:
            raise OverlappingBookingError("La habitación ya tiene una reserva en esas fechas")
        self.repository.add(booking)
        return booking


def add_months(day: date, months: int) -> date:
    """Suma meses calendario y ajusta el día si el mes destino es más corto."""
    month_index = day.month - 1 + months
    year = day.year + month_index // 12
    month = month_index % 12 + 1
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(day.day, last_day))
