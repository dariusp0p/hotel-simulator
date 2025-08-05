class FloorElement:
    def __init__(self, db_id=None, element_type=None, floor_id=None, position=None):
        self.__db_id = db_id
        self.__element_type = element_type
        self.__floor_id = floor_id
        self.__position = position


    @property
    def db_id(self):
        return self.__db_id
    @db_id.setter
    def db_id(self, db_id):
        self.__db_id = db_id

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
    def position(self):
        return self.__position
    @position.setter
    def position(self, position):
        self.__position = position

    # TODO
    def validate(self) -> list:
        errors = []
        return errors
