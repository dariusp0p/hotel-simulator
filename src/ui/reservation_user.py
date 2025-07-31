from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtCore import Qt


class ReservationUserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reservation Manager - User")
        self.resize(800, 600)

        label = QLabel("Reservation Manager - User", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)
