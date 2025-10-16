from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from src.view.home_window import HomeWindow
from src.view.hotel_configurator.hotel_configurator_window import HotelConfiguratorWindow
from src.view.reservation_manager.reservation_manager_window import ReservationManagerWindow
from src.view.simulator.simulator_window import SimulatorWindow


class MainWindow(QMainWindow):
    """Main application window."""
    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("Hotel Simulator")
        self.resize(1000, 700)

        self.controller = controller
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home = HomeWindow(
            onReservationManagerClick=self.showReservationManager,
            onSimulatorClick=self.showSimulator,
            onHotelConfiguratorClick=self.showHotelConfigurator,
        )

        self.hotelConfigurator = HotelConfiguratorWindow(
            onBack=self.showHome,
            controller=controller
        )

        self.reservationManager = ReservationManagerWindow(
            onBack=self.showHome,
            controller=controller
        )

        self.simulator = SimulatorWindow(
            onBack=self.showHome,
            controller=controller
        )

        self.stack.addWidget(self.home)
        self.stack.addWidget(self.hotelConfigurator)
        self.stack.addWidget(self.reservationManager)
        self.stack.addWidget(self.simulator)

        self.stack.setCurrentWidget(self.home)

    def showHome(self):
        self.controller.clear_stacks()
        self.stack.setCurrentWidget(self.home)

    def showHotelConfigurator(self):
        self.hotelConfigurator.sideBar.populateFloorList()
        self.hotelConfigurator.updateUndoRedoButtons()
        self.hotelConfigurator.ensureSelectedFloorExists()
        self.hotelConfigurator.refreshGrid()
        self.stack.setCurrentWidget(self.hotelConfigurator)

    def showSimulator(self):
        self.stack.setCurrentWidget(self.simulator)

    def showReservationManager(self):
        self.stack.setCurrentWidget(self.reservationManager)
