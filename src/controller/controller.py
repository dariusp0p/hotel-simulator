from datetime import datetime, date

from src.controller.dto import FloorDTO, FloorElementDTO, RoomDTO, ReservationDTO
from src.model.service.hotel_service import HotelService
from src.model.service.reservation_service import ReservationService
from src.utilities.exceptions import ControllerError
from src.controller.action_manager import ActionManager
from src.controller.action import (
    AddFloorAction, RemoveFloorAction, AddElementAction, RemoveElementAction,
    EditRoomAction, MoveElementAction, MakeReservationAction, EditReservationAction, DeleteReservationAction,
    UpdateFloorLevelAction, RenameFloorAction

)


class Controller:
    """
    Controller class that mediates between the view and the model.
    """
    def __init__(self, reservation_service: ReservationService, hotel_service: HotelService):
        self.__reservation_service = reservation_service
        self.__hotel_service = hotel_service
        self.__action_manager = ActionManager()

    # Undo/Redo operations
    def undo(self) -> None:
        """Undoes the last action."""
        self.__action_manager.undo()

    def redo(self) -> None:
        """Redoes the last undone action."""
        self.__action_manager.redo()

    def can_undo(self) -> bool:
        """Checks if there are actions to undo."""
        return self.__action_manager.can_undo()

    def can_redo(self) -> bool:
        """Checks if there are actions to redo."""
        return self.__action_manager.can_redo()

    def clear_stacks(self) -> None:
        """Clears the undo and redo stacks."""
        self.__action_manager.clear_stacks()

    # Getters

    # Hotel
    def get_floor(self, floor_id: int) -> FloorDTO:
        """Returns a FloorDTO for the specified floor ID."""
        return self._to_floor_dto(self.__hotel_service.get_floor(floor_id))

    def get_all_floors(self) -> list[FloorDTO]:
        """Returns a list of all FloorDTOs sorted by their level."""
        result = self.__hotel_service.get_all_floors_sorted_by_level()
        return [self._to_floor_dto(floor) for floor in result]

    def get_floor_grid(self, floor_id: int) -> dict[tuple[int, int], FloorElementDTO | RoomDTO | None]:
        """Returns the grid of floor elements and rooms for the specified floor ID."""
        grid = self.__hotel_service.get_floor_grid(floor_id)
        dto_grid = {}
        for position, element in grid.items():
            if element is None:
                dto_grid[position] = None
            elif element.type == 'room':
                dto_grid[position] = self._to_room_dto(element)
            else:
                dto_grid[position] = self._to_floor_element_dto(element)
        return dto_grid

    def get_floor_connections(self, floor_id: int) -> list[tuple[int, int]]:
        """Returns a list of connections (as tuples of positions) for the specified floor ID."""
        return self.__hotel_service.get_floor_connections(floor_id)

    def get_floor_elements(self, floor_id: int) -> list[FloorElementDTO]:
        """Returns a list of FloorElementDTOs for the specified floor ID."""
        elements = self.__hotel_service.get_elements_by_floor_id(floor_id)
        return [self._to_floor_element_dto(el) for el in elements]

    def get_room_by_id(self, room_id: int) -> RoomDTO:
        """Returns a RoomDTO for the specified room ID."""
        return self._to_room_dto(self.__hotel_service.get_room_by_id(room_id))

    def get_room_by_number(self, room_number: str) -> RoomDTO:
        """Returns a RoomDTO for the specified room number."""
        return self._to_room_dto(self.__hotel_service.get_room_by_number(room_number))

    def get_all_connections(self) -> list[tuple[int, int]]:
        """Returns a list of all connections in the hotel as tuples (floor_id, pos1, pos2)."""
        return self.__hotel_service.get_all_connections()

    def get_rooms_availability_for_date(self, date_string: str) -> tuple[set[int], set[int]]:
        """Returns available and unavailable room IDs for a specific date."""
        available_rooms = set()
        unavailable_rooms = set()
        date_val = self._parse_iso_date(date_string)

        all_reservations = self.get_all_reservations()
        unavailable_room_ids = set()

        for res in all_reservations:
            check_in = res.check_in_date
            check_out = res.check_out_date
            if check_in <= date_val < check_out:
                unavailable_room_ids.add(res.room_id)

        floors = self.get_all_floors()

        for floor in floors:
            floor_grid = self.get_floor_grid(floor.db_id)

            for pos, element in floor_grid.items():
                if not element or element.type != "room":
                    continue
                room_id = element.db_id
                if room_id in unavailable_room_ids:
                    unavailable_rooms.add(room_id)
                else:
                    available_rooms.add(room_id)
        return available_rooms, unavailable_rooms

    def get_floor_number_of_rooms(self, floor_id: int) -> tuple[int, int]:
        """Returns the number of rooms and total reservations on a specific floor."""
        elements = self.__hotel_service.get_elements_by_floor_id(floor_id)
        rooms = [el for el in elements if el.type == 'room']
        nr_of_reservations = 0
        for room in rooms:
            nr_of_reservations += self.get_room_number_of_reservations(room.db_id)
        return len(rooms), nr_of_reservations

    def get_room_number_of_reservations(self, room_id: int) -> int:
        """Returns the number of reservations for a specific room."""
        reservations = self.__reservation_service.get_reservations_by_room_id(room_id)
        return len(reservations)

    def get_available_rooms(self, check_in_date: str, check_out_date: str, number_of_guests: int) -> list[RoomDTO]:
        """Returns a list of available RoomDTOs for the specified date range and number of guests"""
        check_in = self._parse_iso_date(check_in_date)
        check_out = self._parse_iso_date(check_out_date)

        rooms = self.__hotel_service.get_rooms_by_capacity(number_of_guests)
        result: list[RoomDTO] = []

        for room in rooms:
            room_id = room.db_id
            reservations = self.__reservation_service.get_reservations_by_room_id(room_id) # Theta(1)
            is_available = all(
                not (check_in <= res.check_out_date and check_out >= res.check_in_date)
                for res in reservations
            )

            if is_available:
                result.append(self._to_room_dto(room))
        return result

    def get_total_rooms_count(self) -> int:
        """Returns the total number of rooms in the hotel."""
        rooms_count = 0
        floors = self.get_all_floors()

        for floor in floors:
            floor_grid = self.get_floor_grid(floor.db_id)
            for element in floor_grid.values():
                if element and element.type == "room":
                    rooms_count += 1
        return rooms_count

    # Reservations
    def get_reservation_by_id(self, reservation_id: str) -> ReservationDTO:
        """Returns a ReservationDTO for the specified reservation ID."""
        return self._to_reservation_dto(self.__reservation_service.get_by_reservation_id(reservation_id))

    def get_all_reservations(self) -> list[ReservationDTO]:
        """Returns a list of all ReservationDTOs."""
        result = self.__reservation_service.get_all_reservations()
        return [self._to_reservation_dto(res) for res in result]

    def get_total_reservations_income(self) -> float:
        """Calculates the total income from all reservations."""
        total_income = 0
        reservations = self.get_all_reservations()

        for res in reservations:
            room = self.get_room_by_id(res.room_id)
            if room:
                check_in = res.check_in_date
                check_out = res.check_out_date
                days = (check_out - check_in).days
                total_income += days * room.price_per_night
        return total_income

    # Search
    def reservation_search(self, search_bar_string: str, from_date: date = None,
                           to_date: date = None) -> list[ReservationDTO]:
        """Search reservations by reservation ID, guest name, or room number, with optional date filtering."""
        results = []

        rooms = self.__hotel_service.get_rooms_by_partial_number(search_bar_string)
        room_ids = {room.db_id for room in rooms}

        all_reservations = self.__reservation_service.get_all_reservations()
        for reservation in all_reservations:
            if (
                    search_bar_string in reservation.reservation_id
                    or search_bar_string.lower() in reservation.guest_name.lower()
                    or reservation.room_id in room_ids
            ):
                results.append(reservation)

        if from_date:
            results = [res for res in results if res.check_out_date >= from_date]
        if to_date:
            results = [res for res in results if res.check_in_date <= to_date]

        return [self._to_reservation_dto(res) for res in results]

    def reservation_direct_search(self, search_bar_string: str) -> list[ReservationDTO]:
        """Direct search for reservations by reservation ID, guest name, or room number."""
        results = []
        reservation_by_id = self.__reservation_service.get_by_reservation_id(search_bar_string)
        if reservation_by_id:
            results.append(reservation_by_id)
            return [self._to_reservation_dto(res) for res in results]

        all_reservations = self.__reservation_service.get_all_reservations()
        for reservation in all_reservations:
            if search_bar_string.lower() in reservation.guest_name.lower():
                results.append(reservation)

        try:
            room = self.__hotel_service.get_room_by_number(search_bar_string)
            room_id = room.db_id if room else None
        except Exception:
            room_id = None

        if room_id is not None:
            for reservation in all_reservations:
                if reservation.room_id == room_id:
                    results.append(reservation)

        return [self._to_reservation_dto(res) for res in results]

    # CRUD operations

    # Hotel
    def add_floor(self, request):
        """Adds a new floor to the hotel."""
        action = AddFloorAction(self.__hotel_service, request)
        self.__action_manager.do_action(action)

    def rename_floor(self, request):
        """Renames an existing floor in the hotel."""
        action = RenameFloorAction(self.__hotel_service, request)
        self.__action_manager.do_action(action)

    def update_floor_level(self, request):
        """Updates the level of an existing floor in the hotel."""
        action = UpdateFloorLevelAction(self.__hotel_service, request)
        self.__action_manager.do_action(action)

    def remove_floor(self, request):
        """Removes a floor from the hotel."""
        action = RemoveFloorAction(self.__hotel_service, self.__reservation_service, request)
        self.__action_manager.do_action(action)


    def add_element(self, request):
        """Adds a new floor element or room to a floor."""
        action = AddElementAction(self.__hotel_service, request)
        self.__action_manager.do_action(action)

    def edit_room(self, request):
        """Edits the details of an existing room."""
        action = EditRoomAction(self.__hotel_service, request)
        self.__action_manager.do_action(action)

    def move_element(self, request):
        """Moves a floor element or room to a new position on the floor."""
        if not self._is_position_available(request.floor_id, request.position):
            raise ControllerError("Position is already occupied!")
        action = MoveElementAction(self.__hotel_service, request)
        self.__action_manager.do_action(action)

    def remove_element(self, request):
        """Removes a floor element or room from a floor."""
        action = RemoveElementAction(self.__hotel_service, self.__reservation_service, request)
        self.__action_manager.do_action(action)

    # Reservations
    def make_reservation(self, request):
        """Makes a new reservation for a room."""
        if not self._is_room_available(
                request.room_id,
                request.check_in_date,
                request.check_out_date,
                request.number_of_guests
        ):
            raise ControllerError("Room is not available for the selected dates or guest number!")
        action = MakeReservationAction(self.__reservation_service, request)
        self.__action_manager.do_action(action)

    def edit_reservation(self, request):
        """Edits an existing reservation."""
        if not self._is_room_available(
                request.room_id,
                request.check_in_date,
                request.check_out_date,
                request.number_of_guests,
                request.reservation_id
        ):
            raise ControllerError("Room is not available for the selected dates or guest number!")
        action = EditReservationAction(self.__reservation_service, request)
        self.__action_manager.do_action(action)

    def delete_reservation(self, request):
        """Deletes an existing reservation."""
        action = DeleteReservationAction(self.__reservation_service, request)
        self.__action_manager.do_action(action)

    # Utility methods

    # Availability checks
    def _is_position_available(self, floor_id: int, position: tuple[int, int]) -> bool:
        """Checks if a position on a floor is available for placing a new element."""
        elements = self.__hotel_service.get_elements_by_floor_id(floor_id)
        for el in elements:
            if getattr(el, "position", None) == position:
                return False
        return True

    def _is_room_available(self, room_id: int, check_in_date: str, check_out_date: str,
                           number_of_guests: int, reservation_id: str = None):
        """Checks if a room is available for the specified date range and number of guests."""
        check_in = self._parse_iso_date(check_in_date)
        check_out = self._parse_iso_date(check_out_date)

        room = self.__hotel_service.get_room_by_id(room_id)
        if room is None or room.capacity < number_of_guests:
            return False

        reservations = self.__reservation_service.get_reservations_by_room_id(room_id)
        is_available = all(
            (reservation_id is not None and getattr(res, "reservation_id", None) == reservation_id) or
            not (check_in <= res.check_out_date and check_out >= res.check_in_date)
            for res in reservations
        )
        return is_available

    # Parsing
    def _parse_iso_date(self, s: str) -> date:
        """Parses a date string in ISO format (YYYY-MM-DD) and returns a date object."""
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError(f"Invalid date format, expected YYYY-MM-DD: {s}") from e

    # DTO Conversion
    def _to_floor_dto(self, floor) -> FloorDTO:
        """Converts a Floor model instance to a FloorDTO."""
        elements = {el_id: self._to_floor_element_dto(el) if el.type != 'room' else self._to_room_dto(el)
                    for el_id, el in floor.elements.items()}
        return FloorDTO(db_id=floor.db_id, name=floor.name, level=floor.level, elements=elements)

    def _to_floor_element_dto(self, floor_element) -> FloorElementDTO:
        """Converts a FloorElement model instance to a FloorElementDTO."""
        return FloorElementDTO(
            db_id=floor_element.db_id,
            type=floor_element.type,
            floor_id=floor_element.floor_id,
            position=floor_element.position
        )

    def _to_room_dto(self, room) -> RoomDTO:
        """Converts a Room model instance to a RoomDTO."""
        return RoomDTO(
            db_id=room.db_id,
            type=room.type,
            floor_id=room.floor_id,
            position=room.position,
            number=room.number,
            capacity=room.capacity,
            price_per_night=room.price_per_night,
        )

    def _to_reservation_dto(self, reservation) -> ReservationDTO:
        """Converts a Reservation model instance to a ReservationDTO."""
        room = self.__hotel_service.get_room_by_id(reservation.room_id)
        return ReservationDTO(
            reservation_id=reservation.reservation_id,
            room_id=reservation.room_id,
            room_number=room.number,
            guest_name=reservation.guest_name,
            number_of_guests=reservation.number_of_guests,
            check_in_date=reservation.check_in_date,
            check_out_date=reservation.check_out_date,
        )
