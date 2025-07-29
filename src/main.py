import sys
import os

from PyQt6.QtWidgets import QApplication
from src.db.database_manager import DatabaseManager
from src.repository.reservation_repository import ReservationRepository
from src.service.reservation_service import ReservationService
from src.ui.gui import MainWindow


def main():
    app = QApplication(sys.argv)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, '..', 'data', 'db')

    db_manager = DatabaseManager(
        reservations_db=os.path.join(data_dir, 'reservations.db'),
        rooms_db=os.path.join(data_dir, 'rooms.db'),
    )

    db_manager.initialize_databases()

    reservations_connection = db_manager.reservations_conn

    reservation_repository = ReservationRepository(reservations_connection)
    reservation_service = ReservationService(reservation_repository)

    window = MainWindow(reservation_service)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()