from src.domain.floor_element import FloorElement


class Room(FloorElement):
    """
    Represents a room located on a floor, with attributes for identification, capacity, and pricing.

    Attributes:
        db_id (int): Unique identifier in the database.
        type (str): Type of the room.
        floor_id (int): Identifier of the floor the room belongs to.
        position (tuple): Coordinates of the room on the floor.
        number (str): Room number.
        capacity (int): Maximum occupancy.
        price_per_night (float): Price per night for the room.
    """

    def __init__(
            self,
            db_id: int = None,
            type: str = None,
            floor_id: int = None,
            position: tuple = None,
            number: str = None,
            capacity: int = None,
            price_per_night: float = None
    ):
        super().__init__(db_id, type, floor_id, position)
        self.__number = number
        self.__capacity = capacity
        self.__price_per_night = price_per_night

    @property
    def number(self) -> str:
        return self.__number
    @number.setter
    def number(self, room_number):
        self.__number = room_number

    @property
    def capacity(self) -> int:
        return self.__capacity
    @capacity.setter
    def capacity(self, value):
        self.__capacity = value

    @property
    def price_per_night(self) -> float:
        return self.__price_per_night
    @price_per_night.setter
    def price_per_night(self, value):
        self.__price_per_night = value

    def __str__(self):
        return (f"Room (DB ID: {self._db_id} | Type: {self._type} | Floor ID {self._floor_id} | "
                f"Position: {self._position} | Number: {self.__number} | Capacity: {self.__capacity} | "
                f"Price per night: ${self.__price_per_night})")

    def validate(self) -> list:
        errors = super().validate()
        if not self.__number:
            errors.append("Room number is required!")
        if self.__number and not isinstance(self.__number, str):
            errors.append("Room number must be a string!")
        if self.__capacity is None:
            errors.append("Capacity is required!")
        if self.__capacity and not isinstance(self.__capacity, int):
            errors.append("Invalid capacity!")
        if self.__price_per_night is None:
            errors.append("Price per night is required!")
        if self.__price_per_night and not isinstance(self.__price_per_night, float):
            errors.append("Invalid price per night!")
        return errors
