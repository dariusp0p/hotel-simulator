from PyQt6.QtCore import QTimer, QDate
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout
)

from src.view.components.top_bar import TopBar
from src.view.simulator.components.top_left_panel import TopLeftPanel
from src.view.simulator.components.bottom_left_panel import BottomLeftPanel
from src.view.simulator.components.hot_bar import HotBar
from src.view.simulator.components.simulator_canvas import SimulatorCanvas
from src.utilities.reservation_generator import ReservationGenerator


class SimulatorWindow(QMainWindow):
    """Simulator window."""
    def __init__(self, onBack, controller):
        super().__init__()
        self.onBack = onBack
        self.controller = controller
        self.reservationGenerator = ReservationGenerator(controller)

        self.currentDate = QDate.currentDate()
        self.speed = 1.0
        self.simulationRunning = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulationStep)

        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Hotel Simulator")
        self.resize(1200, 800)

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)

        self.simulatorCanvas = SimulatorCanvas(self.controller)

        self.topBar = TopBar([
            {"label": "← Back", "callback": self.handleBack},
        ])

        self.topLeftPanel = TopLeftPanel(controller=self.controller, generateReservationsCallback=self.generateReservations)
        self.bottomLeftPanel = BottomLeftPanel(self.controller)
        self.hotBar = HotBar()

        self.hotBar.dateChanged.connect(self.handleDateChanged)
        self.hotBar.speedChanged.connect(self.handleSpeedChanged)
        self.hotBar.dayBackBtn.clicked.connect(self.handleDayBack)
        self.hotBar.dayForwardBtn.clicked.connect(self.handleDayForward)
        self.hotBar.startBtn.clicked.connect(self.handleStart)
        self.hotBar.stopBtn.clicked.connect(self.handleStop)

        self.currentDate = self.hotBar.currentDate
        self.updateRoomAvailability()

        self.layout = QVBoxLayout(self.mainWidget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.simulatorCanvas)

        self.topBar.setParent(self.mainWidget)
        self.topLeftPanel.setParent(self.mainWidget)
        self.bottomLeftPanel.setParent(self.mainWidget)
        self.hotBar.setParent(self.mainWidget)

        self.simulatorCanvas.repaintCompleted = self.topLeftPanel.updateStats

        self.resizeEvent(None)

    def handleBack(self):
        if self.onBack:
            self.onBack()

    def handleDateChanged(self, date):
        self.currentDate = date
        self.updateRoomAvailability()

    def handleSpeedChanged(self, speed):
        self.speed = speed
        if self.simulationRunning:
            self.adjustTimerInterval()

    def handleDayBack(self):
        if self.currentDate:
            self.currentDate = self.currentDate.addDays(-1)
            self.hotBar.currentDate = self.currentDate
            self.hotBar.dateBtn.setText(f"Current Date: {self.currentDate.toString('yyyy-MM-dd')}")
            self.updateRoomAvailability()

    def handleDayForward(self):
        if self.currentDate:
            self.currentDate = self.currentDate.addDays(1)
            self.hotBar.currentDate = self.currentDate
            self.hotBar.dateBtn.setText(f"Current Date: {self.currentDate.toString('yyyy-MM-dd')}")
            self.updateRoomAvailability()

    def handleStart(self):
        self.simulationRunning = True
        self.hotBar.startBtn.setEnabled(False)
        self.hotBar.stopBtn.setEnabled(True)
        self.adjustTimerInterval()
        self.timer.start()

    def handleStop(self):
        self.simulationRunning = False
        self.hotBar.startBtn.setEnabled(True)
        self.hotBar.stopBtn.setEnabled(False)
        self.timer.stop()

    def adjustTimerInterval(self):
        interval = int(1000 / self.speed)
        self.timer.setInterval(max(50, interval))

    def simulationStep(self):
        self.handleDayForward()

    def updateRoomAvailability(self):
        if self.currentDate:
            self.simulatorCanvas.updateRoomAvailability(self.currentDate)
            self.simulatorCanvas.update()
            # Update stats when room availability changes
            self.topLeftPanel.updateStats()

    def generateReservations(self, fromDate, toDate, occupancyPercentage):
        createdCount = self.reservationGenerator.generate_reservations(fromDate, toDate, occupancyPercentage)
        self.updateRoomAvailability()
        return createdCount

    def resizeEvent(self, event):
        margin = 10

        self.topBar.setGeometry(
            margin,
            margin,
            self.width() - 2 * margin,
            self.topBar.height()
        )

        topMargin = self.topBar.height() + 2 * margin
        panelWidth = 250

        # Make topLeftPanel larger
        topPanelHeight = int((self.height() - topMargin - margin) * 0.55)  # 55% of available height

        self.topLeftPanel.setGeometry(
            margin,
            topMargin,
            panelWidth,
            topPanelHeight
        )

        # Make bottomLeftPanel smaller
        bottomPanelHeight = int((self.height() - topMargin - margin) * 0.45 - margin)  # 45% of available height

        self.bottomLeftPanel.setGeometry(
            margin,
            topMargin + topPanelHeight + margin,
            panelWidth,
            bottomPanelHeight
        )

        self.hotBar.setGeometry(
            panelWidth + 2 * margin,
            self.height() - self.hotBar.height() - margin,
            self.width() - panelWidth - 3 * margin,
            self.hotBar.height()
        )
