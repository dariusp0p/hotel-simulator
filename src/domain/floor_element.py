class FloorElement:
    def __init__(self, element_id=None, element_type=None, floor_name=None, capacity=None, position=None, connections=None):
        self.__element_id = element_id
        self.__element_type = element_type
        self.__floor_name = floor_name
        self.__capacity = capacity
        self.__position = position
        self.__connections = connections


    @property
    def element_id(self):
        return self.__element_id

    @property
    def element_type(self):
        return self.__element_type

    @property
    def floor_name(self):
        return self.__floor_name

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


    def is_neighbor(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2) == 1


    def can_connect_to(self, other):
        if self.__element_type == 'room':
            return other.element_type in {'hallway', 'staircase'} and self.is_neighbor(self.__position, other.position) and len(self.__connections) < 1
        elif self.__element_type == 'hallway' and self.is_neighbor(other.position, self.__position):
            return len(self.__connections) < 4
        elif self.__element_type == 'staircase' and (self.is_neighbor(other.position, self.__position) or self.floor_name != other.floor_name):
            return len(self.__connections) < 6
        return False
