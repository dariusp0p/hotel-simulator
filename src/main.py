import sys
import os

from PyQt6.QtWidgets import QApplication
from src.db.database_manager import DatabaseManager
from src.repository.hotel_repository import HotelRepository
from src.repository.reservation_repository import ReservationRepository
from src.service.hotel_service import HotelService
from src.service.reservation_service import ReservationService
from src.ui.main_menu import MainMenuPage
from src.ui.main_window import MainWindow
from src.service.controller import Controller


def main():
    app = QApplication(sys.argv)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "data", "db")

    db_manager = DatabaseManager(
        reservations_db=os.path.join(data_dir, "reservations.db"),
        hotel_db=os.path.join(data_dir, "hotel.db"),
    )

    db_manager.initialize_databases()

    reservations_connection = db_manager.reservations_conn
    hotel_connection = db_manager.hotel_conn

    reservation_repository = ReservationRepository(reservations_connection)
    hotel_repository = HotelRepository(hotel_connection)

    reservation_service = ReservationService(reservation_repository)
    hotel_service = HotelService(hotel_repository)

    controller = Controller(reservation_service, hotel_service)

    window = MainWindow(controller=controller)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
