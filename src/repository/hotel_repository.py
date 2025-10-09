import sqlite3
import networkx as nx

from src.db import database_operations as db
from src.domain.floor import Floor
from src.domain.floor_element import FloorElement
from src.domain.room import Room
from src.utilities.exceptions import FloorAlreadyExistsError, FloorNotFoundError, DatabaseError, ElementNotFoundError


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
        """Loads all data from the database into the repository."""
        try:
            floors = db.select_all_floors(self.__connection)

            for db_id, name, level in floors:
                floor = Floor(db_id, name, level)
                self.__floors_by_name[floor.name] = floor
                self.__floors_by_id[floor.db_id] = floor

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
                    self.__graph.add_node(element.db_id, element=element)
                    self.handle_connections(element)

            self.refresh_staircases()

        except sqlite3.OperationalError:
            raise DatabaseError("Database is unavailable or corrupted!")


    # Getters
    def get_all_floors(self) -> list[Floor]:
        """Returns a list of all floors. Theta(1) complexity."""
        return list(self.__floors_by_id.values())

    def get_floor_by_id(self, floor_id: int) -> Floor:
        """Returns the floor with the specified ID. Theta(1) complexity."""
        if floor_id not in self.__floors_by_id:
            raise FloorNotFoundError(f"Floor {floor_id} not found!")
        return self.__floors_by_id[floor_id]

    def get_floor_grid(self, floor_id: int) -> dict:
        """Returns a dictionary representing the grid of the specified floor. Theta(1) complexity."""
        if floor_id not in self.__floors_by_id:
            raise FloorNotFoundError(f"Floor {floor_id} not found!")
        return self.__floors_by_id[floor_id].grid

    def get_floor_id(self, floor_name: str) -> int:
        """Returns the ID of the specified floor. Theta(1) complexity."""
        if floor_name not in self.__floors_by_name:
            raise FloorNotFoundError(f"Floor {floor_name} not found!")
        return self.__floors_by_name[floor_name].db_id

    def get_elements_by_floor_id(self, floor_id: int) -> dict:
        """Returns a dictionary of elements for the specified floor ID. Theta(1) complexity."""
        if floor_id not in self.__floors_by_id:
            raise FloorNotFoundError(f"Floor {floor_id} not found!")
        return self.__floors_by_id[floor_id].elements

    def get_room_by_id(self, room_id: int) -> Room:
        """Returns the room with the specified ID. Theta(1) complexity."""
        room = self.__rooms_by_id.get(room_id)
        if not room:
            raise ElementNotFoundError(f"Room {room_id} not found!")
        return room

    def get_room_by_number(self, room_number: str) -> Room:
        """Returns the room with the specified number. O(R) complexity."""
        for room in self.__rooms_by_id.values():
            if room.number == room_number:
                return room
        raise ElementNotFoundError(f"Room with number {room_number} not found!")

    def get_rooms_by_capacity(self, capacity: int) -> list[Room]:
        """Returns a list of rooms that can accommodate the specified number of guests. Theta(1) complexity."""
        return self.__rooms_by_capacity.get(capacity, [])

    def get_connections_by_floor_id(self, floor_id):
        """Returns a list of connections (edges) between elements on the specified floor. O(E) complexity."""
        floor = self.__floors_by_id[floor_id]
        element_ids = set(floor.elements.keys())
        connections = set()
        for u, v in self.__graph.edges():
            if u in element_ids and v in element_ids:
                connections.add(tuple(sorted((u, v))))
        return list(connections)

    def get_all_connections(self):
        return list(self.__graph.edges)


    # CRUD

    # Floors
    def add_floor(self, floor: Floor):
        """Adds a new floor to the repository and the database. Theta(1) complexity."""
        if floor.db_id in self.__floors_by_id or floor.name in self.__floors_by_name:
            raise FloorAlreadyExistsError(f"Floor {floor.name} already exists!")
        try:
            db_id = db.insert_floor(self.__connection, floor.name, floor.level)
            floor.db_id = db_id
            self.__floors_by_id[floor.db_id] = floor
            self.__floors_by_name[floor.name] = floor
            self.refresh_staircases()
            return db_id
        except sqlite3.IntegrityError:
            raise DatabaseError(f"Database integrity error when adding floor {floor.name}!")
        except sqlite3.OperationalError:
            raise DatabaseError("Database is unavailable or corrupted!")

    def move_floor(self, floor_id, new_level):
        """Changes the level of the specified floor. Theta(1) complexity."""
        if floor_id not in self.__floors_by_id:
            raise FloorNotFoundError(f"Floor {floor_id} not found!")

        try:
            db.update_floor_level(self.__connection, floor_id, new_level)
            floor = self.__floors_by_id[floor_id]
            floor.level = new_level
            self.refresh_staircases()
        except sqlite3.IntegrityError:
            raise DatabaseError(f"Database integrity error when moving floor {floor_id}!")
        except sqlite3.OperationalError:
            raise DatabaseError("Database is unavailable or corrupted!")

    def rename_floor(self, old_name, new_name):
        """Renames the specified floor. Theta(1) complexity."""
        if new_name in self.__floors_by_name:
            raise FloorAlreadyExistsError(f"Floor with name {new_name} already exists!")
        floor = self.__floors_by_name.get(old_name)
        if not floor:
            raise FloorNotFoundError(f"Floor {old_name} not found!")

        try:
            db.update_floor_name(self.__connection, floor.db_id, new_name)
            del self.__floors_by_name[old_name]
            floor.name = new_name
            self.__floors_by_name[new_name] = floor
        except sqlite3.IntegrityError:
            raise DatabaseError(f"Database integrity error when renaming floor {old_name}!")
        except sqlite3.OperationalError:
            raise DatabaseError("Database is unavailable or corrupted!")

    def remove_floor(self, floor_id):
        """Removes the specified floor from the repository and the database. Theta(1) complexity."""
        if floor_id not in self.__floors_by_id:
            raise FloorNotFoundError(f"Floor {floor_id} not found!")

        try:
            db.delete_floor(self.__connection, floor_id)
            floor = self.__floors_by_id[floor_id]
            del self.__floors_by_id[floor.db_id]
            del self.__floors_by_name[floor.name]
            self.refresh_staircases()
        except sqlite3.IntegrityError:
            raise DatabaseError(f"Database integrity error when deleting floor {floor_id}!")
        except sqlite3.OperationalError:
            raise DatabaseError("Database is unavailable or corrupted!")


    # Floor elements
    def add_element(self, element):
        """Adds a new element to the repository and the database. Theta(1) complexity."""
        try:
            if element.type == "room":
                db_id = db.insert_element(
                    self.__connection, element.type, element.floor_id, element.position[0],
                    element.position[1], element.number, element.capacity, element.price_per_night,
                )
            else:
                db_id = db.insert_element(
                    self.__connection, element.type, element.floor_id, element.position[0],
                    element.position[1], "",0,0,
                )
            element.db_id = db_id

            if element.floor_id not in self.__floors_by_id:
                raise FloorNotFoundError(f"Floor {element.floor_id} not found!")

            floor = self.__floors_by_id[element.floor_id]
            floor.add_element(element)

            self.__graph.add_node(element.db_id, element=element)
            self.handle_connections(element)

            if element.type == "room":
                self.__rooms_by_id[element.db_id] = element
                if element.capacity not in self.__rooms_by_capacity:
                    self.__rooms_by_capacity[element.capacity] = []
                self.__rooms_by_capacity[element.capacity].append(element)

            return db_id

        except sqlite3.IntegrityError:
            raise DatabaseError(f"Element with id {element.db_id} already exists!")
        except sqlite3.OperationalError:
            raise DatabaseError("Database is unavailable or corrupted!")

    def move_element(self, element_id, new_position):
        """Moves the specified element to a new position. O(F) complexity."""
        try:
            db.update_element_position(self.__connection, element_id, new_x=new_position[0], new_y=new_position[1])
            for floor in self.__floors_by_id.values():
                if element_id in floor.elements:
                    floor.move_element(element_id, new_position)
                    self.handle_connections(floor.elements[element_id])
                    break
        except sqlite3.IntegrityError:
            raise DatabaseError(f"Database integrity error when moving element {element_id}!")
        except sqlite3.OperationalError:
            raise DatabaseError("Database is unavailable or corrupted!")
        except ElementNotFoundError as e:
            raise e

    def edit_room(self, element_id, new_number, new_capacity, new_price_per_night):
        """Edits the properties of the specified room. O(F) complexity."""
        try:
            db.update_element(self.__connection, element_id, new_number, new_capacity, new_price_per_night)
            for floor in self.__floors_by_id.values():
                if element_id in floor.elements:
                    floor.edit_room(element_id, new_number, new_capacity, new_price_per_night)
                    break
        except sqlite3.IntegrityError:
            raise DatabaseError(f"Database integrity error when editing room {element_id}!")
        except sqlite3.OperationalError:
            raise DatabaseError("Database is unavailable or corrupted!")
        except ElementNotFoundError as e:
            raise e

    def remove_element(self, element_id, element_type, floor_id):
        """Removes the specified element from the repository and the database. O(RC) complexity."""
        try:
            self.delete_all_connections(element_id)
            self.__graph.remove_node(element_id)
            db.delete_element(self.__connection, element_id)

            if element_type == "room" and element_id in self.__rooms_by_id:
                element = self.__rooms_by_id[element_id]
                del self.__rooms_by_id[element_id]
                if element.capacity in self.__rooms_by_capacity:
                    self.__rooms_by_capacity[element.capacity] = [
                        room for room in self.__rooms_by_capacity[element.capacity]
                        if room.db_id != element_id
                    ]
                    if not self.__rooms_by_capacity[element.capacity]:
                        del self.__rooms_by_capacity[element.capacity]

            floor = self.__floors_by_id[floor_id]
            floor.delete_element(element_id)
        except sqlite3.OperationalError:
            raise DatabaseError("Database is unavailable or corrupted!")
        except ElementNotFoundError as e:
            raise e



    def handle_connections(self, element: FloorElement):
        if element.db_id not in self.__graph:
            raise ElementNotFoundError(f"Element {element.db_id} not found in graph!")

        self.delete_all_connections(element.db_id)

        neighbours = self.__floors_by_id[element.floor_id].get_element_neighbors(element.db_id).values()
        if not neighbours:
            return
        if element.type == "staircase":
            for neighbour in neighbours:
                if (neighbour.type == "staircase" or neighbour.type == "hallway"
                        or (neighbour.type == "room" and self.__graph.degree(neighbour.db_id) == 0)):
                    self.add_connection(element.db_id, neighbour.db_id)
            for floor in self.__floors_by_id.values():
                if (floor.db_id != element.floor_id and
                        abs(floor.level - self.__floors_by_id[element.floor_id].level) == 1):
                    for other_element in floor.elements.values():
                        if other_element.type == "staircase" and other_element.position == element.position:
                            self.add_connection(element.db_id, other_element.db_id)
        elif element.type == "hallway":
            for neighbour in neighbours:
                if (neighbour.type == "staircase" or neighbour.type == "hallway"
                        or (neighbour.type == "room" and self.__graph.degree(neighbour.db_id) == 0)):
                    self.add_connection(element.db_id, neighbour.db_id)
        elif element.type == "room":
            for neighbour in neighbours:
                if neighbour.type == "hallway":
                    self.add_connection(element.db_id, neighbour.db_id)
                    break
        else:
            return

    def add_connection(self, from_id, to_id):
        self.__graph.add_edge(from_id, to_id)

    def delete_all_connections(self, element_id):
        self.__graph.remove_edges_from(list(self.__graph.edges(element_id)))

    def refresh_staircases(self):
        for floor in self.__floors_by_id.values():
            for element in floor.elements.values():
                if element.type == "staircase":
                    self.handle_connections(element)


