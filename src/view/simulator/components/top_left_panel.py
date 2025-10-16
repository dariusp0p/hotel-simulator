from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QGroupBox,
                             QGridLayout, QDateEdit, QSlider, QPushButton, QHBoxLayout)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QFont


class TopLeftPanel(QWidget):
    """Top-left panel with hotel stats and reservation generator."""
    def __init__(self, parent=None, controller=None, generateReservationsCallback=None):
        super().__init__(parent)
        self.generateReservationsCallback = generateReservationsCallback
        self.controller = controller
        self.setupUi()

    def setupUi(self):
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(60, 60, 60))
        self.setPalette(palette)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)  # Reduced spacing overall

        # Hotel Stats Section
        statsTitle = QLabel("Hotel Statistics")
        statsTitle.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        statsTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        statsTitle.setStyleSheet("color: white;")

        statsSeparator = QFrame()
        statsSeparator.setFrameShape(QFrame.Shape.HLine)
        statsSeparator.setFrameShadow(QFrame.Shadow.Sunken)
        statsSeparator.setStyleSheet("background-color: #777;")

        layout.addWidget(statsTitle)
        layout.addWidget(statsSeparator)

        # Stats content
        statsContent = QWidget()
        gridLayout = QGridLayout(statsContent)
        gridLayout.setContentsMargins(0, 0, 0, 0)  # Remove internal margins
        gridLayout.setSpacing(8)

        # Create labels with placeholders
        labelStyle = "color: white;"
        valueStyle = "color: #aaa; font-weight: bold;"

        # Row 1: Floors
        floorsLabel = QLabel("Floors:")
        floorsLabel.setStyleSheet(labelStyle)
        self.floorsValue = QLabel("0")
        self.floorsValue.setStyleSheet(valueStyle)

        # Row 2: Rooms
        roomsLabel = QLabel("Total Rooms:")
        roomsLabel.setStyleSheet(labelStyle)
        self.roomsValue = QLabel("0")
        self.roomsValue.setStyleSheet(valueStyle)

        # Row 3: Reservations
        reservationsLabel = QLabel("Total Reservations:")
        reservationsLabel.setStyleSheet(labelStyle)
        self.reservationsValue = QLabel("0")
        self.reservationsValue.setStyleSheet(valueStyle)

        # Row 4: Income
        incomeLabel = QLabel("Generated Income:")
        incomeLabel.setStyleSheet(labelStyle)
        self.incomeValue = QLabel("$0")
        self.incomeValue.setStyleSheet(valueStyle)

        # Add to grid
        gridLayout.addWidget(floorsLabel, 0, 0)
        gridLayout.addWidget(self.floorsValue, 0, 1)
        gridLayout.addWidget(roomsLabel, 1, 0)
        gridLayout.addWidget(self.roomsValue, 1, 1)
        gridLayout.addWidget(reservationsLabel, 2, 0)
        gridLayout.addWidget(self.reservationsValue, 2, 1)
        gridLayout.addWidget(incomeLabel, 3, 0)
        gridLayout.addWidget(self.incomeValue, 3, 1)

        layout.addWidget(statsContent)

        # Add spacing between sections
        layout.addSpacing(15)

        # Reservation Generator Section
        genTitle = QLabel("Reservation Generator")
        genTitle.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        genTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        genTitle.setStyleSheet("color: white;")

        genSeparator = QFrame()
        genSeparator.setFrameShape(QFrame.Shape.HLine)
        genSeparator.setFrameShadow(QFrame.Shadow.Sunken)
        genSeparator.setStyleSheet("background-color: #777;")

        layout.addWidget(genTitle)
        layout.addWidget(genSeparator)

        # Generator content
        genContent = QWidget()
        genLayout = QVBoxLayout(genContent)
        genLayout.setContentsMargins(0, 0, 0, 0)  # Remove internal margins
        genLayout.setSpacing(10)

        # Date range selectors
        dateLabelStyle = "color: white;"
        dateEditStyle = "background-color: #555; color: white;"

        # From date
        fromLayout = QHBoxLayout()
        fromLabel = QLabel("From:")
        fromLabel.setStyleSheet(dateLabelStyle)
        fromDate = QDateEdit()
        fromDate.setDate(QDate.currentDate())
        fromDate.setCalendarPopup(True)
        fromDate.setStyleSheet(dateEditStyle)
        fromLayout.addWidget(fromLabel)
        fromLayout.addWidget(fromDate, 1)

        # To date
        toLayout = QHBoxLayout()
        toLabel = QLabel("To:")
        toLabel.setStyleSheet(dateLabelStyle)
        toDate = QDateEdit()
        toDate.setDate(QDate.currentDate().addDays(7))
        toDate.setCalendarPopup(True)
        toDate.setStyleSheet(dateEditStyle)
        toLayout.addWidget(toLabel)
        toLayout.addWidget(toDate, 1)

        # Occupancy slider
        occupancyLayout = QHBoxLayout()
        occupancyLabel = QLabel("Occupancy:")
        occupancyLabel.setStyleSheet(dateLabelStyle)
        occupancyValue = QLabel("50%")
        occupancyValue.setStyleSheet(dateLabelStyle)
        occupancyLayout.addWidget(occupancyLabel)
        occupancyLayout.addWidget(occupancyValue)

        occupancySlider = QSlider(Qt.Orientation.Horizontal)
        occupancySlider.setMinimum(0)
        occupancySlider.setMaximum(100)
        occupancySlider.setValue(50)
        occupancySlider.setStyleSheet("QSlider::handle:horizontal {background-color: #4a6ea9;}")
        occupancySlider.valueChanged.connect(lambda value: occupancyValue.setText(f"{value}%"))

        # Generate button
        generateBtn = QPushButton("Generate Reservations")
        generateBtn.setStyleSheet(
            "QPushButton {background-color: #2e8b57; color: white; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #3ba968;}"
        )
        self.fromDate = fromDate
        self.toDate = toDate
        self.occupancySlider = occupancySlider
        generateBtn.clicked.connect(lambda: self._handleGenerateBtnClick())

        genLayout.addLayout(fromLayout)
        genLayout.addLayout(toLayout)
        genLayout.addLayout(occupancyLayout)
        genLayout.addWidget(occupancySlider)
        genLayout.addWidget(generateBtn)

        layout.addWidget(genContent)
        layout.addStretch()

    def _handleGenerateBtnClick(self):
        if self.generateReservationsCallback:
            fromDate = self.fromDate.date()
            toDate = self.toDate.date()
            occupancy = self.occupancySlider.value()

            self.generateReservationsCallback(fromDate, toDate, occupancy)

    def updateStats(self):
        if not self.controller:
            return

        # Update floors count
        floors = self.controller.get_all_floors()
        self.floorsValue.setText(str(len(floors)))

        # Get room count
        totalRooms = self.controller.get_total_rooms_count()
        self.roomsValue.setText(str(totalRooms))

        # Get reservations count
        reservations = self.controller.get_all_reservations()
        self.reservationsValue.setText(str(len(reservations)))

        # Get total income
        totalIncome = self.controller.get_total_reservations_income()
        self.incomeValue.setText(f"${totalIncome:,.2f}")