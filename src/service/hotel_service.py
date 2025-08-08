from random import randint
from src.domain.floor import Floor
from src.domain.floor_element import FloorElement
from src.repository.hotel_repository import HotelRepository
from src.utilities.exceptions import ValidationError


class HotelService:
    def __init__(self, repository: HotelRepository):
        self.__repository = repository


    # Getters
    def get_all_floors_sorted_by_level(self):
        floors = self.__repository.get_all_floors()
        return sorted(floors, key=lambda floor: floor.level, reverse=True)

    def get_floor_id(self, floor_name):
        return self.__repository.get_floor_id(floor_name)

    def get_floor_grid(self, floor_name):
        return self.__repository.get_floor_grid(floor_name)

    def get_rooms_by_capacity(self, capacity):
        #TODO
        pass


    # CRUD

    # Floors
    def add_floor(self, floor_name, level):
        self.__repository.add_floor(Floor(name=floor_name, level=level))
        # Adaugă automat o scară în centrul grilei
        # element_data = {
        #     "element_type": "staircase",
        #     "floor_id": self.__repository.get_floor_id(floor_name),
        #     "capacity": 0,
        #     "position": (5, 5),
        # }
        # self.add_element(element_data)

    def update_floor_level(self, floor_id, new_level):
        self.__repository.move_floor(floor_id, new_level)

    def rename_floor(self, old_name, new_name):
        self.__repository.rename_floor(old_name, new_name)

    def remove_floor(self, floor_id):
        floor_elements = self.__repository.get_elements_by_floor_id(floor_id)
        for element in floor_elements:
            self.__repository.remove_element(element.db_id)
        self.__repository.remove_floor(floor_id)

    # Elements
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
