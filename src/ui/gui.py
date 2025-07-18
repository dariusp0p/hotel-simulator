from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)
from src.service.reservation_service import ReservationService
from src.utilities.exceptions import ValidationError


class MainWindow(QMainWindow):
    def __init__(self, reservation_service: ReservationService):
        super().__init__()
        self.service = reservation_service
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Hotel Reservation System")
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.guest_name_input = QLineEdit()
        self.room_number_input = QLineEdit()
        self.number_of_guests_input = QLineEdit()
        self.check_in_input = QLineEdit()
        self.check_out_input = QLineEdit()

        self.check_in_input.setPlaceholderText("YYYY-MM-DD")
        self.check_out_input.setPlaceholderText("YYYY-MM-DD")

        form_layout.addRow("Guest Name:", self.guest_name_input)
        form_layout.addRow("Room Number:", self.room_number_input)
        form_layout.addRow("Number of Guests:", self.number_of_guests_input)
        form_layout.addRow("Check-in Date:", self.check_in_input)
        form_layout.addRow("Check-out Date:", self.check_out_input)

        self.add_button = QPushButton("Make Reservation")
        self.add_button.clicked.connect(self.handle_add_reservation)

        self.show_button = QPushButton("Show All Reservations")
        self.show_button.clicked.connect(self.show_all_reservations)

        self.reservations_display = QTextEdit()
        self.reservations_display.setReadOnly(True)

        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.add_button)
        main_layout.addWidget(self.show_button)
        main_layout.addWidget(self.reservations_display)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def handle_add_reservation(self):
        data = {
            'guest_name': self.guest_name_input.text(),
            'room_number': self.room_number_input.text(),
            'number_of_guests': int(self.number_of_guests_input.text()),
            'check_in_date': self.check_in_input.text(),
            'check_out_date': self.check_out_input.text(),
        }
        try:
            self.service.make_reservation(data)
            QMessageBox.information(self, "Success", "Reservation created successfully.")
            self.show_all_reservations()
        except ValidationError as ve:
            QMessageBox.warning(self, "Validation Error", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def show_all_reservations(self):
        self.reservations_display.clear()
        reservations = self.service.get_all_reservations()
        for r in reservations:
            self.reservations_display.append(
                f"{r.reservation_id}: {r.guest_name}, Room {r.room_number}, "
                f"{r.check_in_date} to {r.check_out_date}, Guests: {r.number_of_guests}"
            )