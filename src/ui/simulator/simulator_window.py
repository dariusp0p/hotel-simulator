from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from src.ui.components.top_bar import TopBar

class SimulatorWindow(QMainWindow):
    def __init__(self, on_back=None, controller=None):
        super().__init__()
        self.on_back = on_back
        self.controller = controller

        self.setWindowTitle("Hotel 3D Graph Simulator")
        self.resize(1200, 800)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.top_bar = TopBar([
            {"label": "← Back", "callback": self.handle_back},
            {"label": "↩ Undo", "callback": self.undo_action},
            {"label": "↪ Redo", "callback": self.redo_action},
        ])
        self.layout.addWidget(self.top_bar)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.plot_3d_hotel()

    def plot_3d_hotel(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='3d')

        # Collect all elements and their positions
        floors = self.controller.hotel_service.get_all_floors_sorted_by_level()
        pos = {}
        for floor in floors:
            z = floor.level
            elements = self.controller.hotel_service.get_elements_by_floor_id(floor.db_id)
            for el in elements:
                x, y = el.position
                pos[el.db_id] = (x, y, z)

        # Fetch all connections in the hotel (including inter-floor)
        all_connections = self.controller.hotel_service.get_all_connections()

        # Draw nodes
        for el_id, (x, y, z) in pos.items():
            ax.scatter(x, y, z, s=100, c="blue")
            ax.text(x, y, z, str(el_id), color="black")

        # Draw edges (including inter-floor)
        for u, v in all_connections:
            if u in pos and v in pos:
                x = [pos[u][0], pos[v][0]]
                y = [pos[u][1], pos[v][1]]
                z = [pos[u][2], pos[v][2]]
                ax.plot(x, y, z, c="gray")

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Floor (Z)")
        ax.set_title("Hotel 3D Graph")
        self.canvas.draw()

    def handle_back(self):
        if self.on_back:
            self.on_back()

    def undo_action(self):
        pass

    def redo_action(self):
        pass