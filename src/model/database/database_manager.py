import sqlite3
from src.model.database.database_operations import create_hotel_simulator_model


class DatabaseManager:
    """
    Manages the database connection and initialization.
    """

    def __init__(self, db_path: str):
        self.__conn = get_connection(db_path)

    def initialize_database(self):
        create_hotel_simulator_model(self.__conn)

    @property
    def conn(self):
        return self.__conn


def get_connection(db_path: str) -> sqlite3.Connection:
    """
    Establishes and returns a connection to a database.
    :param db_path:
    :return:
    """
    return get_sqlite_connection(db_path)

def get_sqlite_connection(db_path: str) -> sqlite3.Connection:
    """
    Establishes and returns a connection to the SQLite database.
    :param db_path:
    :return:
    """
    return sqlite3.connect(db_path)
