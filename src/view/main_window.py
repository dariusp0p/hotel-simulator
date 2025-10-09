from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from src.view.home_window import HomeWindow
from src.view.hotel_configurator.hotel_configurator_window import HotelConfiguratorWindow
from src.view.reservation_manager.reservation_manager_window import ReservationManagerWindow
from src.view.simulator.simulator_window import SimulatorWindow



class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("Hotel Simulator")
        self.resize(1000, 700)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home = HomeWindow(
            on_reservation_manager_click=self.show_reservation_manager,
            on_simulator_click=self.show_simulator,
            on_hotel_configurator_click=self.show_hotel_configurator,
        )

        self.hotel_configurator = HotelConfiguratorWindow(
            on_back=self.show_home,
            controller=controller
        )

        self.reservation_manager = ReservationManagerWindow(
            on_back=self.show_home,
            controller=controller
        )

        self.simulator = SimulatorWindow(
            on_back=self.show_home,
            controller=controller
        )

        self.stack.addWidget(self.home)
        self.stack.addWidget(self.hotel_configurator)
        self.stack.addWidget(self.reservation_manager)
        self.stack.addWidget(self.simulator)

        self.stack.setCurrentWidget(self.home)


    def show_home(self):
        self.stack.setCurrentWidget(self.home)

    def show_hotel_configurator(self):
        self.stack.setCurrentWidget(self.hotel_configurator)

    def show_simulator(self):
        self.stack.setCurrentWidget(self.simulator)

    def show_reservation_manager(self):
        self.stack.setCurrentWidget(self.reservation_manager)


