from src.utilities.exceptions import RepositoryError
from src.domain.reservation import Reservation
from src.db import reservation_model as db
from datetime import datetime



class ReservationRepository:
    def __init__(self, connection):
        self.__connection = connection

        self.__by_db_id = {}
        self.__by_reservation_id = {}
        self.__by_room_number = {}
        self.__by_guest_name = {}

        self.load_from_db()


    def load_from_db(self):
        reservations = db.get_all_reservations(self.__connection)
        for row in reservations:
            check_in_date = datetime.strptime(row[5], "%Y-%m-%d").date()
            check_out_date = datetime.strptime(row[6], "%Y-%m-%d").date()
            reservation = Reservation(
                db_id=row[0],
                reservation_id=row[1],
                room_number=row[2],
                guest_name=row[3],
                number_of_guests=row[4],
                check_in_date=check_in_date,
                check_out_date=check_out_date,
            )
            self.add_to_cache(reservation)


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
        self.__by_db_id.pop(reservation.db_id)
        self.__by_reservation_id.pop(reservation.reservation_id)

        self.__by_room_number[reservation.room_number].remove(reservation)
        self.__by_guest_name[reservation.guest_name].remove(reservation)


    def add_reservation(self, reservation: Reservation):
        db.add_reservation(
            self.__connection,
            reservation.reservation_id,
            reservation.room_number,
            reservation.guest_name,
            reservation.number_of_guests,
            reservation.check_in_date,
            reservation.check_out_date,
        )

        new_db_row = db.get_reservation_by_reservation_id(self.__connection, reservation.reservation_id)
        reservation.db_id = new_db_row[0]
        self.add_to_cache(reservation)

    def get_by_reservation_id(self, reservation_id):
        return self.__by_reservation_id.get(reservation_id)

    def get_by_room_number(self, room_nr):
        return self.__by_room_number.get(room_nr)

    def get_by_guest_name(self, guest_name):
        return self.__by_guest_name.get(guest_name)

    def update_reservation(self, reservation: Reservation):
        db.update_reservation(
            self.__connection,
            reservation.db_id,
            reservation.reservation_id,
            reservation.room_number,
            reservation.guest_name,
            reservation.number_of_guests,
            reservation.check_in_date,
            reservation.check_out_date,
        )
        self.remove_from_cache(reservation)
        self.add_to_cache(reservation)

    def delete_reservation(self, reservation_id: str):
        reservation = self.__by_reservation_id.get(reservation_id)
        db.delete_reservation(self.__connection, reservation.db_id)
        self.remove_from_cache(reservation)
