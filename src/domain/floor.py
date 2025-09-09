class Floor:
    def __init__(self, db_id=None, name=None, level=None):
        self.__db_id = db_id
        self.__name = name
        self.__level = level

        self.__elements = {}
        self._grid_cache = None


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
        # return list(self.__elements.values())
        return self.__elements

    def build_grid(self):
        grid_dict = {}
        for element in self.__elements.values():
            if element.position:
                grid_dict[element.position] = element
        return grid_dict

    @property
    def grid(self):
        if self._grid_cache is None:
            self._grid_cache = self.build_grid()
        return self._grid_cache


    def add_element(self, element):
        self.__elements[element.db_id] = element
        if self._grid_cache is not None and element.position:
            self._grid_cache[element.position] = element

    def move_element(self, element_id, new_position):
        if element_id in self.__elements:
            element = self.__elements[element_id]
            old_position = element.position
            element.position = new_position

            if self._grid_cache is not None:
                if old_position in self._grid_cache:
                    del self._grid_cache[old_position]
                self._grid_cache[new_position] = element

    def edit_element(self, element, new_properties):
        pass

    def delete_element(self, element):
        if element.db_id in self.__elements:
            if self._grid_cache is not None and element.position in self._grid_cache:
                del self._grid_cache[element.position]
            del self.__elements[element.db_id]


    def get_element_neighbors(self, element):
        x, y = element.position
        neighbor_positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        neighbors = {}
        grid = self.grid
        for pos in neighbor_positions:
            if pos in grid:
                neighbors[pos] = grid[pos]
        return neighbors

    def are_neighbors(self, element_1, element_2):
        x1, y1 = element_1.position
        x2, y2 = element_2.position
        return abs(x1 - x2) + abs(y1 - y2) == 1
