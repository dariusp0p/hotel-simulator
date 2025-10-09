from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QTextCharFormat, QColor, QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QCalendarWidget, QSpinBox, QListWidget,
    QListWidgetItem, QLineEdit, QPushButton, QSizePolicy, QHBoxLayout, QLabel, QFrame
)



class ReservationLeftPanel(QWidget):
    def __init__(self, controller, make_reservation_click, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.make_reservation_click = make_reservation_click

        self.check_in_date = None
        self.check_out_date = None

        self.setup_ui()


    def setup_ui(self):
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(60, 60, 60))
        self.setPalette(palette)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # Sections
        top_section = QHBoxLayout()
        top_left_section = QVBoxLayout()
        top_right_section = QVBoxLayout()
        bottom_section = QHBoxLayout()

        # Date Selector
        date_title = QLabel("Date Selector")
        date_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        date_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        date_title.setStyleSheet("color: white;")
        date_separator = QFrame()
        date_separator.setFrameShape(QFrame.Shape.HLine)
        date_separator.setFrameShadow(QFrame.Shadow.Sunken)
        date_separator.setStyleSheet("background-color: #777;")

        self.calendar = QCalendarWidget()
        self.calendar.setSelectedDate(QDate.currentDate())
        self.calendar.clicked.connect(self.date_click)
        self.calendar.selectionChanged.connect(self.populate_available_rooms_list)
        self.calendar.setStyleSheet(
            "QCalendarWidget {background-color: #444; color: white; border: 1px solid #666; border-radius: 4px;}"
            "QCalendarWidget QAbstractItemView {background-color: #444; color: white; selection-background-color: #4a6ea9;}"
            "QCalendarWidget QWidget#qt_calendar_navigationbar {background-color: #555; color: white;}"
        )

        # Guests
        guests_title = QLabel("Number of Guests & Guest Name")
        guests_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        guests_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        guests_title.setStyleSheet("color: white;")
        guests_separator = QFrame()
        guests_separator.setFrameShape(QFrame.Shape.HLine)
        guests_separator.setFrameShadow(QFrame.Shadow.Sunken)
        guests_separator.setStyleSheet("background-color: #777;")

        self.guest_spin = QSpinBox()
        self.guest_spin.setMinimum(1)
        self.guest_spin.setMaximum(8)
        self.guest_spin.setStyleSheet(
            "QSpinBox {background-color: #444; color: white; border: 1px solid #666; padding: 5px;}"
        )
        self.guest_spin.valueChanged.connect(self.populate_available_rooms_list)

        # Name Input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter guest name")
        self.name_input.setMinimumHeight(36)
        self.name_input.setStyleSheet(
            "QLineEdit {background-color: #444; color: white; border: 1px solid #666; padding: 5px;}"
        )

        # Available Rooms
        rooms_title = QLabel("Available Rooms")
        rooms_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        rooms_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rooms_title.setStyleSheet("color: white;")
        rooms_separator = QFrame()
        rooms_separator.setFrameShape(QFrame.Shape.HLine)
        rooms_separator.setFrameShadow(QFrame.Shadow.Sunken)
        rooms_separator.setStyleSheet("background-color: #777;")

        self.available_rooms = QListWidget()
        self.available_rooms.setStyleSheet(
            "QListWidget {background-color: #444; color: white; border: 1px solid #666; padding: 5px;}"
        )


        top_left_section.addWidget(date_title)
        top_left_section.addWidget(date_separator)
        top_left_section.addWidget(self.calendar)
        top_left_section.addWidget(guests_title)
        top_left_section.addWidget(guests_separator)
        top_left_section.addWidget(self.guest_spin)
        top_left_section.addWidget(self.name_input)

        top_right_section.addWidget(rooms_title)
        top_right_section.addWidget(rooms_separator)
        top_right_section.addWidget(self.available_rooms)

        top_section.addLayout(top_left_section, 1)
        top_section.addLayout(top_right_section, 1)



        # Reserve Button
        self.reserve_btn = QPushButton("Make a reservation")
        self.reserve_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.reserve_btn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        self.reserve_btn.clicked.connect(self.make_reservation_click)


        self.layout.addLayout(top_section, 7)
        self.layout.addLayout(bottom_section, 3)
        self.layout.addWidget(self.reserve_btn)


    def populate_available_rooms_list(self):
        self.available_rooms.clear()
        if not self.check_in_date or not self.check_out_date:
            return

        rooms = self.controller.get_available_rooms(
            self.check_in_date.toString("yyyy-MM-dd"),
            self.check_out_date.toString("yyyy-MM-dd"),
            self.guest_spin.value()
        )
        for room in rooms:
            item = QListWidgetItem(f"Room {room.number} | {room.capacity} Beds | {room.price_per_night}$")
            item.setData(Qt.ItemDataRole.UserRole, room)
            self.available_rooms.addItem(item)


    def date_click(self, date):
        if not self.check_in_date or (self.check_in_date and self.check_out_date):
            self.check_in_date = date
            self.check_out_date = None
        elif date > self.check_in_date:
            self.check_out_date = date
        else:
            self.check_in_date = date
            self.check_out_date = None

        self._highlight_date_range()
        self.populate_available_rooms_list()

    def _highlight_date_range(self):
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
