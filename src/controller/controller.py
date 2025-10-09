from datetime import datetime, date
from src.controller.dto import FloorDTO, FloorElementDTO, RoomDTO, ReservationDTO
from src.utilities.exceptions import ServiceError, ControllerError
from src.controller.action_manager import ActionManager
from src.controller.action import (
    AddFloorAction, RemoveFloorAction, AddElementAction, RemoveElementAction,
    EditRoomAction, MoveElementAction, MakeReservationAction, EditReservationAction, DeleteReservationAction,
    UpdateFloorLevelAction, RenameFloorAction
)


class Controller:
    def __init__(self, reservation_service, hotel_service):
        self.__reservation_service = reservation_service
        self.__hotel_service = hotel_service
        self.__action_manager = ActionManager()


    # ---- Undo / Redo ----

    def undo(self):
        self.__action_manager.undo()

    def redo(self):
        self.__action_manager.redo()

    def can_undo(self):
        return self.__action_manager.can_undo()

    def can_redo(self):
        return self.__action_manager.can_redo()


    # ---- Getters ----

    def get_reservation_by_id(self, reservation_id):
        return self._to_reservation_dto(self.__reservation_service.get_by_reservation_id(reservation_id))

    def get_all_reservations(self):
        result = self.__reservation_service.get_all_reservations()
        return [self._to_reservation_dto(res) for res in result]

    def reservation_search(self, search_bar_string=None, from_date=None, to_date=None):
        result = self.__reservation_service.search(search_bar_string, from_date, to_date)
        return [self._to_reservation_dto(res) for res in result]

    def reservation_direct_search(self, search_bar_string):
        result = self.__reservation_service.direct_search(search_bar_string)
        return [self._to_reservation_dto(res) for res in result]


    def get_available_rooms(self, arrival_date, departure_date, number_of_guests):
        arrival = self._parse_iso_date(arrival_date)
        departure = self._parse_iso_date(departure_date)

        rooms = self.__hotel_service.get_rooms_by_capacity(number_of_guests)
        result: list[RoomDTO] = []

        for room in rooms:
            room_id = room.db_id
            reservations = self.__reservation_service.get_reservations_by_room_id(room_id) # Theta(1)
            is_available = all(
                not (arrival <= res.check_out_date and departure >= res.check_in_date)
                for res in reservations
            )

            if is_available:
                result.append(self._to_room_dto(room))
        return result

    def get_floor(self, floor_id):
        return self._to_floor_dto(self.__hotel_service.get_floor(floor_id))

    def get_all_floors(self):
        result = self.__hotel_service.get_all_floors_sorted_by_level()
        return [self._to_floor_dto(floor) for floor in result]

    def get_floor_grid(self, floor_id):
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

    def get_floor_connections(self, floor_id):
        return self.__hotel_service.get_floor_connections(floor_id)

    def get_floor_elements(self, floor_id):
        elements = self.__hotel_service.get_elements_by_floor_id(floor_id)
        return [self._to_floor_element_dto(el) for el in elements]

    def get_room_by_id(self, room_id):
        return self._to_room_dto(self.__hotel_service.get_room_by_id(room_id))

    def get_room_by_number(self, room_number):
        return self._to_room_dto(self.__hotel_service.get_room_by_number(room_number))

    def get_all_connections(self):
        return self.__hotel_service.get_all_connections()

    def get_rooms_availability_for_date(self, date_string):
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

    def get_total_rooms_count(self):
        """Returns the total number of rooms in the hotel."""
        rooms_count = 0
        floors = self.get_all_floors()

        for floor in floors:
            floor_grid = self.get_floor_grid(floor.db_id)
            for element in floor_grid.values():
                if element and element.type == "room":
                    rooms_count += 1

        return rooms_count

    def get_total_reservations_income(self):
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

    # ---- CRUD ----

    # Reservations

    def make_reservation(self, request):
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
        action = DeleteReservationAction(self.__reservation_service, request)
        self.__action_manager.do_action(action)


    def _is_room_available(self, room_id, check_in_date, check_out_date, number_of_guests, reservation_id=None):
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


    # Floors

    def add_floor(self, request):
        action = AddFloorAction(self.__hotel_service, request)
        self.__action_manager.do_action(action)

    def rename_floor(self, request):
        action = RenameFloorAction(self.__hotel_service, request)
        self.__action_manager.do_action(action)

    def update_floor_level(self, request):
        action = UpdateFloorLevelAction(self.__hotel_service, request)
        self.__action_manager.do_action(action)

    def remove_floor(self, request):
        action = RemoveFloorAction(self.__hotel_service, self.__reservation_service, request)
        self.__action_manager.do_action(action)


    # Floor Elements

    def add_element(self, request):
        action = AddElementAction(self.__hotel_service, request)
        self.__action_manager.do_action(action)

    def edit_room(self, request):
        action = EditRoomAction(self.__hotel_service, request)
        self.__action_manager.do_action(action)

    def move_element(self, request):
        if not self._is_position_available(request.floor_id, request.position):
            raise ControllerError("Position is already occupied!")
        action = MoveElementAction(self.__hotel_service, request)
        self.__action_manager.do_action(action)

    def remove_element(self, request):
        action = RemoveElementAction(self.__hotel_service, self.__reservation_service, request)
        self.__action_manager.do_action(action)


    def _is_position_available(self, floor_id, position):
        elements = self.__hotel_service.get_elements_by_floor_id(floor_id)
        for el in elements:
            if getattr(el, "position", None) == position:
                return False
        return True


    def get_floor_number_of_rooms(self, floor_id):
        elements = self.__hotel_service.get_elements_by_floor_id(floor_id)
        rooms = [el for el in elements if el.type == 'room']
        nr_of_reservations = 0
        for room in rooms:
            nr_of_reservations += self.get_room_number_of_reservations(room.db_id)
        return len(rooms), nr_of_reservations

    def get_room_number_of_reservations(self, room_id):
        reservations = self.__reservation_service.get_reservations_by_room_id(room_id)
        return len(reservations)



    # --- HELPER METHODS ---

    # Parsing
    def _parse_iso_date(self, s: str) -> date:
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError(f"Invalid date format, expected YYYY-MM-DD: {s}") from e

    # DTO Conversion
    def _to_floor_dto(self, floor) -> FloorDTO:
        elements = {el_id: self._to_floor_element_dto(el) if el.type != 'room' else self._to_room_dto(el)
                    for el_id, el in floor.elements.items()}
        return FloorDTO(db_id=floor.db_id, name=floor.name, level=floor.level, elements=elements)

    def _to_floor_element_dto(self, floor_element) -> FloorElementDTO:
        return FloorElementDTO(
            db_id=floor_element.db_id,
            type=floor_element.type,
            floor_id=floor_element.floor_id,
            position=floor_element.position
        )

    def _to_room_dto(self, room) -> RoomDTO:
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
