from dataclasses import dataclass
from datetime import date



# ---- Backend -> Frontend DTOs ----

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


# ---- Frontend -> Backend Requests ----

# ---- Reservation Requests ----

@dataclass(frozen=True)
class MakeReservationRequest:
    room_id: int
    guest_name: str
    number_of_guests: int
    check_in_date: str
    check_out_date: str

@dataclass(frozen=True)
class EditReservationRequest:
    reservation_id: str
    room_id: int
    guest_name: str
    number_of_guests: int
    check_in_date: str
    check_out_date: str

@dataclass(frozen=True)
class DeleteReservationRequest:
    reservation_id: str


# ---- Floor Requests ----

@dataclass(frozen=True)
class AddFloorRequest:
    name: str
    level: int

@dataclass(frozen=True)
class RenameFloorRequest:
    floor_id: int
    new_name: str

@dataclass(frozen=True)
class UpdateFloorLevelRequest:
    floor_id: int
    new_level: int

@dataclass(frozen=True)
class RemoveFloorRequest:
    floor_id: int


# ---- Floor Element Requests ----

@dataclass(frozen=True)
class AddElementRequest:
    type: str
    floor_id: int
    position: tuple[int, int]
    number: str | None = None
    capacity: int | None = None
    price_per_night: float | None = None

@dataclass(frozen=True)
class EditRoomRequest:
    element_id: int
    number: str
    capacity: int
    price_per_night: float

@dataclass(frozen=True)
class MoveElementRequest:
    element_id: int
    floor_id: int
    position: tuple[int, int]

@dataclass(frozen=True)
class RemoveElementRequest:
    element_id: int
    type: str
    floor_id: int
    position: tuple[int, int]
