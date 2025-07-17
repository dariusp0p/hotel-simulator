from datetime import date



class Reservation:
    def __init__(self, db_id=None, reservation_id=None, room_number=None, guest_name=None, number_of_guests=None, check_in_date=None, check_out_date=None):
        self.__db_id = db_id
        self.__reservation_id = reservation_id
        self.__room_number = room_number
        self.__guest_name = guest_name
        self.__number_of_guests = number_of_guests
        self.__check_in_date = check_in_date
        self.__check_out_date = check_out_date


    @property
    def db_id(self):
        return self.__db_id
    @db_id.setter
    def db_id(self, value):
        self.__db_id = value

    @property
    def reservation_id(self):
        return self.__reservation_id


    @property
    def room_number(self):
        return self.__room_number

    @property
    def guest_name(self):
        return self.__guest_name

    @property
    def number_of_guests(self):
        return self.__number_of_guests

    @property
    def check_in_date(self):
        return self.__check_in_date

    @property
    def check_out_date(self):
        return self.__check_out_date


    def __str__(self):
        return f'Room: {self.__room_number} | Guest name: {self.__guest_name} | Number of guests: {self.__number_of_guests} | Check-in: {self.__check_in_date} | Check-out: {self.__check_out_date}'


    def validate(self) -> list:
        errors = []
        if not isinstance(self.__room_number, str):
            errors.append("Invalid room!")
        if not isinstance(self.__number_of_guests, int):
            errors.append("Invalid guest number!")
        if not isinstance(self.__check_in_date, date) or not isinstance(self.__check_out_date, date):
            errors.append("Invalid dates!")
        if self.__check_in_date > self.__check_out_date:
            errors.append("Invalid dates!")
        if len(errors) > 0:
            return errors
