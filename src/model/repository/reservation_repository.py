import sqlite3
from datetime import datetime

from src.utilities.exceptions import (ReservationAlreadyExistsError, ReservationNotFoundError)
from src.model.domain.reservation import Reservation
from src.model.database import database_operations as db


class ReservationRepository:
    """
    Repository for managing Reservation entities with in-memory caching and SQLite persistence.
    """

    def __init__(self, connection: sqlite3.Connection):
        self.__connection = connection

        self.__by_reservation_id = {}
        self.__by_room_id = {}
        self.__by_guest_name = {}

        self.load_from_db()

    @property
    def connection(self) -> sqlite3.Connection:
        return self.__connection

    # Data persistence
    def load_from_db(self):
        """Load all reservations from the database into the in-memory cache. Theta(n) complexity."""
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

    def add_to_cache(self, reservation: Reservation):
        """Add a reservation to the in-memory cache. Theta(1) complexity."""
        self.__by_reservation_id[reservation.reservation_id] = reservation

        if reservation.room_id not in self.__by_room_id:
            self.__by_room_id[reservation.room_id] = []
        self.__by_room_id[reservation.room_id].append(reservation)

        if reservation.guest_name not in self.__by_guest_name:
            self.__by_guest_name[reservation.guest_name] = []
        self.__by_guest_name[reservation.guest_name].append(reservation)

    def remove_from_cache(self, reservation: Reservation):
        """Remove a reservation from the in-memory cache. Theta(1) complexity."""
        self.__by_reservation_id.pop(reservation.reservation_id, None)

        room_reservations = self.__by_room_id.get(reservation.room_id)
        if room_reservations:
            room_reservations = [r for r in room_reservations if r != reservation]
            if room_reservations:
                self.__by_room_id[reservation.room_id] = room_reservations
            else:
                del self.__by_room_id[reservation.room_id]

        name_resevations = self.__by_guest_name.get(reservation.guest_name)
        if name_resevations:
            name_resevations = [r for r in name_resevations if r != reservation]
            if name_resevations:
                self.__by_guest_name[reservation.guest_name] = name_resevations
            else:
                del self.__by_guest_name[reservation.guest_name]

    # Getters
    def get_all_reservations(self) -> list[Reservation]:
        """Return a list of all reservations. Theta(n) complexity."""
        return list(self.__by_reservation_id.values())

    def get_by_reservation_id(self, reservation_id: str) -> Reservation | None:
        """Return a reservation by its reservation_id. Theta(1) complexity."""
        return self.__by_reservation_id.get(reservation_id)

    def get_reservations_by_room_id(self, room_id: int) -> list[Reservation]:
        """Return a list of reservations for a specific room_id. Theta(1) complexity."""
        return self.__by_room_id.get(room_id, [])

    def get_reservations_by_guest_name(self, guest_name: str) -> list[Reservation]:
        """Return a list of reservations for a specific guest_name. Theta(1) complexity."""
        return self.__by_guest_name.get(guest_name, [])

    # CRUD operations
    def add_reservation(self, reservation: Reservation):
        """Add a new reservation to the repository and persist it to the database. Theta(1) complexity."""
        if reservation.reservation_id in self.__by_reservation_id:
            raise ReservationAlreadyExistsError(f"Reservation with ID {reservation.reservation_id} already exists!")

        reservation.db_id = db.insert_reservation(
            self.__connection,
            reservation.reservation_id, reservation.room_id,
            reservation.guest_name, reservation.number_of_guests,
            reservation.check_in_date.isoformat(), reservation.check_out_date.isoformat(),
        )
        self.add_to_cache(reservation)

    def update_reservation(self, reservation_id: str, **kwargs):
        """Update an existing reservation in the repository and the database. Theta(1) complexity."""
        reservation = self.__by_reservation_id.get(reservation_id)
        if reservation is None:
            raise ReservationNotFoundError(f"Reservation with id {reservation_id} does not exist!")

        self.remove_from_cache(reservation)
        for key, value in kwargs.items():
            if hasattr(reservation, key):
                setattr(reservation, key, value)

        db.update_reservation(
            self.__connection,
            reservation.db_id,
            reservation.reservation_id,
            reservation.room_id,
            reservation.guest_name,
            reservation.number_of_guests,
            reservation.check_in_date.isoformat(),
            reservation.check_out_date.isoformat(),
        )
        self.add_to_cache(reservation)

    def delete_reservation(self, reservation_id: str):
        """Delete a reservation from the repository and the database. Theta(1) complexity."""
        reservation = self.__by_reservation_id.get(reservation_id)
        if reservation is None:
            raise ReservationNotFoundError(f"Reservation with id {reservation_id} does not exist!")

        db.delete_reservation(self.__connection, reservation.db_id)
        self.remove_from_cache(reservation)
