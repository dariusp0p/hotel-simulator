from src.db.db_connection import get_connection
from src.db.reservation_model import create_reservation_model
from src.db.hotel_model import create_hotel_model



class DatabaseManager:
    def __init__(self, reservations_db, hotel_db):
        self.__reservations_conn = get_connection(reservations_db)
        self.__hotel_conn = get_connection(hotel_db)

    def initialize_databases(self):
        create_reservation_model(self.__reservations_conn)
        create_hotel_model(self.__hotel_conn)

    @property
    def reservations_conn(self):
        return self.__reservations_conn

    @property
    def hotel_conn(self):
        return self.__hotel_conn
