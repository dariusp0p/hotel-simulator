import sqlite3
import networkx as nx

from src.domain.floor_element import FloorElement
from src.domain.room import Room
from src.domain.floor import Floor
from src.db import hotel_model as db



class HotelRepository:
    def __init__(self, connection):
        self.__connection = connection

        self.__graph = nx.Graph()

        self.__floors_by_id = {}
        self.__floors_by_name = {}

        self.__rooms_by_id = {}
        self.__rooms_by_capacity = {}

        self.load_from_db()


    @property
    def connection(self):
        return self.__connection


    # Data persistence
    def load_from_db(self):
        floors = db.select_all_floors(self.__connection)

        for db_id, name, level in floors:
            floor = Floor(db_id, name, level)
            elements = db.select_elements_by_floor_id(self.__connection, db_id)
            for row in elements:
                if row[1] == "room":
                    element = Room(
                        db_id=row[0],
                        type=row[1],
                        floor_id=row[2],
                        position=(row[3], row[4]),
                        number=row[5],
                        capacity=row[6],
                        price_per_night=row[7]
                    )
                    self.__rooms_by_id[element.db_id] = element
                    if element.capacity not in self.__rooms_by_capacity:
                        self.__rooms_by_capacity[element.capacity] = []
                    self.__rooms_by_capacity[element.capacity].append(element)
                else:
                    element = FloorElement(
                        db_id=row[0],
                        type=row[1],
                        floor_id=row[2],
                        position=(row[3], row[4])
                    )
                floor.add_element(element)
                self.__graph.add_node(element.db_id)

            self.__floors_by_name[floor.name] = floor
            self.__floors_by_id[floor.db_id] = floor

        connections = db.select_all_connections(self.__connection)
        for element_id_1, element_id_2 in connections:
            self.__graph.add_edge(element_id_1, element_id_2)


    # Getters
    def get_all_floors(self):
        return list(self.__floors_by_id.values())

    def get_floor_grid(self, floor_name):
        return self.__floors_by_name[floor_name].grid

    def get_floor_id(self, floor_name):
        return self.__floors_by_name[floor_name].db_id

    def get_graph(self):
        return self.__global_graph

    def find_path(self, from_id, to_id):
        if not self.__global_graph.has_node(from_id) or not self.__global_graph.has_node(to_id):
            raise Exception("Invalid element IDs")
        return nx.shortest_path(self.__global_graph, from_id, to_id)

    def get_elements_by_floor_id(self, floor_id):
        return self.__floors_by_id[floor_id].elements


    # CRUD

    # Floors
    def add_floor(self, floor):
        if floor.db_id in self.__floors_by_id or floor.name in self.__floors_by_name:
            raise Exception("Floor already exists")
        try:
            db_id = db.insert_floor(self.__connection, floor.name, floor.level)
            floor.db_id = db_id
            self.__floors_by_id[floor.db_id] = floor
            self.__floors_by_name[floor.name] = floor
        except sqlite3.IntegrityError:
            raise Exception(f"NONO")
        except sqlite3.OperationalError:
            raise Exception("Database is unavailable or corrupted.")

    def move_floor(self, floor_id, new_level):
        if floor_id not in self.__floors_by_id:
            raise Exception("Floor not found")

        db.update_floor_level(self.__connection, floor_id, new_level)

        floor = self.__floors_by_id[floor_id]
        floor.level = new_level

        self.__floors_by_id[floor.db_id] = floor
        self.__floors_by_name[floor.name] = floor

    def rename_floor(self, old_name, new_name):
        if new_name in self.__floors_by_name:
            raise Exception("New floor name already exists")
        floor = self.__floors_by_name.get(old_name)
        if not floor:
            raise Exception("Old floor not found")

        db.update_floor_name(self.__connection, floor.db_id, new_name)

        del self.__floors_by_name[old_name]
        floor.name = new_name
        self.__floors_by_name[new_name] = floor

    def add_element_to_floor(self, element, floor_id):
        if floor_id not in self.__floors_by_id:
            raise Exception("Floor not found")

        floor = self.__floors_by_id[floor_id]
        floor.add_element(element)

        self.__floors_by_id[floor.db_id] = floor
        self.__floors_by_name[floor.name] = floor

    def remove_floor(self, floor_id):
        if floor_id not in self.__floors_by_id:
            raise Exception("Floor not found")

        db.delete_floor(self.__connection, floor_id)

        floor = self.__floors_by_id[floor_id]

        del self.__floors_by_id[floor.db_id]
        del self.__floors_by_name[floor.name]



    # Floor elements
    def add_element(self, element):
        try:
            if element.type == "room":
                db_id = db.insert_element(
                    self.__connection,
                    element.type,
                    element.floor_id,
                    element.position[0],
                    element.position[1],
                    element.number,
                    element.capacity,
                    element.price_per_night,
                )
            else:
                db_id = db.insert_element(
                    self.__connection,
                    element.type,
                    element.floor_id,
                    element.position[0],
                    element.position[1],
                    "",
                    0,
                    0,
                )

            element.db_id = db_id

            self.__graph.add_node(element.db_id)

            if element.type == "room":
                self.__rooms_by_id[element.db_id] = element
                if element.capacity not in self.__rooms_by_capacity:
                    self.__rooms_by_capacity[element.capacity] = []
                self.__rooms_by_capacity[element.capacity].append(element)

        except sqlite3.IntegrityError:
            raise Exception(f"Element with id {element.db_id} already exists.")
        except sqlite3.OperationalError:
            raise Exception("Database is unavailable or corrupted.")

    def move_element(self, element_id, new_position):
        db.update_element_position(self.__connection, element_id, new_x=new_position[0], new_y=new_position[1])
        for floor in self.__floors_by_id.values():
            if element_id in floor.elements:
                floor.move_element(element_id, new_position)

                element = floor.elements[element_id]
                if element.db_id in self.__rooms_by_id:
                    self.__rooms_by_id[element.db_id].position = new_position

                if hasattr(element, 'capacity') and element.capacity in self.__rooms_by_capacity:
                    for room in self.__rooms_by_capacity[element.capacity]:
                        if room.db_id == element_id:
                            room.position = new_position
                            break
                break

    def edit_room(self, element_id, new_number, new_capacity, new_price_per_night):
        db.update_element(self.__connection, element_id, new_number, new_capacity, new_price_per_night)
        for floor in self.__floors_by_id.values():
            if element_id in floor.elements:
                element = floor.elements[element_id]
                element.capacity = new_capacity
                element.number = new_number
                element.price_per_night = new_price_per_night
                break

    def remove_element(self, element):
        if element.db_id not in self.__graph:
            raise Exception("Element not found")

        self.__graph.remove_node(element.db_id)
        db.delete_element(self.__connection, element.db_id)

        floor = self.__floors_by_id[element.floor_id]
        floor.delete_element(element)



    def connect_elements(self, from_id, to_id):
        db.add_connection(self.__connection, from_id, to_id)
        db.add_connection(self.__connection, to_id, from_id)
        self.__global_graph.add_edge(from_id, to_id)
