from src.utilities.exceptions import ValidationError
from src.domain.reservation import Reservation

from datetime import datetime
from random import randint



class ReservationService:
    def __init__(self, reservation_repository):
        self.__repository = reservation_repository


    def make_reservation(self, reservation_data: dict) -> None:
        number = self.generate_reservation_number(reservation_data)
        arrival_date = datetime.strptime(reservation_data['arrival_date'], "%d.%m.%Y").date()
        departure_date = datetime.strptime(reservation_data['departure_date'], "%d.%m.%Y").date()
        reservation = Reservation(reservation_data['room_number'], reservation_data['guest_name'],
                                  reservation_data['guest_number'], arrival_date, departure_date)

        errors = reservation.validate()
        if errors:
            raise ValidationError('Validation error!', errors)

        try:
            self.__repository.add(number, reservation)
        except Exception as e:
            raise e


    def update_reservation(self, old_reservation_data: dict, new_reservation_data: dict) -> None:
        arrival_date = datetime.strptime(new_reservation_data['arrival_date'], "%d.%m.%Y").date()
        departure_date = datetime.strptime(new_reservation_data['departure_date'], "%d.%m.%Y").date()
        new_reservation = Reservation(new_reservation_data['room_number'], new_reservation_data['guest_name'],
                                      new_reservation_data['guest_number'], arrival_date, departure_date)

        errors = new_reservation.validate()
        if errors:
            raise ValidationError('Validation error!', errors)

        try:
            old_arrival_date = datetime.strptime(old_reservation_data['arrival_date'], "%d.%m.%Y").date()
            old_departure_date = datetime.strptime(old_reservation_data['departure_date'], "%d.%m.%Y").date()
            number = self.__repository.get_number(old_reservation_data['room_number'], old_arrival_date, old_departure_date)
            self.__repository.update(number, new_reservation)
        except Exception as e:
            raise e


    def delete_reservation(self, reservation_number: str) -> None:
        try:
            return self.__repository.remove(reservation_number)
        except Exception as e:
            raise e


    def get_all_reservations(self):
        return self.__repository.get_all()


    def get_reservations_for_room(self, room_number: str) -> dict:
        reservations = {}
        for reservation in self.__repository.get_all():
            if reservation.room_number == room_number:
                reservations[reservation.number] = reservation
        return reservations


    def generate_reservation_number(self, reservation_data):
        arrival_date = datetime.strptime(reservation_data['arrival_date'], "%d.%m.%Y").strftime("%d%m")
        departure_date = datetime.strptime(reservation_data['departure_date'], "%d.%m.%Y").strftime("%d%m")
        code = str(randint(1000, 9999))
        number = "R" + reservation_data['room_number'] + arrival_date + departure_date + code
        return number




    # def getIntervals(self, room):
    #     intervals = []
    #     for reservation in self.getAll():
    #         if reservation.room == room:
    #             intervals.append([reservation.arrivalDate, reservation.departureDate])
    #     return intervals
    #
    #
    # def getAvailableRooms(self, arrivalDate, departureDate):
    #     availableRooms = {}
    #     for room, capacity in self.__rooms.items():
    #         intervals = self.getIntervals(room)
    #         overlap = any(s <= departureDate and e >= arrivalDate for s, e in intervals)
    #         if not overlap:
    #             availableRooms[room] = capacity
    #     return availableRooms
    #
    # def getIntervalReservations(self, startDate, endDate):
    #     reservations = {}
    #     for reservation in self.getAll():
    #         overlap = reservation.arrivalDate <= endDate and reservation.departureDate >= startDate
    #         if overlap:
    #             reservations[reservation.number] = reservation
    #     return reservations
