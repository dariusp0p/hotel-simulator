from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout


class HotelConfiguratorPage(QWidget):
    def __init__(self, on_back=None, hotel_service=None, controller=None):
        super().__init__()
        self.controller = controller
        self.on_back = on_back
        self.hotel_service = hotel_service

        self.setStyleSheet("background-color: #bfbfbf;")
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.back_btn = QPushButton("← Back")
        self.back_btn.clicked.connect(self.handle_back_click)
        layout.addWidget(self.back_btn)

    def handle_back_click(self):
        if self.on_back:
            self.on_back()
