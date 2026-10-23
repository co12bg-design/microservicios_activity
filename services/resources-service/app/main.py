from uuid import UUID

from fastapi import FastAPI, HTTPException, status

from app.application.get_rooms import GetRooms
from app.domain.entities import Room
from app.infrastructure.memory_room_repository import MemoryRoomRepository
from app.presentation.schemas import RoomResponse

app = FastAPI(title="Resources Service", version="0.1.0")
repository = MemoryRoomRepository()
get_rooms = GetRooms(repository)


@app.get("/rooms", response_model=list[RoomResponse])
def list_rooms() -> list[Room]:
    return get_rooms.list()


@app.get("/rooms/{room_id}", response_model=RoomResponse)
def get_room(room_id: UUID) -> Room:
    room = get_rooms.get(room_id)
    if room is None or not room.active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habitación no disponible")
    return room
