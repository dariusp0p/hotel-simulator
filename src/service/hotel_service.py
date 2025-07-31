from random import randint
from src.domain.floor import Floor
from src.domain.floor_element import FloorElement
from src.repository.hotel_repository import HotelRepository
from src.utilities.exceptions import ValidationError


class HotelService:
    def __init__(self, repository: HotelRepository):
        self.__repository = repository

    def get_floors(self):
        return self.__repository.get_floors()

    def get_floor_id(self, floor_name):
        return self.__repository.get_floor_id(floor_name)

    def add_floor(self, floor_name):
        self.__repository.add_floor(Floor(name=floor_name))
        # Adaugă automat o scară în centrul grilei
        element_data = {
            "element_type": "staircase",
            "floor_id": self.__repository.get_floor_id(floor_name),
            "capacity": 0,
            "position": (5, 5),
        }
        self.add_element(element_data)

    def rename_floor(self, old_name, new_name):
        self.__repository.rename_floor(old_name, new_name)

    def remove_floor(self, floor_name):
        self.__repository.remove_floor(floor_name)

    def get_floor_grid(self, floor_name):
        return self.__repository.get_floor_grid(floor_name)

    def get_rooms_by_capacity(self, capacity):
        return self.__repository.get_rooms_by_capacity(capacity)

    def add_element(self, element_data):
        floor_element = FloorElement(
            element_id=self.generate_element_id(element_data),
            element_type=element_data["element_type"],
            floor_id=element_data["floor_id"],
            capacity=element_data["capacity"],
            position=element_data["position"],
        )
        errors = floor_element.validate()
        if errors:
            raise ValidationError("Invalid Floor Element!", errors)
        self.__repository.add_element(floor_element)

    def move_element(self, element_id, new_position):
        self.__repository.move_element(element_id, new_position)

    def edit_element(self, element_id, new_capacity):
        self.__repository.edit_element(element_id, new_capacity)

    def remove_element(self, element_id):
        self.__repository.remove_element(element_id)

    def generate_element_id(self, element_data):
        prefix = {"staircase": "S", "hallway": "H", "room": "R"}.get(
            element_data["element_type"], "X"
        )
        floor_id = str(element_data["floor_id"])
        code = str(randint(100, 999))
        return f"{prefix}{floor_id}{code}"
