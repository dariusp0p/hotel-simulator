from datetime import datetime, date
from random import randint

from src.model.repository.reservation_repository import ReservationRepository
from src.utilities.exceptions import ValidationError
from src.model.domain.reservation import Reservation


class ReservationService:
    """
    Service layer for managing reservations, providing business logic and validation.
    """

    def __init__(self, reservation_repository: ReservationRepository):
        self.__repository = reservation_repository

    # Getters
    def get_all_reservations(self) -> list[Reservation]:
        """Returns all reservations."""
        return self.__repository.get_all_reservations()

    def get_by_reservation_id(self, reservation_id: str) -> Reservation | None:
        """Returns the reservation with the given reservation ID."""
        return self.__repository.get_by_reservation_id(reservation_id)

    def get_reservations_by_room_id(self, room_id: int) -> list[Reservation]:
        """Returns all reservations for the given room ID."""
        return self.__repository.get_reservations_by_room_id(room_id)

    # Searches
    def search(self, search_bar_string: str, from_date: date = None, to_date: date = None) -> list[Reservation]:
        """Performs a flexible search for reservations based on a search string and optional date range."""
        results = []
        for reservation in self.__repository.get_all_reservations():
            if (search_bar_string in reservation.reservation_id
                    or search_bar_string.lower() in reservation.guest_name.lower()):
                results.append(reservation)

        if from_date:
            filtered_results = [
                res for res in results
                if res.check_out_date >= from_date
            ]
            results = filtered_results
        if to_date:
            filtered_results = [
                res for res in results
                if res.check_in_date <= to_date
            ]
            results = filtered_results

        return results

    def direct_search(self, search_bar_string: str) -> list[Reservation]:
        """Performs a direct search for reservations based on reservation ID or guest name."""
        results = []

        reservation_by_id = self.__repository.get_by_reservation_id(search_bar_string)
        if reservation_by_id:
            results.append(reservation_by_id)
            return results

        reservations_by_guest_name = self.__repository.get_reservations_by_guest_name(search_bar_string)
        if reservations_by_guest_name:
            results.extend(reservations_by_guest_name)
            return results

        # reservations_by_room_id = self.__repository.get_reservations_by_room_id(search_bar_string)
        # if reservations_by_room_id:
        #     results.extend(reservations_by_room_id)
        #     return results

        return results

    # CRUD operations
    def make_reservation(self, room_id: int, guest_name: str, number_of_guests: int,
                         check_in_date: str, check_out_date: str, reservation_id: str = None) -> str | None:
        """Creates a new reservation with the provided details. If reservation_id is not provided,"""
        if reservation_id is None:
            reservation_id = self._generate_reservation_id(room_id, check_in_date, check_out_date)

        reservation = Reservation(
            reservation_id=reservation_id, room_id=room_id,
            guest_name=guest_name, number_of_guests=number_of_guests,
            check_in_date=self._parse_iso_date(check_in_date),
            check_out_date=self._parse_iso_date(check_out_date)
        )

        errors = reservation.validate()
        if errors:
            raise ValidationError('Invalid Reservation!', errors)

        self.__repository.add_reservation(reservation)
        return reservation_id

    def update_reservation(self, reservation_id: str, room_id: int, guest_name: str,
                           number_of_guests: int, check_in_date: str, check_out_date: str) -> None:
        """Updates an existing reservation with the provided details."""
        reservation = Reservation(
            reservation_id=reservation_id, room_id=room_id,
            guest_name=guest_name, number_of_guests=number_of_guests,
            check_in_date=self._parse_iso_date(check_in_date),
            check_out_date=self._parse_iso_date(check_out_date),
        )

        errors = reservation.validate()
        if errors:
            raise ValidationError('Invalid Reservation!', errors)

        self.__repository.update_reservation(reservation_id=reservation_id, room_id=room_id,
                                             guest_name=guest_name, number_of_guests=number_of_guests,
                                             check_in_date=check_in_date, check_out_date=check_out_date)

    def delete_reservation(self, reservation_id: str) -> Reservation:
        """Deletes the reservation with the given reservation ID."""
        return self.__repository.delete_reservation(reservation_id)

    # Utility methods
    def _generate_reservation_id(self, room_id: int, check_in_date: str, check_out_date: str) -> str:
        """Generates a unique reservation ID based on room ID, check-in and check-out dates, and a random code."""
        room_id = str(room_id).zfill(3)
        year = str(datetime.strptime(check_in_date, "%Y-%m-%d").year)[-2:]
        month = datetime.strptime(check_in_date, "%Y-%m-%d").strftime("%m")
        check_in_day = datetime.strptime(check_in_date, "%Y-%m-%d").strftime("%d")
        check_out_day = datetime.strptime(check_out_date, "%Y-%m-%d").strftime("%d")
        code = str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))

        reservation_id = "R" + room_id + year + month + check_in_day + check_out_day + code
        return reservation_id

    def _parse_iso_date(self, s: str) -> date | None:
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError(f"Invalid date format, expected YYYY-MM-DD: {s}") from e
