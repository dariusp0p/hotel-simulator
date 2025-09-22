from src.domain.floor import Floor
from src.domain.room import Room
from src.domain.floor_element import FloorElement
from src.repository.hotel_repository import HotelRepository
from src.utilities.exceptions import ValidationError



class HotelService:
    def __init__(self, repository: HotelRepository):
        self.__repository = repository


    # Getters
    def get_all_floors_sorted_by_level(self) -> list[Floor]:
        """Returns all floors sorted by their level in descending order (highest level first)."""
        floors = self.__repository.get_all_floors()
        return sorted(floors, key=lambda floor: floor.level, reverse=True)

    def get_floor(self, floor_id) -> Floor:
        """Returns the floor with the given ID."""
        return self.__repository.get_floor_by_id(floor_id)

    def get_floor_id(self, floor_name) -> int:
        """Returns the ID of the floor with the given name."""
        return self.__repository.get_floor_id(floor_name)

    def get_floor_grid(self, floor_id) -> dict:
        """Returns the grid representation of the floor with the given id."""
        return self.__repository.get_floor_grid(floor_id)

    def get_elements_by_floor_id(self, floor_id) -> list[FloorElement]:
        """Returns all elements on the floor with the given ID."""
        elements_dict = self.__repository.get_elements_by_floor_id(floor_id)
        return list(elements_dict.values())

    def get_floor_connections(self, floor_id):
        """Returns all connections on the floor with the given id."""
        return self.__repository.get_connections_by_floor_id(floor_id)

    def get_all_connections(self):
        return self.__repository.get_all_connections()

    def get_room_by_id(self, room_id) -> Room:
        return self.__repository.get_room_by_id(room_id)

    def get_room_by_number(self, room_number) -> Room:
        return self.__repository.get_room_by_number(room_number)

    def get_rooms_by_capacity(self, capacity):
        return self.__repository.get_rooms_by_capacity(capacity)


    # CRUD

    # Floors
    def add_floor(self, floor_name, level):
        """Adds a new floor with the given name and level."""
        return self.__repository.add_floor(Floor(name=floor_name, level=level))

    def rename_floor(self, old_name, new_name):
        """Renames the floor with the given old name to the new name."""
        self.__repository.rename_floor(old_name, new_name)

    def update_floor_level(self, floor_id, new_level):
        """Updates the level of the floor with the given ID to the new level."""
        self.__repository.move_floor(floor_id, new_level)

    def remove_floor(self, floor_id):
        """Removes the floor with the given ID."""
        self.__repository.remove_floor(floor_id)


    # Elements
    def add_element(self, element_type, floor_id, position, number=None, capacity=None, price_per_night=None) -> int:
        if element_type == "room":
            element = Room(
                type=element_type, floor_id=floor_id,
                position=position, number=number,
                capacity=capacity, price_per_night=price_per_night
            )
        else:
            element = FloorElement(
                type=element_type, floor_id=floor_id,
                position=position
            )

        errors = element.validate()
        if errors:
            raise ValidationError("Invalid Floor Element!", errors)

        return self.__repository.add_element(element)


    def move_element(self, element_id, new_position):
        self.__repository.move_element(element_id, new_position)

    def edit_room(self, element_id, new_number, new_capacity, new_price_per_night):
        self.__repository.edit_room(element_id, new_number, new_capacity, new_price_per_night)

    def remove_element(self, element_id, element_type, floor_id):
        self.__repository.remove_element(element_id, element_type, floor_id)
