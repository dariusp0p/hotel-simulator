from src.domain.floor_element import FloorElement



class Room(FloorElement):
    def __init__(self, db_id=None, element_type=None, floor_id=None, position=None,
                 room_number=None, capacity=None, price_per_night=None):
        super().__init__(db_id, element_type, floor_id, position)
        self.__room_number = room_number
        self.__capacity = capacity
        self.__price_per_night = price_per_night


    @property
    def room_number(self):
        return self.__room_number
    @room_number.setter
    def room_number(self, room_number):
        self.__room_number = room_number

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
