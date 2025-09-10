from src.domain.floor_element import FloorElement



class Room(FloorElement):
    def __init__(self, db_id=None, type=None, floor_id=None, position=None,
                 number=None, capacity=None, price_per_night=None):
        super().__init__(db_id, type, floor_id, position)
        self.__number = number
        self.__capacity = capacity
        self.__price_per_night = price_per_night


    @property
    def number(self):
        return self.__number
    @number.setter
    def number(self, room_number):
        self.__number = room_number

    @property
    def capacity(self):
        return self.__capacity
    @capacity.setter
    def capacity(self, value):
        self.__capacity = value

    @property
    def price_per_night(self):
        return self.__price_per_night
    @price_per_night.setter
    def price_per_night(self, value):
        self.__price_per_night = value

    # TODO
    def validate(self):
        errors = []
        return errors
