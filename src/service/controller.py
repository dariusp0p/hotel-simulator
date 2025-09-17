from datetime import datetime, date
from src.service.dto import FloorDTO, FloorElementDTO, RoomDTO, ReservationDTO



class Controller:
    def __init__(self, reservation_service, hotel_service):
        self.__reservation_service = reservation_service
        self.__hotel_service = hotel_service


    # GETTERS

    # Reservation
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

    # Hotel
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

    def is_room_available(self, room_id, arrival_date, departure_date, number_of_guests):
        arrival = self._parse_iso_date(arrival_date)
        departure = self._parse_iso_date(departure_date)

        room = self.__hotel_service.get_room_by_id(room_id)
        if room is None or room.capacity < number_of_guests:
            return False

        reservations = self.__reservation_service.get_reservations_by_room_id(room_id)
        is_available = all(
            not (arrival <= res.check_out_date and departure >= res.check_in_date)
            for res in reservations
        )
        return is_available

    def get_all_floors(self):
        result = self.__hotel_service.get_all_floors_sorted_by_level()
        return [self._to_floor_dto(floor) for floor in result]

    def get_floor_grid(self, floor_name):
        grid = self.__hotel_service.get_floor_grid(floor_name)
        dto_grid = {}
        for position, element in grid.items():
            if element is None:
                dto_grid[position] = None
            elif element.type == 'room':
                dto_grid[position] = self._to_room_dto(element)
            else:
                dto_grid[position] = self._to_floor_element_dto(element)
        return dto_grid

    def get_floor_connections(self, floor_name):
        return self.__hotel_service.get_floor_connections(floor_name)

    def get_floor_elements(self, floor_id):
        elements = self.__hotel_service.get_elements_by_floor_id(floor_id)
        return [self._to_floor_element_dto(el) for el in elements]

    def get_room_by_id(self, room_id):
        return self._to_room_dto(self.__hotel_service.get_room_by_id(room_id))

    def get_room_by_number(self, room_number):
        return self._to_room_dto(self.__hotel_service.get_room_by_number(room_number))

    def get_all_connections(self):
        return self.__hotel_service.get_all_connections()


    # CRUD

    # Reservation
    def make_reservation(self, room_id, guest_name, guest_number, arrival_date, departure_date):
        reservation_data = {
            "room_id": room_id,
            "guest_name": guest_name,
            "number_of_guests": guest_number,
            "check_in_date": arrival_date,
            "check_out_date": departure_date,
        }
        try:
            self.__reservation_service.make_reservation(reservation_data)
        except Exception as e:
            raise e

    def update_reservation(self, reservation_id, room_id, guest_name, guest_number, arrival_date, departure_date):
        reservation_data = {
            "reservation_id": reservation_id,
            "room_id": room_id,
            "guest_name": guest_name,
            "number_of_guests": guest_number,
            "check_in_date": arrival_date,
            "check_out_date": departure_date,
        }
        try:
            self.__reservation_service.update_reservation(reservation_data)
        except Exception as e:
            raise e

    def delete_reservation(self, reservation_id):
        try:
            self.__reservation_service.delete_reservation(reservation_id)
        except Exception as e:
            raise e


    # Hotel
    def add_floor(self, floor_name, level=0):
        try:
            self.__hotel_service.add_floor(floor_name, level)
        except Exception as e:
            raise e

    def rename_floor(self, old_name, new_name):
        try:
            self.__hotel_service.rename_floor(old_name, new_name)
        except Exception as e:
            raise e

    def update_floor_level(self, floor_id, new_level):
        try:
            self.__hotel_service.update_floor_level(floor_id, new_level)
        except Exception as e:
            raise e

    def remove_floor(self, floor_id):
        try:
            elements = self.__hotel_service.get_elements_by_floor_id(floor_id)
            for element in elements:
                self.__hotel_service.remove_element(element)
            self.__hotel_service.remove_floor(floor_id)
        except Exception as e:
            raise e



    def add_element(self, element_data):
        try:
            self.__hotel_service.add_element(element_data)
        except Exception as e:
            raise e




    # --- HELPER METHODS ---

    # Parsing
    def _parse_iso_date(self, s: str) -> date:
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError(f"Invalid date format, expected YYYY-MM-DD: {s}") from e

    # DTO Conversion
    def _to_floor_dto(self, floor) -> FloorDTO:
        return FloorDTO(db_id=floor.db_id, name=floor.name, level=floor.level)

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
