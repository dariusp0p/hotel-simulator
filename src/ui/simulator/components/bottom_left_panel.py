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

        floors = self.controller.get_all_floors()
        pos = {}
        elements = {}

        for floor in floors:
            z = floor.level
            floor_grid = self.controller.get_floor_grid(floor.db_id)

            for position, element in floor_grid.items():
                if element and position:
                    x, y = position
                    pos[element.db_id] = (x, y, z)
                    elements[element.db_id] = element

        all_connections = self.controller.get_all_connections()

        for el_id, (x, y, z) in pos.items():
            element = elements.get(el_id)

            if not element:
                continue

            if element.type == "room":
                ax.scatter(x, y, z, s=120, c="blue")
                room_number = getattr(element, 'number', '?')
                ax.text(x, y, z, f"{room_number}", color="black")  # Higher zorder ensures text is on top
            elif element.type == "hallway":
                ax.scatter(x, y, z, s=20, c="darkgray")
            elif element.type == "staircase":
                ax.scatter(x, y, z, s=40, c="yellow")

        for u, v in all_connections:
            if u in pos and v in pos:
                x = [pos[u][0], pos[v][0]]
                y = [pos[u][1], pos[v][1]]
                z = [pos[u][2], pos[v][2]]
                ax.plot(x, y, z, c="gray")

        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])

        ax.grid(False)

        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_zlabel("Level")

        self.canvas.draw()