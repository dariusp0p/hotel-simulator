from src.utilities.exceptions import ValidationError, ElementNotFoundError


class Floor:
    def __init__(self, db_id=None, name=None, level=None):
        self.__db_id = db_id
        self.__name = name
        self.__level = level

        self.__elements = {}
        self.__grid_cache = None


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
        return self.__elements

    def _build_grid(self):
        grid_dict = {}
        for element in self.__elements.values():
            if element.position:
                grid_dict[element.position] = element
        return grid_dict

    @property
    def grid(self):
        if self.__grid_cache is None:
            self.__grid_cache = self._build_grid()
        return self.__grid_cache


    # CRUD Operations for Floor Elements

    def add_element(self, element):
        """Adds a FloorElement (Room or Staircase) to the floor. Theta(1) complexity."""
        self.__elements[element.db_id] = element
        if self.__grid_cache is not None and element.position:
            self.__grid_cache[element.position] = element

    def move_element(self, element_id, new_position):
        """Moves an element to a new position. Theta(1) complexity."""
        if element_id not in self.__elements:
            raise ElementNotFoundError("Element not found!")

        element = self.__elements[element_id]
        old_position = element.position
        element.position = new_position

        if self.__grid_cache is not None:
            if old_position in self.__grid_cache:
                del self.__grid_cache[old_position]
            self.__grid_cache[new_position] = element

    def edit_room(self, element_id, new_number, new_capacity, new_price_per_night):
        """Edits the details of a room. Theta(1) complexity."""
        if element_id not in self.__elements:
            raise ElementNotFoundError("Room not found!")

        element = self.__elements[element_id]
        element.number = new_number
        element.capacity = new_capacity
        element.price_per_night = new_price_per_night

    def delete_element(self, element_id):
        """Deletes an element from the floor. Theta(1) complexity."""
        if element_id not in self.__elements:
            raise ElementNotFoundError("Element not found!")

        element = self.__elements[element_id]
        if self.__grid_cache is not None and element.position in self.__grid_cache:
            del self.__grid_cache[element.position]
        del self.__elements[element_id]


    def get_element_neighbors(self, element_id):
        element = self.__elements.get(element_id)
        x, y = element.position
        neighbor_positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        neighbors = {}
        grid = self.grid
        for pos in neighbor_positions:
            if pos in grid:
                neighbors[pos] = grid[pos]
        return neighbors
