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
from datetime import datetime



class ReservationManagerWindow(QWidget):
    def __init__(self, on_back=None, controller=None):
        super().__init__()
        self.on_back = on_back
        self.controller = controller

        self.reservation_list = None

        self.check_in_date = None
        self.check_out_date = None

        self.setup_ui()


    # Setup
    def setup_ui(self):
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
        # Date Selector
        date_group = QGroupBox("Date Selector")
        date_layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.calendar.setSelectedDate(QDate.currentDate())
        self.calendar.clicked.connect(self.handle_date_click)
        self.calendar.selectionChanged.connect(self.populate_available_rooms_list)

        date_layout.addWidget(self.calendar)
        date_group.setLayout(date_layout)

        # Number of guests
        self.guest_spin = QSpinBox()
        self.guest_spin.setMinimum(1)
        self.guest_spin.setMaximum(8)
        self.guest_spin.valueChanged.connect(self.populate_available_rooms_list)
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

        # Name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(
            "Enter the name of the person the reservation is being made for:"
        )
        self.name_input.setMinimumHeight(40)
        name_layout = QVBoxLayout()
        name_layout.addWidget(self.name_input)

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
        self.left_layout.addLayout(name_layout)
        self.left_layout.addStretch()
        self.left_layout.addWidget(self.reserve_btn)


    def setup_right_side(self):
        self.reservations_box = QGroupBox("All Reservations")
        main_res_layout = QVBoxLayout()

        # Direct Search Bar
        direct_search_layout = QHBoxLayout()

        self.direct_search_bar = QLineEdit()
        self.direct_search_bar.setPlaceholderText("Direct search...")
        self.direct_search_bar.textChanged.connect(self.handle_direct_search_bar_change)
        # self.direct_search_bar.setStyleSheet(
        #     """
        #     QLineEdit {
        #         padding: 6px;
        #         font-size: 11pt;
        #         border: 1px solid #555;
        #         border-radius: 8px;
        #     }
        #     """
        # )

        self.direct_search_button = QPushButton("Search")
        self.direct_search_button.setEnabled(False)
        self.direct_search_button.clicked.connect(self.direct_search_reservations)
        # self.direct_search_button.setStyleSheet(
        #     "padding: 6px; font-weight: bold; background-color: #666; color: white"
        # )

        direct_search_layout.addWidget(self.direct_search_bar)
        direct_search_layout.addWidget(self.direct_search_button)
        main_res_layout.addLayout(direct_search_layout)

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.handle_filter_change)
        # self.search_bar.setStyleSheet(
        #     """
        #     QLineEdit {
        #         padding: 6px;
        #         font-size: 11pt;
        #         border: 1px solid #555;
        #         border-radius: 8px;
        #     }
        #     """
        # )

        main_res_layout.addWidget(self.search_bar)

        # Date Filter + Reset Filters Button
        date_filter_layout = QHBoxLayout()

        self.from_btn = QPushButton("From")
        self.to_btn = QPushButton("To")
        self.clear_filters_btn = QPushButton("X")
        self.clear_filters_btn.setFixedWidth(30)

        for btn in [self.from_btn, self.to_btn]:
            btn.setStyleSheet(
                "padding: 6px; font-weight: bold; background-color: #666; color: white"
            )
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.clear_filters_btn.setStyleSheet(
            "padding: 6px; font-weight: bold; background-color: #900; color: white"
        )

        self.from_btn.clicked.connect(lambda: self.open_date_picker("from"))
        self.to_btn.clicked.connect(lambda: self.open_date_picker("to"))
        self.clear_filters_btn.clicked.connect(self.reset_all_filters)

        date_filter_layout.addWidget(self.from_btn)
        date_filter_layout.addWidget(self.to_btn)
        date_filter_layout.addWidget(self.clear_filters_btn)
        main_res_layout.addLayout(date_filter_layout)

        # Reservation List
        self.reservation_list = QListWidget()
        self.reservation_list.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.reservation_list.itemSelectionChanged.connect(self.handle_selection_change)

        main_res_layout.addWidget(self.reservation_list)

        self.reservations_box.setLayout(main_res_layout)

        # Edit / Delete Buttons
        btns_layout = QHBoxLayout()

        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")
        for btn in [self.edit_btn, self.delete_btn]:
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.setStyleSheet(
                "padding: 8px; font-weight: bold; background-color: #333; color: white"
            )
            btn.setEnabled(False)
        self.edit_btn.clicked.connect(self.edit_reservation)
        self.delete_btn.clicked.connect(self.delete_reservation)

        btns_layout.addWidget(self.edit_btn)
        btns_layout.addWidget(self.delete_btn)

        self.right_layout.addWidget(self.reservations_box)
        self.right_layout.addLayout(btns_layout)

        self.populate_reservation_list(self.controller.get_all_reservations())

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
            self.available_rooms.addItem(f"Room {room.number} | {room.capacity} Beds")

    # Right
    def handle_direct_search_bar_change(self):
        if self.direct_search_bar.text().strip():
            self.direct_search_button.setEnabled(True)
        else:
            self.direct_search_button.setEnabled(False)

    def direct_search_reservations(self):
        self.reset_filters()
        search_text = self.direct_search_bar.text().strip()

        reservations = self.controller.reservation_direct_search(search_text)

        if not reservations:
            QMessageBox.information(self, "No Results", "No reservations found for the given search term.")
            return

        self.populate_reservation_list(reservations)

    def handle_filter_change(self):
        self.direct_search_bar.clear()

        search_bar_string = self.search_bar.text().strip()
        from_date = None
        to_date = None

        if self.from_btn.text() != "From":
            from_date = datetime.strptime(self.from_btn.text().split(" ")[1].strip(), "%Y-%m-%d").date()

        if self.to_btn.text() != "To":
            to_date = datetime.strptime(self.to_btn.text().split(" ")[1].strip(), "%Y-%m-%d").date()

        reservations = self.controller.reservation_search(search_bar_string, from_date, to_date)
        self.populate_reservation_list(reservations)

    def reset_filters(self):
        self.from_btn.setText("From")
        self.to_btn.setText("To")
        self.search_bar.setText("")
        self.populate_reservation_list(self.controller.get_all_reservations())

    def reset_all_filters(self):
        self.direct_search_bar.clear()
        self.reset_filters()


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
                self.from_btn.setText(f"From {selected_date.toString('yyyy-MM-dd')}")
            else:
                self.to_btn.setText(f"To {selected_date.toString('yyyy-MM-dd')}")

            dialog.accept()
            self.handle_filter_change()

        def reject():
            dialog.reject()

        buttons.accepted.connect(accept)
        buttons.rejected.connect(reject)

        dialog.setLayout(layout)
        dialog.exec()



    def handle_selection_change(self):
        has_selection = bool(self.reservation_list.selectedItems())
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)

    def populate_reservation_list(self, reservations):
        self.reservation_list.clear()

        for reservation in reservations:
            self.reservation_list.addItem(
                f"{reservation.reservation_id} | {reservation.room_number} | "
                f"{reservation.guest_name} | {reservation.check_in_date} | "
                f"{reservation.check_out_date} | {reservation.number_of_guests}"
            )


    # CRUD
    def make_reservation(self):
        if not self.check_in_date or not self.check_out_date:
            QMessageBox.warning(self, "Warning", "Please select check-in and check-out dates")
            return

        selected_items = self.available_rooms.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a room")
            return

        guest_name = self.name_input.text().strip()
        if not guest_name:
            QMessageBox.warning(self, "Warning", "Please enter guest name")
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
            self.reset_filters()
            self.populate_reservation_list(self.controller.get_all_reservations())
            QMessageBox.information(self, "Success", "Reservation created successfully!")
            self.name_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to make reservation: {str(e)}")


    def edit_reservation(self):
        selected_item = self.reservation_list.currentItem()

        reservation_id = selected_item.text().split(" | ")[0].strip()
        reservation = self.controller.get_reservation_by_id(reservation_id)

        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Reservation")

        layout = QVBoxLayout()

        room_input = QLineEdit(reservation.room_number)
        guest_name_input = QLineEdit(reservation.guest_name)
        guest_count_input = QSpinBox()
        guest_count_input.setValue(reservation.number_of_guests)
        guest_count_input.setMinimum(1)
        guest_count_input.setMaximum(8)
        check_in_input = QLineEdit(reservation.check_in_date.strftime("%Y-%m-%d"))
        check_out_input = QLineEdit(reservation.check_out_date.strftime("%Y-%m-%d"))

        layout.addWidget(QLabel("Room Number:"))
        layout.addWidget(room_input)
        layout.addWidget(QLabel("Guest Name:"))
        layout.addWidget(guest_name_input)
        layout.addWidget(QLabel("Number of Guests:"))
        layout.addWidget(guest_count_input)
        layout.addWidget(QLabel("Check-in Date (YYYY-MM-DD):"))
        layout.addWidget(check_in_input)
        layout.addWidget(QLabel("Check-out Date (YYYY-MM-DD):"))
        layout.addWidget(check_out_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        layout.addWidget(buttons)

        def confirm():
            if not all([
                room_input.text().strip(),
                guest_name_input.text().strip(),
                check_in_input.text().strip(),
                check_out_input.text().strip()
            ]):
                QMessageBox.warning(self, "Warning", "All fields must be filled out.")
                return

            try:
                self.controller.update_reservation(
                    reservation_id,
                    room_input.text().strip(),
                    guest_name_input.text().strip(),
                    guest_count_input.value(),
                    check_in_input.text().strip(),
                    check_out_input.text().strip()
                )
                self.reset_all_filters()
                self.populate_reservation_list(self.controller.get_all_reservations())
                QMessageBox.information(self, "Success", "Reservation updated successfully!")
                dialog.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update reservation: {str(e)}")

        def cancel():
            dialog.reject()

        buttons.accepted.connect(confirm)
        buttons.rejected.connect(cancel)

        dialog.setLayout(layout)
        dialog.exec()


    def delete_reservation(self):
        selected_item = self.reservation_list.currentItem()

        reservation_id = selected_item.text().split(" | ")[0].strip()

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete reservation {reservation_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.controller.delete_reservation(reservation_id)
                self.reset_all_filters()
                self.populate_reservation_list(self.controller.get_all_reservations())
                QMessageBox.information(self, "Success", "Reservation deleted successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete reservation: {str(e)}")