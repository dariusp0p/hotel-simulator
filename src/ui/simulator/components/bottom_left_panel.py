from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class BottomLeftPanel(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(60, 60, 60))
        self.setPalette(palette)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Title
        title = QLabel("3D Hotel Structure")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white;")

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #777;")

        # 3D Graph
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(title)
        layout.addWidget(separator)
        layout.addWidget(self.canvas)

        self.refresh()

    def refresh(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='3d')

        # Collect all elements and their positions
        floors = self.controller.get_all_floors()
        pos = {}
        for floor in floors:
            z = floor.level
            elements = self.controller.get_floor_elements(floor.db_id)
            for el in elements:
                x, y = el.position
                pos[el.db_id] = (x, y, z)

        # Fetch all connections in the hotel
        all_connections = self.controller.get_all_connections()

        # Draw nodes
        for el_id, (x, y, z) in pos.items():
            ax.scatter(x, y, z, s=100, c="blue")
            ax.text(x, y, z, str(el_id), color="black")

        # Draw edges
        for u, v in all_connections:
            if u in pos and v in pos:
                x = [pos[u][0], pos[v][0]]
                y = [pos[u][1], pos[v][1]]
                z = [pos[u][2], pos[v][2]]
                ax.plot(x, y, z, c="gray")

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Floor (Z)")
        self.canvas.draw()