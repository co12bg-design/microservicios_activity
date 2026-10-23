from fastapi import FastAPI

from app.application.send_booking_update import SendBookingUpdate
from app.domain.entities import Notification
from app.infrastructure.memory_notification_repository import MemoryNotificationRepository
from app.presentation.schemas import BookingUpdateRequest, NotificationResponse

app = FastAPI(title="Notifications Service", version="0.1.0")
repository = MemoryNotificationRepository()
send_update = SendBookingUpdate(repository)


@app.post("/notifications", response_model=list[NotificationResponse])
def post_notification(request: BookingUpdateRequest) -> list[Notification]:
    return send_update.execute(
        booking_id=request.booking_id,
        email=request.email,
        phone_number=request.phone_number,
        check_in=request.check_in,
        booking_status=request.booking_status,
        update_description=request.update_description,
    )


@app.get("/notifications", response_model=list[NotificationResponse])
def list_notifications() -> list[Notification]:
    return repository.list_all()
