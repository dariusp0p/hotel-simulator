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

    def get_floor_grid(self, floor_name):
        return self.__repository.get_floor_grid(floor_name)


    def add_floor(self, floor_name):
        self.__repository.add_floor(Floor(name=floor_name))
        element_data = {
            "element_type": "staircase",
            "floor_id": self.__repository.get_floor_id(floor_name),
            "capacity": 0,
            "position": (5, 5)
        }
        self.add_element(element_data)


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
            raise ValidationError('Invalid Floor Element!', errors)
        try:
            self.__repository.add_element(floor_element)
        except Exception as e:
            raise e



    def generate_element_id(self, element_data):
        if element_data["element_type"] == "staircase":
            type = "S"
        elif element_data["element_type"] == "hallway":
            type = "H"
        else:
            type = "R"
        floor_name = str(element_data["floor_id"])
        code = str(randint(100, 999))
        element_id = type + floor_name + code
        return element_id


    # def rename_floor(self, floor_name, new_name):
    #     hotel = self.__repository.get()
    #     hotel.rename_floor(floor_name, new_name)
    #     self.__repository.save(hotel)
    #
    # def remove_floor(self, floor_name):
    #     hotel = self.__repository.get()
    #     if len(hotel.floors) <= 1:
    #         raise ValueError("Hotel must have at least one floor.")
    #     hotel.delete_floor(floor_name)
    #     self.__repository.save(hotel)
    #
    #
    #
    #     element_id = str(uuid.uuid4())
    #     element = FloorElement(
    #         element_id=element_id,
    #         element_type=element_data["element_type"],
    #         floor_name=element_data["floor_name"],
    #         position=element_data["position"],
    #         capacity=element_data.get("capacity")
    #     )
    #     floor.add_element(element, element.position)
    #     self.__repository.save(hotel)
    #
    #
    #
    # def edit_room(self, element_data: dict, new_name, new_capacity):
    #     pass
    #
    # def move_element(self, element_data: dict, new_position):
    #     pass
    #
    #
    # def remove_element(self, floor_name, element_id):
    #     pass


