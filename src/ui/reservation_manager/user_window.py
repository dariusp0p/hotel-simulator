from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QSizePolicy,
    QCalendarWidget,
    QSpinBox,
    QGroupBox,
    QDialog,
    QDialogButtonBox,
    QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QTextCharFormat, QColor

from src.utilities.user import User



class ReservationManagerUserWindow(QWidget):
    def __init__(self, on_back=None, controller=None):
        super().__init__()
        self.on_back = on_back
        self.controller = controller

        self.check_in_date = None
        self.check_out_date = None

        self.setup_ui()


    # Setup
    def setup_ui(self):
        self.setStyleSheet("background-color: #bfbfbf;")

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.top_bar = QHBoxLayout()
        self.back_btn = QPushButton("\u2190 Back")
        self.back_btn.setFixedHeight(40)
        self.back_btn.setStyleSheet(
            "padding: 6px; font-weight: bold; background-color: #444; color: white"
        )
        self.back_btn.clicked.connect(self.handle_back_click)
        self.top_bar.addWidget(self.back_btn)
        self.top_bar.addStretch()

        self.content_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.setup_left_side()
        self.setup_right_side()

        self.content_layout.addLayout(self.left_layout, 2)
        self.content_layout.addLayout(self.right_layout, 1)

        self.main_layout.addLayout(self.top_bar)
        self.main_layout.addLayout(self.content_layout)


    def setup_left_side(self):
        # Date selector
        date_group = QGroupBox("Date Selector")
        date_layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.calendar.setSelectedDate(QDate.currentDate())
        self.calendar.clicked.connect(self.handle_date_click)
        self.calendar.selectionChanged.connect(self.populate_available_rooms_list)  # Refresh on calendar change

        date_layout.addWidget(self.calendar)
        date_group.setLayout(date_layout)

        # Number of guests
        self.guest_spin = QSpinBox()
        self.guest_spin.setMinimum(1)
        self.guest_spin.setMaximum(20)
        self.guest_spin.valueChanged.connect(self.populate_available_rooms_list)  # Refresh on guest count change
        guest_box = QGroupBox("Number of guests")
        guest_layout = QVBoxLayout()
        guest_layout.addWidget(self.guest_spin)
        guest_box.setLayout(guest_layout)

        calendar_guest_layout = QVBoxLayout()
        calendar_guest_layout.addWidget(date_group)
        calendar_guest_layout.addWidget(guest_box)

        # Available Rooms List
        self.rooms_box = QGroupBox("Available Rooms")
        self.available_rooms = QListWidget()
        room_layout = QVBoxLayout()
        room_layout.addWidget(self.available_rooms)
        self.rooms_box.setLayout(room_layout)

        calendar_and_rooms_layout = QHBoxLayout()
        calendar_and_rooms_layout.addLayout(calendar_guest_layout, 2)
        calendar_and_rooms_layout.addWidget(self.rooms_box, 2)

        # Make a reservation
        self.reserve_btn = QPushButton("Make a reservation")
        self.reserve_btn.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.reserve_btn.setStyleSheet(
            "padding: 10px; font-weight: bold; background-color: #333; color: white"
        )
        self.reserve_btn.clicked.connect(self.make_reservation)

        self.left_layout.addLayout(calendar_and_rooms_layout)
        self.left_layout.addStretch()
        self.left_layout.addWidget(self.reserve_btn)


    def setup_right_side(self):
        self.reservations_box = QGroupBox("Your Reservations")
        main_res_layout = QVBoxLayout()

        # Reservation List
        self.reservation_list = QListWidget()
        self.reservation_list.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.reservation_list.itemSelectionChanged.connect(self.handle_selection_change)

        main_res_layout.addWidget(self.reservation_list)

        self.reservations_box.setLayout(main_res_layout)

        self.cancel_btn = QPushButton("Cancel Reservation")
        self.cancel_btn.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.cancel_btn.setStyleSheet(
            "padding: 8px; font-weight: bold; background-color: red; color: white"
        )
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self.cancel_reservation)

        self.right_layout.addWidget(self.reservations_box)
        self.right_layout.addWidget(self.cancel_btn)

        self.populate_reservation_list()


    # Handlers

    # Top
    def handle_back_click(self):
        if self.on_back:
            self.on_back()

    # Left
    def handle_date_click(self, date):
        if not self.check_in_date or (self.check_in_date and self.check_out_date):
            self.check_in_date = date
            self.check_out_date = None
        elif date > self.check_in_date:
            self.check_out_date = date
        else:
            self.check_in_date = date
            self.check_out_date = None

        self.highlight_date_range()
        self.populate_available_rooms_list()

    def highlight_date_range(self):
        default_format = QTextCharFormat()
        self.calendar.setDateTextFormat(QDate(), default_format)

        if self.check_in_date:
            fmt_in = QTextCharFormat()
            fmt_in.setBackground(QColor("green"))
            self.calendar.setDateTextFormat(self.check_in_date, fmt_in)

        if self.check_in_date and self.check_out_date:
            fmt_out = QTextCharFormat()
            fmt_out.setBackground(QColor("red"))
            self.calendar.setDateTextFormat(self.check_out_date, fmt_out)

            fmt_between = QTextCharFormat()
            fmt_between.setBackground(QColor("lightgray"))

            d = QDate(self.check_in_date)
            while d < self.check_out_date:
                d = d.addDays(1)
                if d < self.check_out_date:
                    self.calendar.setDateTextFormat(d, fmt_between)

    def populate_available_rooms_list(self):
        self.available_rooms.clear()

        if not self.check_in_date or not self.check_out_date:
            return

        available_rooms = self.controller.get_available_rooms(
            self.check_in_date.toString("yyyy-MM-dd"),
            self.check_out_date.toString("yyyy-MM-dd"),
            self.guest_spin.value()
        )

        for room in available_rooms:
            self.available_rooms.addItem(f"Room {room[1]} | {room[4]} Beds")

    # Right
    def handle_selection_change(self):
        has_selection = bool(self.reservation_list.selectedItems())
        self.cancel_btn.setEnabled(has_selection)

    def populate_reservation_list(self):
        self.reservation_list.clear()

        username = User.username

        reservations = self.controller.get_reservations_by_guest_name(username) or []
        for reservation in reservations:
            self.reservation_list.addItem(
                f"{reservation.reservation_id} | {reservation.room_number} | "
                f"{reservation.guest_name} | {reservation.check_in_date} | "
                f"{reservation.check_out_date} | {reservation.number_of_guests} | "
            )


    # CRUD
    def make_reservation(self):
        if not self.check_in_date or not self.check_out_date:
            QMessageBox.warning(self, "Warning", "Please select check-in and check-out dates.")
            return

        selected_items = self.available_rooms.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a room.")
            return

        guest_name = User.username
        if not guest_name:
            QMessageBox.warning(self, "Warning", "Guest name is not available.")
            return

        selected_room = selected_items[0].text().split()[1]

        try:
            self.controller.make_reservation(
                room_number=selected_room,
                guest_name=guest_name,
                guest_number=self.guest_spin.value(),
                arrival_date=self.check_in_date.toString("yyyy-MM-dd"),
                departure_date=self.check_out_date.toString("yyyy-MM-dd")
            )
            self.populate_reservation_list()
            QMessageBox.information(self, "Success", "Reservation created successfully!")
            self.populate_available_rooms_list()
            self.populate_reservation_list()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create reservation: {str(e)}")

    def cancel_reservation(self):
        selected_item = self.reservation_list.currentItem()

        reservation_id = selected_item.text().split(" | ")[0].strip()

        reply = QMessageBox.question(
            self,
            "Confirm Cancellation",
            f"Are you sure you want to cancel reservation {reservation_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.controller.delete_reservation(reservation_id)
                self.populate_reservation_list()
                QMessageBox.information(self, "Success", "Reservation canceled successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to cancel reservation: {str(e)}")