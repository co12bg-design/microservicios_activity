from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class Room:
    id: UUID
    hotel_name: str
    name: str
    nightly_rate: Decimal
    currency: str = "COP"
    active: bool = True
