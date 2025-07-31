from datetime import datetime
from random import randint

from src.repository.reservation_repository import ReservationRepository
from src.utilities.exceptions import ValidationError
from src.domain.reservation import Reservation



class ReservationService:
    def __init__(self, reservation_repository: ReservationRepository):
        self.__repository = reservation_repository


    def get_all_reservations(self):
        return self.__repository.get_all_reservations()

    def get_reservations_by_date_interval(self, from_date, to_date):
        from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

        all_reservations = self.__repository.get_all_reservations()
        filtered_reservations = [
            reservation for reservation in all_reservations
            if not (reservation.check_out_date < from_date or reservation.check_in_date > to_date)
        ]

        return filtered_reservations

    def get_reservations_by_room_id(self, room_id):
        return self.__repository.get_reservations_by_room_number(room_id)

    def get_reservation_by_id(self, reservation_id):
        return self.__repository.get_by_reservation_id(reservation_id)

    def get_reservations_by_guest_name(self, guest_name):
        return self.__repository.get_by_guest_name(guest_name)


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








    def generate_reservation_id(self, reservation_data):
        check_in_date = datetime.strptime(reservation_data['check_in_date'], "%Y-%m-%d").strftime("%d%m")
        check_out_date = datetime.strptime(reservation_data['check_out_date'], "%Y-%m-%d").strftime("%d%m")
        code = str(randint(1000, 9999))
        reservation_id = "R" + reservation_data['room_number'] + check_in_date + check_out_date + code
        return reservation_id


