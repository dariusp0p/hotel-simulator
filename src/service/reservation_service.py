from datetime import datetime, date
from random import randint

from src.repository.reservation_repository import ReservationRepository
from src.utilities.exceptions import ValidationError
from src.domain.reservation import Reservation



class ReservationService:
    def __init__(self, reservation_repository: ReservationRepository):
        self.__repository = reservation_repository


    # Getters
    def get_all_reservations(self):
        return self.__repository.get_all_reservations()

    def get_by_reservation_id(self, reservation_id):
        return self.__repository.get_by_reservation_id(reservation_id)

    def get_reservations_by_room_id(self, room_id):
        return self.__repository.get_reservations_by_room_id(room_id)


    # Searches
    def search(self, search_bar_string, from_date, to_date):
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

    def direct_search(self, search_bar_string):
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


    # ---- CRUD Operations ----

    def make_reservation(self, reservation_id=None, room_id=None, guest_name=None, number_of_guests=None,
                         check_in_date=None, check_out_date=None) -> str | None:
        if not reservation_id:
            reservation_id = self._generate_reservation_id(room_id, check_in_date, check_out_date)
        reservation = Reservation(
            reservation_id=reservation_id,
            room_id=room_id, guest_name=guest_name, number_of_guests=number_of_guests,
            check_in_date=self._parse_iso_date(check_in_date),
            check_out_date=self._parse_iso_date(check_out_date)
        )

        errors = reservation.validate()
        if errors:
            raise ValidationError('Invalid Reservation!', errors)

        self.__repository.add_reservation(reservation)
        return reservation_id

    def update_reservation(self, reservation_id, room_id, guest_name, number_of_guests,
                           check_in_date, check_out_date) -> None:
        reservation = Reservation(
            reservation_id=reservation_id,
            room_id=room_id, guest_name=guest_name, number_of_guests=number_of_guests,
            check_in_date=self._parse_iso_date(check_in_date),
            check_out_date=self._parse_iso_date(check_out_date),
        )

        errors = reservation.validate()
        if errors:
            raise ValidationError('Invalid Reservation!', errors)

        self.__repository.update_reservation(reservation)

    def delete_reservation(self, reservation_id: str) -> None:
        self.__repository.delete_reservation(reservation_id)


    # ---- Utilities ----

    def _generate_reservation_id(self, room_id, check_in_date, check_out_date):
        room_id = str(room_id).zfill(3)
        year = str(datetime.strptime(check_in_date, "%Y-%m-%d").year)[-2:]
        month = datetime.strptime(check_in_date, "%Y-%m-%d").strftime("%m")
        check_in_day = datetime.strptime(check_in_date, "%Y-%m-%d").strftime("%d")
        check_out_day = datetime.strptime(check_out_date, "%Y-%m-%d").strftime("%d")
        code = str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))

        reservation_id = "R" + room_id + year + month + check_in_day + check_out_day + code
        return reservation_id

    def _parse_iso_date(self, s: str) -> date:
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError(f"Invalid date format, expected YYYY-MM-DD: {s}") from e

