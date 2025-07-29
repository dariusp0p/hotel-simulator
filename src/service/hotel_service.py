import uuid

from src.domain.floor import Floor
from src.domain.floor_element import FloorElement
from src.repository.hotel_repository import HotelRepository



class HotelService:
    def __init__(self, repository: HotelRepository):
        self.__repository = repository


    def get_floors(self):
        hotel = self.__repository.get()
        return list(hotel.floors.keys())

    def get_floor_grid(self, floor_name):
        hotel = self.__repository.get()
        floor = hotel.floors.get(floor_name)
        if not floor:
            raise ValueError(f"Floor '{floor_name}' does not exist.")
        return floor.grid


    def add_floor(self, floor_name):
        hotel = self.__repository.get()
        hotel.add_floor(floor_name)
        staircase = FloorElement(
            element_id=str(uuid.uuid4()),
            element_type="staircase",
            floor_name=floor_name,
            position=(5, 5)
        )
        hotel.floors[floor_name].add_element(staircase)
        self.__repository.save(hotel)

    def rename_floor(self, floor_name, new_name):
        hotel = self.__repository.get()
        hotel.rename_floor(floor_name, new_name)
        self.__repository.save(hotel)

    def remove_floor(self, floor_name):
        hotel = self.__repository.get()
        if len(hotel.floors) <= 1:
            raise ValueError("Hotel must have at least one floor.")
        hotel.delete_floor(floor_name)
        self.__repository.save(hotel)


    def add_element(self, element_data: dict):
        hotel = self.__repository.get()
        floor = hotel.floors.get(element_data["floor_name"])
        if not floor:
            raise ValueError("Floor does not exist")

        element_id = str(uuid.uuid4())
        element = FloorElement(
            element_id=element_id,
            element_type=element_data["element_type"],
            floor_name=element_data["floor_name"],
            position=element_data["position"],
            capacity=element_data.get("capacity")
        )
        floor.add_element(element, element.position)
        self.__repository.save(hotel)



    def edit_room(self, element_data: dict, new_name, new_capacity):
        hotel = self.__repository.get()
        floor = hotel.floors.get(element_data["floor_name"])
        room = floor.elements.get(element_data["element_id"])
        if not room:
            raise ValueError("Room does not exist")
        room.name = new_name
        room.capacity = new_capacity
        self.__repository.save(hotel)

    def move_element(self, element_data: dict, new_position):
        hotel = self.__repository.get()
        floor = hotel.floors.get(element_data["floor_name"])
        floor.move_element(element_data["element_id"], new_position)
        self.__repository.save(hotel)


    def remove_element(self, floor_name, element_id):
        hotel = self.__repository.get()
        floor = hotel.floors[floor_name]
        element = floor.elements[element_id]
        if element.element_type == 'staircase':
            staircases = [e for e in floor.elements.values() if e.element_type == 'staircase']
            if len(staircases) <= 1:
                raise ValueError("Cannot remove the only staircase on a floor")
        floor.remove_element(element_id)
        self.__repository.save(hotel)


