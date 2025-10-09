from src.domain.floor_element import FloorElement
from src.utilities.exceptions import ElementNotFoundError


class Floor:
    """
    Represents a floor in a building, containing floor elements.

    Attributes:
        db_id (int): Unique identifier in the database.
        name (str): Name of the floor.
        level (int): Level number of the floor.
        elements (dict): Dictionary of floor elements, keyed by their db_id.
    """

    def __init__(self, db_id: int = None, name: str = None, level: int = None):
        self.__db_id = db_id
        self.__name = name
        self.__level = level

        self.__elements = {}
        self.__grid_cache = None

    @property
    def db_id(self) -> int:
        return self.__db_id
    @db_id.setter
    def db_id(self, db_id):
        self.__db_id = db_id

    @property
    def name(self) -> str:
        return self.__name
    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def level(self) -> int:
        return self.__level
    @level.setter
    def level(self, level):
        self.__level = level

    @property
    def elements(self) -> dict:
        return self.__elements

    @property
    def grid(self):
        if self.__grid_cache is None:
            self.__grid_cache = self._build_grid()
        return self.__grid_cache

    def _build_grid(self):
        grid_dict = {}
        for element in self.__elements.values():
            if element.position:
                grid_dict[element.position] = element
        return grid_dict

    # Floor Elements CRUD

    def add_element(self, element: FloorElement):
        """Adds a FloorElement to the floor. Theta(1) complexity."""
        self.__elements[element.db_id] = element
        if self.__grid_cache is not None and element.position:
            self.__grid_cache[element.position] = element

    def move_element(self, element_id: int, new_position: tuple[int, int]):
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

    def edit_room(self, element_id: int, new_number: str, new_capacity: int, new_price_per_night: float):
        """Edits the details of a room. Theta(1) complexity."""
        if element_id not in self.__elements:
            raise ElementNotFoundError("Room not found!")

        element = self.__elements[element_id]
        element.number = new_number
        element.capacity = new_capacity
        element.price_per_night = new_price_per_night

    def delete_element(self, element_id: int):
        """Deletes an element from the floor. Theta(1) complexity."""
        if element_id not in self.__elements:
            raise ElementNotFoundError("Element not found!")

        element = self.__elements[element_id]
        if self.__grid_cache is not None and element.position in self.__grid_cache:
            del self.__grid_cache[element.position]
        del self.__elements[element_id]

    def get_element_neighbors(self, element_id: int) -> dict:
        """Returns neighboring elements (up, down, left, right) of the specified element."""
        element = self.__elements.get(element_id)
        x, y = element.position
        neighbor_positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        neighbors = {}
        grid = self.grid
        for pos in neighbor_positions:
            if pos in grid:
                neighbors[pos] = grid[pos]
        return neighbors

    # Others

    def __str__(self):
        return (f'Floor (DB ID: {self.__db_id} | Name: {self.__name} | Level: {self.__level} | '
                f'Element IDs: {list(self.__elements.keys())})')

    def validate(self) -> list:
        errors = []
        if not isinstance(self.db_id, (int, type(None))):
            errors.append("DB ID must be an integer or None!")
        if not self.__name:
            errors.append("Name is required!")
        if self.__name and not isinstance(self.__name, str):
            errors.append("Name must be a string!")
        if self.__level is None:
            errors.append("Level is required!")
        if self.__level and not isinstance(self.__level, int):
            errors.append("Level must be an integer!")
        return errors
