import sqlite3

from src.domain.floor import Floor
from src.domain.floor_element import FloorElement
from src.db import hotel_model as db


class HotelRepository:
    def __init__(self, connection):
        self.__connection = connection

        self.__floors_by_id = {}
        self.__floors_by_name = {}

        self.load_from_db()

    @property
    def connection(self):
        return self.__connection

    def get_floors(self):
        return self.__floors_by_name.keys()

    def get_floor_grid(self, floor_name):
        return self.__floors_by_name[floor_name].grid

    def get_floor_id(self, floor_name):
        return self.__floors_by_name[floor_name].db_id

    def get_rooms_by_capacity(self, capacity):
        return db.get_rooms_by_capacity(self.__connection, capacity)

    def load_from_db(self):
        floors = db.get_all_floors(self.__connection)

        for db_id, floor_name in floors:
            floor_obj = Floor(db_id, floor_name)
            elements = db.get_elements_by_floor_id(self.__connection, db_id)
            for row in elements:
                floor_element = FloorElement(
                    db_id=row[0],
                    element_id=row[1],
                    element_type=row[2],
                    floor_id=row[3],
                    capacity=row[4],
                    position=(row[5], row[6]),
                )
                floor_obj.load_element(floor_element)
            self.__floors_by_name[floor_name] = floor_obj
            self.__floors_by_id[db_id] = floor_obj

    def add_floor(self, floor):
        if floor.db_id in self.__floors_by_id or floor.name in self.__floors_by_name:
            raise Exception("Floor already exists")
        try:
            db.add_floor(self.__connection, floor.name)
            new_db_row = db.get_floor_by_name(self.__connection, floor.name)
            floor.db_id = new_db_row[0][0]
            self.__floors_by_id[floor.db_id] = floor
            self.__floors_by_name[floor.name] = floor
        except sqlite3.IntegrityError:
            raise Exception(f"NONO")
        except sqlite3.OperationalError:
            raise Exception("Database is unavailable or corrupted.")

    def add_element(self, element):
        if element.element_id in self.__floors_by_id[element.floor_id].elements:
            raise Exception("Element already exists")
        try:
            db.add_element(
                self.__connection,
                element.element_id,
                element.element_type,
                element.floor_id,
                element.capacity,
                element.position[0],
                element.position[1],
            )
            new_db_row = db.get_element_by_element_id(
                self.__connection, element.element_id
            )
            element.db_id = new_db_row[0]
            self.__floors_by_id[element.floor_id].load_element(element)
        except sqlite3.IntegrityError:
            raise Exception(f"Element with id {element.element_id} already exists.")
        except sqlite3.OperationalError:
            raise Exception("Database is unavailable or corrupted.")

    def rename_floor(self, old_name, new_name):
        if new_name in self.__floors_by_name:
            raise Exception("New floor name already exists")
        floor = self.__floors_by_name.get(old_name)
        if not floor:
            raise Exception("Old floor not found")

        db.rename_floor(self.__connection, floor.db_id, new_name)

        del self.__floors_by_name[old_name]
        floor.name = new_name
        self.__floors_by_name[new_name] = floor

    def remove_floor(self, floor_name):
        floor = self.__floors_by_name.get(floor_name)
        if not floor:
            raise Exception("Floor not found")

        db.remove_floor(self.__connection, floor.db_id)

        del self.__floors_by_id[floor.db_id]
        del self.__floors_by_name[floor_name]

    def move_element(self, element_id, new_position):
        db.update_element_position(
            self.__connection, element_id, new_position[0], new_position[1]
        )
        for floor in self.__floors_by_id.values():
            if element_id in floor.elements:
                element = floor.elements[element_id]
                element.position = new_position
                break

    def edit_element(self, element_id, new_capacity):
        db.update_element_capacity(self.__connection, element_id, new_capacity)
        for floor in self.__floors_by_id.values():
            if element_id in floor.elements:
                element = floor.elements[element_id]
                element.capacity = new_capacity
                break

    def remove_element(self, element_id):
        db.delete_element(self.__connection, element_id)
        for floor in self.__floors_by_id.values():
            if element_id in floor.elements:
                del floor.elements[element_id]
                break
