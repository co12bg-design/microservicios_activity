from datetime import date
from uuid import UUID

from app.domain.entities import Notification, NotificationChannel
from app.domain.repositories import NotificationRepository


class SendBookingUpdate:
    def __init__(self, repository: NotificationRepository) -> None:
        self.repository = repository

    def execute(
        self,
        booking_id: UUID,
        email: str,
        phone_number: str,
        check_in: date,
        booking_status: str,
        update_description: str,
    ) -> list[Notification]:
        message = (
            f"Reserva {booking_id}: {update_description}. "
            f"Estado: {booking_status}. Llegada: {check_in.isoformat()}."
        )
        notices = [
            Notification.create(booking_id, NotificationChannel.EMAIL, email, message),
            Notification.create(booking_id, NotificationChannel.SMS, phone_number, message),
        ]
        for notice in notices:
            self.repository.add(notice)
        return notices
