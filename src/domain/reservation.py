from src.exceptions import ValidationError

from datetime import date



class Reservation:
    def __init__(self, room_number, guest_name, guest_number, arrival_date, departure_date):
        self.__room_number = room_number
        self.__guest_name = guest_name
        self.__guest_number = guest_number
        self.__arrival_date = arrival_date
        self.__departure_date = departure_date


    @property
    def room_number(self):
        return self.__room_number

    @property
    def guest_name(self):
        return self.__guest_name

    @property
    def guest_number(self):
        return self.__guest_number

    @property
    def arrival_date(self):
        return self.__arrival_date

    @property
    def departure_date(self):
        return self.__departure_date


    def __str__(self):
        return f'Room: {self.__room_number} | Guest name: {self.__guest_name} | Guest number: {self.__guest_number} | Arrival: {self.__arrival_date} | Departure: {self.__departure_date}'


    def validate(self):
        errors = []
        if not isinstance(self.room_number, str):
            errors.append("Invalid room!")
        if not isinstance(self.guest_number, int):
            errors.append("Invalid guest number!")
        if not isinstance(self.arrival_date, date) or not isinstance(self.departure_date, date):
            errors.append("Invalid dates!")
        if self.arrival_date > self.departure_date:
            errors.append("Invalid dates!")
        if len(errors) > 0:
            raise ValidationError(errors)
