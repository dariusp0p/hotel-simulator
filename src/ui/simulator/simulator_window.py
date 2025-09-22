from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt

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