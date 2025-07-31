import sys
import os

from PyQt6.QtWidgets import QApplication
from src.db.database_manager import DatabaseManager
from src.repository.reservation_repository import ReservationRepository
from src.service.reservation_service import ReservationService
from src.ui.main_menu import MainMenuPage
from src.ui.main_window import MainWindow


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

    reservation_repository = ReservationRepository(reservations_connection)
    reservation_service = ReservationService(reservation_repository)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
