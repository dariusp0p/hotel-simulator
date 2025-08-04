from datetime import datetime
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

    def get_reservations_by_guest_name(self, guest_name):
        return self.__repository.get_reservations_by_guest_name(guest_name)

    def get_reservations_by_room_number(self, room_number):
        return self.__repository.get_reservations_by_room_number(room_number)


    # Searches
    def search(self, search_bar_string, from_date, to_date):
        results = []

        for reservation in self.__repository.get_all_reservations():
            if search_bar_string in reservation.reservation_id or search_bar_string.lower() in reservation.guest_name.lower() or search_bar_string.lower() in reservation.room_number.lower():
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

        reservations_by_room_number = self.__repository.get_reservations_by_room_number(search_bar_string)
        if reservations_by_room_number:
            results.extend(reservations_by_room_number)
            return results

        return results



    # CRUD
    def make_reservation(self, reservation_data: dict) -> None:
        reservation = Reservation(
            reservation_id=self.generate_reservation_id(reservation_data),
            room_number=reservation_data['room_number'],
            guest_name=reservation_data['guest_name'],
            number_of_guests=reservation_data['number_of_guests'],
            check_in_date=datetime.strptime(reservation_data['check_in_date'], "%Y-%m-%d").date(),
            check_out_date=datetime.strptime(reservation_data['check_out_date'], "%Y-%m-%d").date(),
        )

        errors = reservation.validate()
        if errors:
            raise ValidationError('Invalid Reservation!', errors)

        try:
            self.__repository.add_reservation(reservation)
        except Exception as e:
            raise e

    def update_reservation(self, reservation_data: dict) -> None:
        reservation = Reservation(
            reservation_id=reservation_data['reservation_id'],
            room_number=reservation_data['room_number'],
            guest_name=reservation_data['guest_name'],
            number_of_guests=reservation_data['number_of_guests'],
            check_in_date=datetime.strptime(reservation_data['check_in_date'], "%Y-%m-%d").date(),
            check_out_date=datetime.strptime(reservation_data['check_out_date'], "%Y-%m-%d").date(),
        )

        try:
            self.__repository.update_reservation(reservation)
        except Exception as e:
            raise e

    def delete_reservation(self, reservation_id: str) -> None:
        try:
            return self.__repository.delete_reservation(reservation_id)
        except Exception as e:
            raise e


    # Utilities
    def generate_reservation_id(self, reservation_data):
        year = str(datetime.strptime(reservation_data['check_in_date'], "%Y-%m-%d").year)[-2:]
        month = datetime.strptime(reservation_data['check_in_date'], "%Y-%m-%d").strftime("%m")
        check_in_day = datetime.strptime(reservation_data['check_in_date'], "%Y-%m-%d").strftime("%d")
        check_out_day = datetime.strptime(reservation_data['check_out_date'], "%Y-%m-%d").strftime("%d")

        code = str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))
        reservation_id = "R" + reservation_data['room_number'] + year + month + check_in_day + check_out_day + code
        return reservation_id
