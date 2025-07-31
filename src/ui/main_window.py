from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from src.ui.main_menu import MainMenuPage
from src.ui.reservation_admin import ReservationAdminPage
from src.ui.reservation_user import ReservationUserPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hotel Simulator")
        self.resize(1000, 700)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.main_menu = MainMenuPage(
            on_reservation_click=self.handle_reservation_click
        )
        self.reservation_admin = ReservationAdminPage(on_back=self.show_main_menu)
        self.reservation_user = ReservationUserPage(on_back=self.show_main_menu)

        self.stack.addWidget(self.main_menu)
        self.stack.addWidget(self.reservation_admin)
        self.stack.addWidget(self.reservation_user)

        self.stack.setCurrentWidget(self.main_menu)

    def show_reservation_admin(self):
        self.stack.setCurrentWidget(self.reservation_admin)

    def show_main_menu(self):
        self.stack.setCurrentWidget(self.main_menu)

    def handle_reservation_click(self, is_admin: bool):
        if is_admin:
            self.stack.setCurrentWidget(self.reservation_admin)
        else:
            self.stack.setCurrentWidget(self.reservation_user)
