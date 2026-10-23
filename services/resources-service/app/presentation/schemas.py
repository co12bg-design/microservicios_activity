from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RoomResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    hotel_name: str
    name: str
    nightly_rate: Decimal
    currency: str
    active: bool
