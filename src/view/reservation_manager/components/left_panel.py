from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QTextCharFormat, QColor, QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QCalendarWidget, QSpinBox, QListWidget,
    QListWidgetItem, QLineEdit, QPushButton, QSizePolicy, QHBoxLayout, QLabel, QFrame
)


class ReservationLeftPanel(QWidget):
    """Left panel for reservation management."""
    def __init__(self, controller, makeReservationClick, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.makeReservationClick = makeReservationClick

        self.checkInDate = None
        self.checkOutDate = None

        self.setupUi()

    def setupUi(self):
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(60, 60, 60))
        self.setPalette(palette)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # Sections
        topSection = QHBoxLayout()
        topLeftSection = QVBoxLayout()
        topRightSection = QVBoxLayout()
        bottomSection = QHBoxLayout()

        # Date Selector
        dateTitle = QLabel("Date Selector")
        dateTitle.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        dateTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dateTitle.setStyleSheet("color: white;")
        dateSeparator = QFrame()
        dateSeparator.setFrameShape(QFrame.Shape.HLine)
        dateSeparator.setFrameShadow(QFrame.Shadow.Sunken)
        dateSeparator.setStyleSheet("background-color: #777;")

        self.calendar = QCalendarWidget()
        self.calendar.setSelectedDate(QDate.currentDate())
        self.calendar.clicked.connect(self.dateClick)
        self.calendar.selectionChanged.connect(self.populateAvailableRoomsList)
        self.calendar.setStyleSheet(
            "QCalendarWidget {background-color: #444; color: white; border: 1px solid #666; border-radius: 4px;}"
            "QCalendarWidget QAbstractItemView {background-color: #444; color: white; selection-background-color: #4a6ea9;}"
            "QCalendarWidget QWidget#qt_calendar_navigationbar {background-color: #555; color: white;}"
        )

        # Guests
        guestsTitle = QLabel("Number of Guests & Guest Name")
        guestsTitle.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        guestsTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        guestsTitle.setStyleSheet("color: white;")
        guestsSeparator = QFrame()
        guestsSeparator.setFrameShape(QFrame.Shape.HLine)
        guestsSeparator.setFrameShadow(QFrame.Shadow.Sunken)
        guestsSeparator.setStyleSheet("background-color: #777;")

        self.guestSpin = QSpinBox()
        self.guestSpin.setMinimum(1)
        self.guestSpin.setMaximum(8)
        self.guestSpin.setStyleSheet(
            "QSpinBox {background-color: #444; color: white; border: 1px solid #666; padding: 5px;}"
        )
        self.guestSpin.valueChanged.connect(self.populateAvailableRoomsList)

        # Name Input
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText("Enter guest name")
        self.nameInput.setMinimumHeight(36)
        self.nameInput.setStyleSheet(
            "QLineEdit {background-color: #444; color: white; border: 1px solid #666; padding: 5px;}"
        )

        # Available Rooms
        roomsTitle = QLabel("Available Rooms")
        roomsTitle.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        roomsTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        roomsTitle.setStyleSheet("color: white;")
        roomsSeparator = QFrame()
        roomsSeparator.setFrameShape(QFrame.Shape.HLine)
        roomsSeparator.setFrameShadow(QFrame.Shadow.Sunken)
        roomsSeparator.setStyleSheet("background-color: #777;")

        self.availableRooms = QListWidget()
        self.availableRooms.setStyleSheet(
            "QListWidget {background-color: #444; color: white; border: 1px solid #666; padding: 5px;}"
        )

        topLeftSection.addWidget(dateTitle)
        topLeftSection.addWidget(dateSeparator)
        topLeftSection.addWidget(self.calendar)
        topLeftSection.addWidget(guestsTitle)
        topLeftSection.addWidget(guestsSeparator)
        topLeftSection.addWidget(self.guestSpin)
        topLeftSection.addWidget(self.nameInput)

        topRightSection.addWidget(roomsTitle)
        topRightSection.addWidget(roomsSeparator)
        topRightSection.addWidget(self.availableRooms)

        topSection.addLayout(topLeftSection, 1)
        topSection.addLayout(topRightSection, 1)

        # Reserve Button
        self.reserveBtn = QPushButton("Make a reservation")
        self.reserveBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.reserveBtn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        self.reserveBtn.clicked.connect(self.makeReservationClick)

        self.layout.addLayout(topSection, 7)
        self.layout.addLayout(bottomSection, 3)
        self.layout.addWidget(self.reserveBtn)

    def populateAvailableRoomsList(self):
        self.availableRooms.clear()
        if not self.checkInDate or not self.checkOutDate:
            return

        rooms = self.controller.get_available_rooms(
            self.checkInDate.toString("yyyy-MM-dd"),
            self.checkOutDate.toString("yyyy-MM-dd"),
            self.guestSpin.value()
        )
        for room in rooms:
            item = QListWidgetItem(f"Room {room.number} | {room.capacity} Beds | {room.price_per_night}$")
            item.setData(Qt.ItemDataRole.UserRole, room)
            self.availableRooms.addItem(item)

    def dateClick(self, date):
        if not self.checkInDate or (self.checkInDate and self.checkOutDate):
            self.checkInDate = date
            self.checkOutDate = None
        elif date > self.checkInDate:
            self.checkOutDate = date
        else:
            self.checkInDate = date
            self.checkOutDate = None

        self._highlightDateRange()
        self.populateAvailableRoomsList()

    def _highlightDateRange(self):
        defaultFormat = QTextCharFormat()
        self.calendar.setDateTextFormat(QDate(), defaultFormat)

        if self.checkInDate:
            fmtIn = QTextCharFormat()
            fmtIn.setBackground(QColor("green"))
            self.calendar.setDateTextFormat(self.checkInDate, fmtIn)

        if self.checkInDate and self.checkOutDate:
            fmtOut = QTextCharFormat()
            fmtOut.setBackground(QColor("red"))
            self.calendar.setDateTextFormat(self.checkOutDate, fmtOut)

            fmtBetween = QTextCharFormat()
            fmtBetween.setBackground(QColor("lightgray"))

            d = QDate(self.checkInDate)
            while d < self.checkOutDate:
                d = d.addDays(1)
                if d < self.checkOutDate:
                    self.calendar.setDateTextFormat(d, fmtBetween)
