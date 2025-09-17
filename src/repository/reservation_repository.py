import sqlite3
from datetime import datetime
from webbrowser import Error

from src.utilities.exceptions import (RepositoryError, ReservationAlreadyExistsError, ReservationNotFoundError, DatabaseUnavailableError)
from src.domain.reservation import Reservation
from src.db import reservation_model as db



class ReservationRepository:
    def __init__(self, connection):
        self.__connection = connection

        self.__by_db_id = {}
        self.__by_reservation_id = {}
        self.__by_room_id = {}
        self.__by_guest_name = {}

        self.load_from_db()


    @property
    def connection(self):
        return self.__connection


    # Data persistence
    def load_from_db(self):
        try:
            reservations = db.select_all_reservations(self.__connection)
            for row in reservations:
                reservation = Reservation(
                    db_id=row[0],
                    reservation_id=row[1],
                    room_id=row[2],
                    guest_name=row[3],
                    number_of_guests=row[4],
                    check_in_date=datetime.strptime(row[5], "%Y-%m-%d").date(),
                    check_out_date=datetime.strptime(row[6], "%Y-%m-%d").date(),
                )
                self.add_to_cache(reservation)
        except sqlite3.OperationalError:
            raise DatabaseUnavailableError("Database is unavailable or corrupted.")
        except Error:
            raise RepositoryError("An error occurred while loading reservations from the database.")


    def add_to_cache(self, reservation: Reservation):
        self.__by_db_id[reservation.db_id] = reservation
        self.__by_reservation_id[reservation.reservation_id] = reservation

        if reservation.room_id not in self.__by_room_id:
            self.__by_room_id[reservation.room_id] = []
        self.__by_room_id[reservation.room_id].append(reservation)

        if reservation.guest_name not in self.__by_guest_name:
            self.__by_guest_name[reservation.guest_name] = []
        self.__by_guest_name[reservation.guest_name].append(reservation)

    def remove_from_cache(self, reservation: Reservation):
        self.__by_db_id.pop(reservation.db_id, None)
        self.__by_reservation_id.pop(reservation.reservation_id, None)

        if reservation.room_id in self.__by_room_id:
            try:
                self.__by_room_id[reservation.room_id].remove(reservation)
                if not self.__by_room_id[reservation.room_id]:
                    del self.__by_room_id[reservation.room_id]
            except ValueError:
                pass

        if reservation.guest_name in self.__by_guest_name:
            try:
                self.__by_guest_name[reservation.guest_name].remove(reservation)
                if not self.__by_guest_name[reservation.guest_name]:
                    del self.__by_guest_name[reservation.guest_name]
            except ValueError:
                pass


    # Getters
    def get_all_reservations(self):
        return list(self.__by_reservation_id.values())

    def get_by_reservation_id(self, reservation_id):
        return self.__by_reservation_id.get(reservation_id)

    def get_reservations_by_room_id(self, room_id):
        return self.__by_room_id.get(room_id, [])

    def get_reservations_by_guest_name(self, guest_name):
        return self.__by_guest_name.get(guest_name, [])


    # CRUD
    def add_reservation(self, reservation: Reservation):
        try:
            db.insert_reservation(
                self.__connection,
                reservation.reservation_id,
                reservation.room_id,
                reservation.guest_name,
                reservation.number_of_guests,
                reservation.check_in_date.isoformat(),
                reservation.check_out_date.isoformat(),
            )

            new_db_row = db.select_reservation_by_reservation_id(self.__connection, reservation.reservation_id)
            reservation.db_id = new_db_row[0]
            self.add_to_cache(reservation)
        except sqlite3.IntegrityError:
            raise ReservationAlreadyExistsError(f"Reservation with id {reservation.reservation_id} already exists.")
        except sqlite3.OperationalError:
            raise DatabaseUnavailableError("Database is unavailable or corrupted.")
        except Exception:
            raise RepositoryError("An error occurred while adding the reservation.")

    def update_reservation(self, reservation: Reservation):
        old_reservation = self.__by_reservation_id.get(reservation.reservation_id)
        if old_reservation is None:
            raise ReservationNotFoundError(f"Reservation with id {reservation.reservation_id} does not exist.")
        try:
            db.update_reservation(
                self.__connection,
                old_reservation.db_id,
                reservation.reservation_id,
                reservation.room_id,
                reservation.guest_name,
                reservation.number_of_guests,
                reservation.check_in_date.isoformat(),
                reservation.check_out_date.isoformat(),
            )
            self.remove_from_cache(old_reservation)
            self.add_to_cache(reservation)
        except sqlite3.OperationalError:
            raise DatabaseUnavailableError("Database is unavailable or corrupted.")
        except Exception:
            raise RepositoryError("An error occurred while updating the reservation.")

    def delete_reservation(self, reservation_id: str):
        reservation = self.__by_reservation_id.get(reservation_id)
        if reservation is None:
            raise ReservationNotFoundError(f"Reservation with id {reservation_id} does not exist.")
        try:
            db.delete_reservation(self.__connection, reservation.db_id)
            self.remove_from_cache(reservation)
        except sqlite3.OperationalError:
            raise DatabaseUnavailableError("Database is unavailable or corrupted.")
        except Exception:
            raise RepositoryError("An error occurred while deleting reservation.")
