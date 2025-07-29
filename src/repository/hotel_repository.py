import sqlite3

from src.domain.floor import Floor
from src.domain.floor_element import FloorElement
from src.db import hotel_model as db



class HotelRepository:
    def __init__(self, connection):
        self.__connection = connection

        self.__floors = {} # key: floor name | value: floor object
        # floor object: - set of FloorElement objects - key: coordinates | value: FloorElement object

        self.load_from_db()


    @property
    def connection(self):
        return self.__connection


    def load_from_db(self):
        floors = db.get_all_floors(self.__connection)

        for floor in floors:
            floor_obj = Floor(floor)
            elements = db.get_elements_from_floor(self.__connection, floor)
            for row in elements:
                floor_element = FloorElement(
                    element_id=row[0],
                    element_type=row[1],
                    floor_name=row[2],
                    capacity=row[3],
                    position=(row[4], row[5])
                )
                floor_obj.add_element(floor_element)
            self.__floors[floor] = floor_obj



    def save(self, hotel: Hotel):
        db.save_hotel(self.__connection, hotel)

    def get(self, hotel_name="Default Hotel") -> Hotel:
        return db.load_hotel(self.__connection, hotel_name)

    def delete(self, hotel_name):
        db.delete_hotel(self.__connection, hotel_name)









    def add_to_cache(self, reservation: Reservation):
        self.__by_db_id[reservation.db_id] = reservation
        self.__by_reservation_id[reservation.reservation_id] = reservation

        if reservation.room_number not in self.__by_room_number:
            self.__by_room_number[reservation.room_number] = []
        self.__by_room_number[reservation.room_number].append(reservation)

        if reservation.guest_name not in self.__by_guest_name:
            self.__by_guest_name[reservation.guest_name] = []
        self.__by_guest_name[reservation.guest_name].append(reservation)

    def remove_from_cache(self, reservation: Reservation):
        self.__by_db_id.pop(reservation.db_id, None)
        self.__by_reservation_id.pop(reservation.reservation_id, None)

        if reservation.room_number in self.__by_room_number:
            try:
                self.__by_room_number[reservation.room_number].remove(reservation)
                if not self.__by_room_number[reservation.room_number]:
                    del self.__by_room_number[reservation.room_number]
            except ValueError:
                pass

        if reservation.guest_name in self.__by_guest_name:
            try:
                self.__by_guest_name[reservation.guest_name].remove(reservation)
                if not self.__by_guest_name[reservation.guest_name]:
                    del self.__by_guest_name[reservation.guest_name]
            except ValueError:
                pass


    def add_reservation(self, reservation: Reservation):
        try:
            db.add_reservation(
                self.__connection,
                reservation.reservation_id,
                reservation.room_number,
                reservation.guest_name,
                reservation.number_of_guests,
                reservation.check_in_date.isoformat(),
                reservation.check_out_date.isoformat(),
            )

            new_db_row = db.get_reservation_by_reservation_id(self.__connection, reservation.reservation_id)
            reservation.db_id = new_db_row[0]
            self.add_to_cache(reservation)
        except sqlite3.IntegrityError:
            raise ReservationAlreadyExistsError(f"Reservation with id {reservation.reservation_id} already exists.")
        except sqlite3.OperationalError:
            raise DatabaseUnavailableError("Database is unavailable or corrupted.")

    def get_all_reservations(self):
        return list(self.__by_reservation_id.values())

    def get_by_reservation_id(self, reservation_id):
        return self.__by_reservation_id.get(reservation_id)

    def get_by_room_number(self, room_nr):
        return self.__by_room_number.get(room_nr)

    def get_by_guest_name(self, guest_name):
        return self.__by_guest_name.get(guest_name)


    def update_reservation(self, reservation: Reservation):
        old_reservation = self.__by_reservation_id.get(reservation.reservation_id)
        if old_reservation is None:
            raise ReservationNotFoundError(f"Reservation with id {reservation.reservation_id} does not exist.")
        try:
            db.update_reservation(
                self.__connection,
                reservation.db_id,
                reservation.reservation_id,
                reservation.room_number,
                reservation.guest_name,
                reservation.number_of_guests,
                reservation.check_in_date.isoformat(),
                reservation.check_out_date.isoformat(),
            )
            self.remove_from_cache(old_reservation)
            self.add_to_cache(reservation)
        except sqlite3.OperationalError:
            raise DatabaseUnavailableError("Database is unavailable or corrupted.")


    def delete_reservation(self, reservation_id: str):
        reservation = self.__by_reservation_id.get(reservation_id)
        if reservation is None:
            raise ReservationNotFoundError(f"Reservation with id {reservation_id} does not exist.")
        try:
            db.delete_reservation(self.__connection, reservation.db_id)
            self.remove_from_cache(reservation)
        except sqlite3.OperationalError:
            raise DatabaseUnavailableError("Database is unavailable or corrupted.")
