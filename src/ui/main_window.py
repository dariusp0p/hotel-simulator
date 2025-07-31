from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from src.ui.main_menu import MainMenuPage
from src.ui.reservation_admin import ReservationAdminPage
from src.ui.reservation_user import ReservationUserPage
from src.ui.hotel_configurator import HotelConfiguratorPage
from src.service.controller import Controller


class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("Hotel Simulator")
        self.resize(1000, 700)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.main_menu = MainMenuPage(
            on_reservation_click=self.handle_reservation_click,
            on_configurator_click=self.show_hotel_configurator,
        )

        self.reservation_admin = ReservationAdminPage(
            on_back=self.show_main_menu,
            controller=controller
        )
        self.reservation_user = ReservationUserPage(on_back=self.show_main_menu)
        self.hotel_configurator = HotelConfiguratorPage(
            on_back=self.show_main_menu,
            controller=controller
        )

        self.stack.addWidget(self.main_menu)
        self.stack.addWidget(self.reservation_admin)
        self.stack.addWidget(self.reservation_user)
        self.stack.addWidget(self.hotel_configurator)

        self.stack.setCurrentWidget(self.main_menu)

    def show_reservation_admin(self):
        self.stack.setCurrentWidget(self.reservation_admin)

    def show_main_menu(self):
        self.stack.setCurrentWidget(self.main_menu)

    def show_hotel_configurator(self):
        self.stack.setCurrentWidget(self.hotel_configurator)

    def handle_reservation_click(self, is_admin: bool):
        if is_admin:
            self.stack.setCurrentWidget(self.reservation_admin)
        else:
            self.stack.setCurrentWidget(self.reservation_user)
