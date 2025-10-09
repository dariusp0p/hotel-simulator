class FloorElement:
    """
    Represents a generic element located on a floor, such as a room or other structure.

    Attributes:
        db_id (int): Unique identifier in the database.
        type (str): Type of the floor element.
        floor_id (int): Identifier of the floor this element belongs to.
        position (tuple): Position of the element on the floor.
    """

    def __init__(self, db_id: int = None, type: str = None, floor_id: int = None, position: tuple = None):
        self._db_id = db_id
        self._type = type
        self._floor_id = floor_id
        self._position = position

    @property
    def db_id(self) -> int:
        return self._db_id
    @db_id.setter
    def db_id(self, db_id: int):
        self._db_id = db_id

    @property
    def type(self) -> str:
        return self._type

    @property
    def floor_id(self) -> int:
        return self._floor_id
    @floor_id.setter
    def floor_id(self, floor_id: int):
        self._floor_id = floor_id

    @property
    def position(self) -> tuple:
        return self._position
    @position.setter
    def position(self, position: tuple):
        self._position = position

    def __str__(self):
        return (f"Floor Element (DB ID: {self._db_id} | Type: {self._type} | Floor ID {self._floor_id} | "
                f"Position: {self._position})")

    def validate(self) -> list:
        errors = []
        if not isinstance(self._db_id, (int, type(None))):
            errors.append("DB ID must be an integer or None!")
        if not self._type:
            errors.append("Type is required!")
        if self._type and not isinstance(self._type, str):
            errors.append("Type must be a string!")
        if not self._floor_id:
            errors.append("Floor ID is required!")
        if self._floor_id and not isinstance(self._floor_id, int):
            errors.append("Floor ID must be an integer!")
        if not self._position:
            errors.append("Position is required!")
        if self._position and (not isinstance(self._position, tuple) or len(self._position) != 2 or
                             not all(isinstance(coord, int) for coord in self._position)):
            errors.append("Position must be a tuple of two integers!")
        return errors
