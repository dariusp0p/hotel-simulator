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

    def get_floor_id(self, floor_name) -> int:
        """Returns the ID of the floor with the given name."""
        return self.__repository.get_floor_id(floor_name)

    def get_floor_grid(self, floor_name) -> dict:
        """Returns the grid representation of the floor with the given name."""
        return self.__repository.get_floor_grid(floor_name)

    def get_elements_by_floor_id(self, floor_id) -> list[FloorElement]:
        """Returns all elements on the floor with the given ID."""
        elements_dict = self.__repository.get_elements_by_floor_id(floor_id)
        return list(elements_dict.values())

    def get_connections_by_floor_name(self, floor_name):
        """Returns all connections on the floor with the given name."""
        floor_id = self.get_floor_id(floor_name)
        return self.__repository.get_connections_by_floor_id(floor_id)

    def get_all_connections(self):
        return self.__repository.get_all_connections()

    def get_rooms_by_capacity(self, capacity):
        return self.__repository.get_rooms_by_capacity(capacity)


    # CRUD

    # Floors
    def add_floor(self, floor_name, level):
        """Adds a new floor with the given name and level."""
        self.__repository.add_floor(Floor(name=floor_name, level=level))

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
    def add_element(self, element_data):
        if element_data["type"] == "room":
            element = Room(
                type=element_data["type"], floor_id=element_data["floor_id"],
                position=element_data["position"], number=element_data["number"],
                capacity=element_data["capacity"], price_per_night=element_data["price_per_night"],
            )
        else:
            element = FloorElement(
                type=element_data["type"],
                floor_id=element_data["floor_id"],
                position=element_data["position"],
            )

        errors = element.validate()
        if errors:
            raise ValidationError("Invalid Floor Element!", errors)

        try:
            self.__repository.add_element(element)
        except Exception as e:
            raise e


    def move_element(self, element_id, new_position):
        self.__repository.move_element(element_id, new_position)

    def edit_room(self, element_id, new_number, new_capacity, new_price_per_night):
        self.__repository.edit_room(element_id, new_number, new_capacity, new_price_per_night)

    def remove_element(self, element):
        self.__repository.remove_element(element)
