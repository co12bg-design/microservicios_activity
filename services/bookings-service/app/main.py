import os
from uuid import UUID

from fastapi import FastAPI, HTTPException, status

from app.application.create_booking import CreateBooking, OverlappingBookingError, RoomNotFoundError, UserNotFoundError
from app.domain.entities import Booking
from app.infrastructure.memory_booking_repository import MemoryBookingRepository
from app.infrastructure.service_clients import (
    NotificationsServiceClient,
    PaymentsServiceClient,
    ResourcesServiceClient,
    UserServiceClient,
)
from app.application.ports import UpstreamServiceError
from app.presentation.schemas import BookingResponse, CreateBookingRequest

app = FastAPI(title="Bookings Service", version="0.1.0")
repository = MemoryBookingRepository()
create_booking = CreateBooking(
    repository=repository,
    users=UserServiceClient(os.getenv("USERS_SERVICE_URL", "http://127.0.0.1:8001")),
    rooms=ResourcesServiceClient(os.getenv("RESOURCES_SERVICE_URL", "http://127.0.0.1:8003")),
    payments=PaymentsServiceClient(os.getenv("PAYMENTS_SERVICE_URL", "http://127.0.0.1:8004")),
    notifications=NotificationsServiceClient(
        os.getenv("NOTIFICATIONS_SERVICE_URL", "http://127.0.0.1:8005")
    ),
)


@app.post("/bookings", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def post_booking(request: CreateBookingRequest) -> Booking:
    try:
        return create_booking.execute(
            user_id=request.user_id,
            room_id=request.room_id,
            start_date=request.start_date,
            end_date=request.end_date,
            payment_method=request.payment_method,
        )
    except OverlappingBookingError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except UserNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except RoomNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except UpstreamServiceError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Un servicio necesario no está disponible: {error}",
        ) from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.get("/bookings/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: UUID) -> Booking:
    booking = repository.get_by_id(booking_id)
    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
    return booking
