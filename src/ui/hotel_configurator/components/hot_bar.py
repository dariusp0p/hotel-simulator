from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor



class HotBar(QWidget):
    def __init__(self, add_room_callback, add_hallway_callback, add_staircase_callback, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(60, 60, 60))
        self.setPalette(palette)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        layout.addStretch()

        add_room_btn = QPushButton("Add Room")
        add_room_btn.setFixedHeight(40)
        add_room_btn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        add_room_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_room_btn.clicked.connect(add_room_callback)

        add_hallway_btn = QPushButton("Add Hallway")
        add_hallway_btn.setFixedHeight(40)
        add_hallway_btn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        add_hallway_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_hallway_btn.clicked.connect(add_hallway_callback)

        add_staircase_btn = QPushButton("Add Staircase")
        add_staircase_btn.setFixedHeight(40)
        add_staircase_btn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        add_staircase_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_staircase_btn.clicked.connect(add_staircase_callback)

        layout.addWidget(add_room_btn)
        layout.addWidget(add_hallway_btn)
        layout.addWidget(add_staircase_btn)

        layout.addStretch()
