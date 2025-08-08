class Floor:
    def __init__(self, db_id=None, name=None, level=None):
        self.__db_id = db_id
        self.__name = name
        self.__level = level

        self.__grid = {}
        self.__elements = {}


    @property
    def db_id(self):
        return self.__db_id
    @db_id.setter
    def db_id(self, db_id):
        self.__db_id = db_id

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def level(self):
        return self.__level
    @level.setter
    def level(self, level):
        self.__level = level

    @property
    def elements(self):
        return list(self.__elements.values())

    @property
    def grid(self):
        return self.__grid



    def add_element(self, element):
        self.__elements[element.db_id] = element
        self.__grid[element.position] = element

    def move_element(self, element, new_position):
        pass

    def edit_element(self, element, new_properties):
        pass

    def delete_element(self, element):
        if element.db_id in self.__elements:
            del self.__elements[element.db_id]
        if element.position in self.__grid:
            del self.__grid[element.position]


    def get_element_neighbors(self, element):
        x, y = element.position
        neighbor_positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        neighbors = {}
        for pos in neighbor_positions:
            if pos in self.__grid:
                neighbors[pos] = self.__grid[pos]
        return neighbors

    def are_neighbors(self, element_1, element_2):
        x1, y1 = element_1.position
        x2, y2 = element_2.position
        return abs(x1 - x2) + abs(y1 - y2) == 1
