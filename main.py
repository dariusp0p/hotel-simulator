import sys
import os
from PyQt6.QtWidgets import QApplication

from src.model.database.database_manager import DatabaseManager
from src.model.repository.hotel_repository import HotelRepository
from src.model.repository.reservation_repository import ReservationRepository
from src.model.service.hotel_service import HotelService
from src.model.service.reservation_service import ReservationService
from src.controller.controller import Controller
from src.view.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data", "db")

    db_manager = DatabaseManager(os.path.join(data_dir, "hotel_simulator.db"))
    db_manager.initialize_database()
    connection = db_manager.conn

    reservation_repository = ReservationRepository(connection)
    hotel_repository = HotelRepository(connection)

    reservation_service = ReservationService(reservation_repository)
    hotel_service = HotelService(hotel_repository)

    controller = Controller(reservation_service, hotel_service)

    window = MainWindow(controller=controller)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
