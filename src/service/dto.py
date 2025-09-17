from dataclasses import dataclass
from datetime import date



@dataclass(frozen=True)
class FloorDTO:
    db_id: int
    name: str
    level: int
    elements: dict[int, 'FloorElementDTO']

@dataclass(frozen=True)
class FloorElementDTO:
    db_id: int
    type: str
    floor_id: int
    position: tuple[int, int]

@dataclass(frozen=True)
class RoomDTO:
    db_id: int
    type: str
    floor_id: int
    position: tuple[int, int]
    number: str
    capacity: int
    price_per_night: float

@dataclass(frozen=True)
class ReservationDTO:
    reservation_id: int
    room_id: int
    room_number: str
    guest_name: str
    number_of_guests: int
    check_in_date: date
    check_out_date: date
