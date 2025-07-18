from src.db.db_connection import get_connection
from src.db.reservation_model import create_reservation_model
from src.db.room_model import create_room_model



class DatabaseManager:
    def __init__(self, reservations_db, rooms_db):
        self.__reservations_conn = get_connection(reservations_db)
        self.__rooms_conn = get_connection(rooms_db)

    def initialize_databases(self):
        create_reservation_model(self.__reservations_conn)
        # create_room_model(self.__rooms_conn)

    @property
    def reservations_conn(self):
        return self.__reservations_conn

    @property
    def rooms_conn(self):
        return self.__rooms_conn
