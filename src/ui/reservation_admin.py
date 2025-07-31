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
    QMessageBox,
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QTextCharFormat, QColor


class ReservationAdminPage(QWidget):
    def __init__(self, on_back=None, controller=None):
        super().__init__()
        self.on_back = on_back
        self.controller = controller

        self.check_in_date = None
        self.check_out_date = None

        self.setStyleSheet("background-color: #bfbfbf;")

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.top_bar = QHBoxLayout()
        self.back_btn = QPushButton("← Back")
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
        date_group = QGroupBox("Date Selector")
        date_layout = QVBoxLayout()
        self.calendar = QCalendarWidget()
        self.calendar.setSelectedDate(QDate.currentDate())
        self.calendar.clicked.connect(self.handle_date_click)
        self.calendar.selectionChanged.connect(self.update_available_rooms)
        date_layout.addWidget(self.calendar)
        date_group.setLayout(date_layout)

        self.guest_spin = QSpinBox()
        self.guest_spin.setMinimum(1)
        self.guest_spin.setMaximum(20)
        self.guest_spin.valueChanged.connect(self.update_available_rooms)
        guest_box = QGroupBox("Number of guests")
        guest_layout = QVBoxLayout()
        guest_layout.addWidget(self.guest_spin)
        guest_box.setLayout(guest_layout)

        calendar_guest_layout = QVBoxLayout()
        calendar_guest_layout.addWidget(date_group)
        calendar_guest_layout.addWidget(guest_box)

        self.rooms_box = QGroupBox("Available Rooms")
        self.available_rooms = QListWidget()
        room_layout = QVBoxLayout()
        room_layout.addWidget(self.available_rooms)
        self.rooms_box.setLayout(room_layout)

        calendar_and_rooms_layout = QHBoxLayout()
        calendar_and_rooms_layout.addLayout(calendar_guest_layout, 2)
        calendar_and_rooms_layout.addWidget(self.rooms_box, 2)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(
            "Enter the name of the person the reservation is being made for:"
        )
        self.name_input.setMinimumHeight(40)
        name_layout = QVBoxLayout()
        name_layout.addWidget(self.name_input)

        self.reserve_btn = QPushButton("Make a reservation")
        self.reserve_btn.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.reserve_btn.setStyleSheet(
            "padding: 10px; font-weight: bold; background-color: #333; color: white"
        )
        self.reserve_btn.clicked.connect(self.make_reservation)

        self.left_layout.addLayout(calendar_and_rooms_layout)
        self.left_layout.addLayout(name_layout)
        self.left_layout.addStretch()
        self.left_layout.addWidget(self.reserve_btn)

    def setup_right_side(self):
        self.reservations_box = QGroupBox("All Reservations")
        main_res_layout = QVBoxLayout()

        date_filter_layout = QHBoxLayout()
        self.from_btn = QPushButton("From")
        self.to_btn = QPushButton("To")

        for btn in [self.from_btn, self.to_btn]:
            btn.setStyleSheet(
                "padding: 6px; font-weight: bold; background-color: #666; color: white"
            )
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.from_btn.clicked.connect(lambda: self.open_date_picker("from"))
        self.to_btn.clicked.connect(lambda: self.open_date_picker("to"))

        date_filter_layout.addWidget(self.from_btn)
        date_filter_layout.addWidget(self.to_btn)
        main_res_layout.addLayout(date_filter_layout)

        self.reservations_list = QListWidget()
        self.reservations_list.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        main_res_layout.addWidget(self.reservations_list)
        self.reservations_box.setLayout(main_res_layout)

        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")

        for btn in [self.edit_btn, self.delete_btn]:
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.setStyleSheet(
                "padding: 8px; font-weight: bold; background-color: #333; color: white"
            )

        btns_layout = QHBoxLayout()
        btns_layout.addWidget(self.edit_btn)
        btns_layout.addWidget(self.delete_btn)

        self.right_layout.addWidget(self.reservations_box)
        self.right_layout.addLayout(btns_layout)

    def open_date_picker(self, which):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Select {which.capitalize()} Date")
        layout = QVBoxLayout()

        calendar = QCalendarWidget()
        calendar.setGridVisible(True)
        calendar.setSelectedDate(QDate.currentDate())
        layout.addWidget(calendar)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        layout.addWidget(buttons)

        def accept():
            selected_date = calendar.selectedDate()
            if which == "from":
                self.from_btn.setText(f"From: {selected_date.toString('yyyy-MM-dd')}")
            else:
                self.to_btn.setText(f"To: {selected_date.toString('yyyy-MM-dd')}")
            dialog.accept()

        def reject():
            dialog.reject()

        buttons.accepted.connect(accept)
        buttons.rejected.connect(reject)

        dialog.setLayout(layout)
        dialog.exec()

    def handle_back_click(self):
        if self.on_back:
            self.on_back()

    def handle_date_click(self, date):
        if not self.check_in_date or (self.check_in_date and self.check_out_date):
            self.check_in_date = date
            self.check_out_date = None
        elif date > self.check_in_date:
            self.check_out_date = date
        else:
            self.check_in_date = date
            self.check_out_date = None
        print(self.check_in_date, self.check_out_date)
        self.highlight_date_range()

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

    def update_available_rooms(self):
        if not self.controller or not self.check_in_date or not self.check_out_date:
            return

        self.available_rooms.clear()

        # Fetch available rooms from the controller
        available_rooms = self.controller.get_available_rooms(
            self.check_in_date.toString("yyyy-MM-dd"),
            self.check_out_date.toString("yyyy-MM-dd"),
            self.guest_spin.value(),
        )

        # Populate the available rooms list
        for room in available_rooms:
            self.available_rooms.addItem(f"Room {room[1]} - Capacity: {room[4]}")

    def make_reservation(self):
        if not self.controller:
            print("Problem")
            return
        print("YEAH")
        if not self.check_in_date or not self.check_out_date:
            QMessageBox.warning(
                self, "Warning", "Please select check-in and check-out dates"
            )
            return

        selected_items = self.available_rooms.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a room")
            return

        guest_name = self.name_input.text().strip()
        if not guest_name:
            QMessageBox.warning(self, "Warning", "Please enter guest name")
            return

        selected_room = selected_items[0].text().split()[1]  # Extract room number
        print("YEY")
        try:
            self.controller.make_reservation(
                room_number=selected_room,
                guest_name=guest_name,
                guest_number=self.guest_spin.value(),
                arrival_date=self.check_in_date.toString("yyyy-MM-dd"),
                departure_date=self.check_out_date.toString("yyyy-MM-dd"),
            )
            QMessageBox.information(
                self, "Success", "Reservation created successfully!"
            )
            self.name_input.clear()
            self.update_available_rooms()
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to create reservation: {str(e)}"
            )
