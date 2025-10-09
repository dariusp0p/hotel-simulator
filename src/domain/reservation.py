from datetime import date


class Reservation:
    """
    Class representing a reservation in the hotel management system.

    Attributes:
        db_id (int): Unique identifier in the database.
        reservation_id (str): Unique reservation identifier.
        room_id (int): Identifier of the room being reserved.
        guest_name (str): Name of the guest making the reservation.
        number_of_guests (int): Number of guests for the reservation.
        check_in_date (date): Check-in date for the reservation.
        check_out_date (date): Check-out date for the reservation.
    """

    def __init__(
            self,
            db_id: int = None,
            reservation_id: str = None,
            room_id: int = None,
            guest_name: str = None,
            number_of_guests: int = None,
            check_in_date: date = None,
            check_out_date: date = None
    ):
        self.__db_id = db_id
        self.__reservation_id = reservation_id
        self.__room_id = room_id
        self.__guest_name = guest_name
        self.__number_of_guests = number_of_guests
        self.__check_in_date = check_in_date
        self.__check_out_date = check_out_date

    @property
    def db_id(self) -> int:
        return self.__db_id
    @db_id.setter
    def db_id(self, value):
        self.__db_id = value

    @property
    def reservation_id(self) -> str:
        return self.__reservation_id

    @property
    def room_id(self) -> int:
        return self.__room_id
    @room_id.setter
    def room_id(self, value):
        self.__room_id = value

    @property
    def guest_name(self) -> str:
        return self.__guest_name
    @guest_name.setter
    def guest_name(self, value):
        self.__guest_name = value

    @property
    def number_of_guests(self) -> int:
        return self.__number_of_guests
    @number_of_guests.setter
    def number_of_guests(self, value):
        self.__number_of_guests = value

    @property
    def check_in_date(self) -> date:
        return self.__check_in_date
    @check_in_date.setter
    def check_in_date(self, value):
        self.__check_in_date = value

    @property
    def check_out_date(self) -> date:
        return self.__check_out_date
    @check_out_date.setter
    def check_out_date(self, value):
        self.__check_out_date = value

    def __str__(self):
        return (f'Reservation (DB ID: {self.__db_id} | Reservation ID: {self.__reservation_id} | '
                f'Room ID: {self.__room_id} | Guest name: {self.__guest_name} | '
                f'Number of guests: {self.__number_of_guests} | '
                f'Check-in date: {self.__check_in_date.isoformat()} | '
                f'Check-out date: {self.__check_out_date.isoformat()})')

    def validate(self) -> list:
        errors = []
        if not isinstance(self.__db_id, (int, type(None))):
            errors.append("DB ID must be an integer or None!")
        if not self.__reservation_id:
            errors.append("Reservation ID is required!")
        if self.__reservation_id and not isinstance(self.__reservation_id, str):
            errors.append("Reservation ID must be a string or None!")
        if self.__room_id is None:
            errors.append("Room ID is required!")
        if self.__room_id and not isinstance(self.__room_id, int):
            errors.append("Room ID must be an integer!")
        if not self.__guest_name:
            errors.append("Guest name is required!")
        if self.__guest_name and not isinstance(self.__guest_name, str):
            errors.append("Guest name must be a string!")
        if self.__number_of_guests is None:
            errors.append("Number of guests is required!")
        if self.__number_of_guests and not isinstance(self.__number_of_guests, int):
            errors.append("Number of guests must be an integer!")
        if isinstance(self.__number_of_guests, int) and self.__number_of_guests <= 0:
            errors.append("Number of guests must be greater than zero!")
        if not self.__check_in_date:
            errors.append("Check-in date is required!")
        if self.__check_in_date and not isinstance(self.__check_in_date, date):
            errors.append("Check-in date must be a date!")
        if not self.__check_out_date:
            errors.append("Check-out date is required!")
        if self.__check_out_date and not isinstance(self.__check_out_date, date):
            errors.append("Check-out date must be a date!")
        if (isinstance(self.__check_in_date, date) and isinstance(self.__check_out_date, date)
                and self.check_in_date > self.__check_out_date):
            errors.append("Invalid date interval!")
        return errors
