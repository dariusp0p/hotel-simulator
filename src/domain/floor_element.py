class FloorElement:
    def __init__(self, db_id=None, element_id=None, element_type=None, floor_id=None, capacity=None, position=None, connections=None):
        self.__db_id = db_id
        self.__element_id = element_id
        self.__element_type = element_type
        self.__floor_id = floor_id
        self.__capacity = capacity
        self.__position = position
        self.__connections = connections


    @property
    def db_id(self):
        return self.__db_id
    @db_id.setter
    def db_id(self, db_id):
        self.__db_id = db_id

    @property
    def element_id(self):
        return self.__element_id

    @property
    def element_type(self):
        return self.__element_type

    @property
    def floor_id(self):
        return self.__floor_id
    @floor_id.setter
    def floor_id(self, floor_id):
        self.__floor_id = floor_id

    @property
    def capacity(self):
        return self.__capacity

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        self.__position = position

    @property
    def connections(self):
        return self.__connections

    # TODO
    def validate(self) -> list:
        pass
