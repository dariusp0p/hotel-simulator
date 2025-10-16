from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class HotBar(QWidget):
    """A horizontal toolbar with buttons to add rooms, hallways, and staircases."""
    def __init__(self, addElementCallback, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(60, 60, 60))
        self.setPalette(palette)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        layout.addStretch()

        addRoomBtn = QPushButton("Add Room")
        addRoomBtn.setFixedHeight(40)
        addRoomBtn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        addRoomBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        addRoomBtn.clicked.connect(lambda: addElementCallback("room"))

        addHallwayBtn = QPushButton("Add Hallway")
        addHallwayBtn.setFixedHeight(40)
        addHallwayBtn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        addHallwayBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        addHallwayBtn.clicked.connect(lambda: addElementCallback("hallway"))

        addStaircaseBtn = QPushButton("Add Staircase")
        addStaircaseBtn.setFixedHeight(40)
        addStaircaseBtn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        addStaircaseBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        addStaircaseBtn.clicked.connect(lambda: addElementCallback("staircase"))

        layout.addWidget(addRoomBtn)
        layout.addWidget(addHallwayBtn)
        layout.addWidget(addStaircaseBtn)

        layout.addStretch()
