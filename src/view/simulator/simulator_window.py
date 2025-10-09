from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout
)
from PyQt6.QtCore import Qt, QTimer
from datetime import datetime

from src.view.components.top_bar import TopBar
from src.view.simulator.components.top_left_panel import TopLeftPanel
from src.view.simulator.components.bottom_left_panel import BottomLeftPanel
from src.view.simulator.components.hot_bar import HotBar
from src.view.simulator.components.simulator_canvas import SimulatorCanvas
from src.utilities.reservation_generator import ReservationGenerator


class SimulatorWindow(QMainWindow):
    def __init__(self, on_back, controller):
        super().__init__()
        self.on_back = on_back
        self.controller = controller
        self.reservation_generator = ReservationGenerator(controller)

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

        self.top_left_panel = TopLeftPanel(controller=self.controller, generate_reservations_callback=self.generate_reservations)
        self.bottom_left_panel = BottomLeftPanel(self.controller)
        self.hot_bar = HotBar()

        self.hot_bar.date_changed.connect(self.handle_date_changed)
        self.hot_bar.speed_changed.connect(self.handle_speed_changed)
        self.hot_bar.day_back_btn.clicked.connect(self.handle_day_back)
        self.hot_bar.day_forward_btn.clicked.connect(self.handle_day_forward)
        self.hot_bar.start_btn.clicked.connect(self.handle_start)
        self.hot_bar.stop_btn.clicked.connect(self.handle_stop)

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

        self.simulator_canvas.repaint_completed = self.top_left_panel.update_stats

        self.resizeEvent(None)

    def handle_back(self):
        if self.on_back:
            self.on_back()

    def handle_date_changed(self, date):
        self.current_date = date
        self.update_room_availability()

    def handle_speed_changed(self, speed):
        self.speed = speed
        if self.simulation_running:
            self.adjust_timer_interval()

    def handle_day_back(self):
        if self.current_date:
            self.current_date = self.current_date.addDays(-1)
            self.hot_bar.current_date = self.current_date
            self.hot_bar.date_btn.setText(f"Current Date: {self.current_date.toString('yyyy-MM-dd')}")
            self.update_room_availability()

    def handle_day_forward(self):
        if self.current_date:
            self.current_date = self.current_date.addDays(1)
            self.hot_bar.current_date = self.current_date
            self.hot_bar.date_btn.setText(f"Current Date: {self.current_date.toString('yyyy-MM-dd')}")
            self.update_room_availability()

    def handle_start(self):
        self.simulation_running = True
        self.hot_bar.start_btn.setEnabled(False)
        self.hot_bar.stop_btn.setEnabled(True)
        self.adjust_timer_interval()
        self.timer.start()

    def handle_stop(self):
        self.simulation_running = False
        self.hot_bar.start_btn.setEnabled(True)
        self.hot_bar.stop_btn.setEnabled(False)
        self.timer.stop()

    def adjust_timer_interval(self):
        interval = int(1000 / self.speed)
        self.timer.setInterval(max(50, interval))

    def simulation_step(self):
        self.handle_day_forward()

    def update_room_availability(self):
        if self.current_date:
            self.simulator_canvas.update_room_availability(self.current_date)
            self.simulator_canvas.update()
            # Update stats when room availability changes
            self.top_left_panel.update_stats()

    def generate_reservations(self, from_date, to_date, occupancy_percentage):
        created_count = self.reservation_generator.generate_reservations(from_date, to_date, occupancy_percentage)
        self.update_room_availability()
        return created_count

    def resizeEvent(self, event):
        margin = 10

        self.top_bar.setGeometry(
            margin,
            margin,
            self.width() - 2 * margin,
            self.top_bar.height()
        )

        top_margin = self.top_bar.height() + 2 * margin
        panel_width = 250

        # Make top_left_panel larger
        top_panel_height = int((self.height() - top_margin - margin) * 0.55)  # 55% of available height

        self.top_left_panel.setGeometry(
            margin,
            top_margin,
            panel_width,
            top_panel_height
        )

        # Make bottom_left_panel smaller
        bottom_panel_height = int((self.height() - top_margin - margin) * 0.45 - margin)  # 45% of available height

        self.bottom_left_panel.setGeometry(
            margin,
            top_margin + top_panel_height + margin,
            panel_width,
            bottom_panel_height
        )

        self.hot_bar.setGeometry(
            panel_width + 2 * margin,
            self.height() - self.hot_bar.height() - margin,
            self.width() - panel_width - 3 * margin,
            self.hot_bar.height()
        )