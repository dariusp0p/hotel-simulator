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
                    position=(row[5], row[6])
                )
                floor_obj.load_element(floor_element)
            self.__floors_by_name[floor_name] = floor_obj
            self.__floors_by_id[db_id] = floor_obj


    def add_floor(self, floor):
        if floor.db_id in self.__floors_by_id or floor.name in self.__floors_by_name:
            raise Exception('Floor already exists')
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
            raise Exception('Element already exists')
        try:
            db.add_element(
                self.__connection,
                element.element_id,
                element.element_type,
                element.floor_id,
                element.capacity,
                element.position[0],
                element.position[1]
            )
            new_db_row = db.get_element_by_element_id(self.__connection, element.element_id)
            element.db_id = new_db_row[0]
            self.__floors_by_id[element.floor_id].load_element(element)
        except sqlite3.IntegrityError:
            raise Exception(f"Element with id {element.element_id} already exists.")
        except sqlite3.OperationalError:
            raise Exception("Database is unavailable or corrupted.")

