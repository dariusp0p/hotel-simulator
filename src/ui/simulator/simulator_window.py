from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer
from datetime import datetime

from src.ui.components.top_bar import TopBar
from src.ui.simulator.components.top_left_panel import TopLeftPanel
from src.ui.simulator.components.bottom_left_panel import BottomLeftPanel
from src.ui.simulator.components.hot_bar import HotBar
from src.ui.simulator.components.simulator_canvas import SimulatorCanvas


class SimulatorWindow(QMainWindow):
    def __init__(self, on_back, controller):
        super().__init__()
        self.on_back = on_back
        self.controller = controller

        # Simulation variables
        self.current_date = datetime.now().date()
        self.speed = 1.0
        self.simulation_running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulation_step)

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Hotel Simulator")
        self.resize(1200, 800)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.simulator_canvas = SimulatorCanvas(self.controller)

        self.top_bar = TopBar([
            {"label": "← Back", "callback": self.handle_back},
        ])

        self.top_left_panel = TopLeftPanel()
        self.bottom_left_panel = BottomLeftPanel(self.controller)
        self.hot_bar = HotBar()

        # Connect HotBar signals to handlers
        self.hot_bar.date_changed.connect(self.handle_date_changed)
        self.hot_bar.speed_changed.connect(self.handle_speed_changed)
        self.hot_bar.day_back_btn.clicked.connect(self.handle_day_back)
        self.hot_bar.day_forward_btn.clicked.connect(self.handle_day_forward)
        self.hot_bar.start_btn.clicked.connect(self.handle_start)
        self.hot_bar.stop_btn.clicked.connect(self.handle_stop)

        # Initialize current date
        self.current_date = self.hot_bar.current_date
        self.update_room_availability()

        self.layout = QVBoxLayout(self.main_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.simulator_canvas)

        self.top_bar.setParent(self.main_widget)
        self.top_left_panel.setParent(self.main_widget)
        self.bottom_left_panel.setParent(self.main_widget)
        self.hot_bar.setParent(self.main_widget)

        self.resizeEvent(None)

    def handle_back(self):
        if self.on_back:
            self.on_back()

    def handle_date_changed(self, date):
        self.current_date = date
        self.update_room_availability()
        print(f"Date changed to: {date.toString('yyyy-MM-dd')}")

    def handle_speed_changed(self, speed):
        self.speed = speed
        print(f"Speed changed to: {speed}x")
        if self.simulation_running:
            self.adjust_timer_interval()

    def handle_day_back(self):
        if self.current_date:
            self.current_date = self.current_date.addDays(-1)
            self.hot_bar.current_date = self.current_date
            self.hot_bar.date_btn.setText(f"Current Date: {self.current_date.toString('yyyy-MM-dd')}")
            self.update_room_availability()
            print(f"Date moved back to: {self.current_date.toString('yyyy-MM-dd')}")

    def handle_day_forward(self):
        if self.current_date:
            self.current_date = self.current_date.addDays(1)
            self.hot_bar.current_date = self.current_date
            self.hot_bar.date_btn.setText(f"Current Date: {self.current_date.toString('yyyy-MM-dd')}")
            self.update_room_availability()
            print(f"Date moved forward to: {self.current_date.toString('yyyy-MM-dd')}")

    def handle_start(self):
        self.simulation_running = True
        self.hot_bar.start_btn.setEnabled(False)
        self.hot_bar.stop_btn.setEnabled(True)
        self.adjust_timer_interval()
        self.timer.start()
        print(f"Starting simulation at {self.speed}x speed")

    def handle_stop(self):
        self.simulation_running = False
        self.hot_bar.start_btn.setEnabled(True)
        self.hot_bar.stop_btn.setEnabled(False)
        self.timer.stop()
        print("Stopping simulation")

    def adjust_timer_interval(self):
        # Base interval is 1000ms (1 second)
        # Adjust based on speed factor
        interval = int(1000 / self.speed)
        self.timer.setInterval(max(50, interval))  # Minimum 50ms for UI responsiveness

    def simulation_step(self):
        # This will be called according to the timer interval
        # Advance the simulation by one time step
        self.handle_day_forward()

    def update_room_availability(self):
        if self.current_date:
            self.simulator_canvas.update_room_availability(self.current_date)
            self.simulator_canvas.update()

    def resizeEvent(self, event):
        margin = 10

        # Position top bar
        self.top_bar.setGeometry(
            margin,
            margin,
            self.width() - 2 * margin,
            self.top_bar.height()
        )

        top_margin = self.top_bar.height() + 2 * margin
        panel_width = 250

        # Position top left panel
        self.top_left_panel.setGeometry(
            margin,
            top_margin,
            panel_width,
            (self.height() - top_margin - margin) // 2
        )

        # Position bottom left panel
        self.bottom_left_panel.setGeometry(
            margin,
            top_margin + (self.height() - top_margin - margin) // 2 + margin,
            panel_width,
            (self.height() - top_margin - margin) // 2 - margin
        )

        # Position hot bar
        self.hot_bar.setGeometry(
            panel_width + 2 * margin,
            self.height() - self.hot_bar.height() - margin,
            self.width() - panel_width - 3 * margin,
            self.hot_bar.height()
        )