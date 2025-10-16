from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QLabel,
                             QComboBox, QCalendarWidget, QVBoxLayout, QDialog)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QColor, QFont


class HotBar(QWidget):
    """Hot bar with date display, simulation controls, and speed control."""
    dateChanged = pyqtSignal(QDate)
    speedChanged = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.currentDate = QDate.currentDate()
        self.setupUi()

    def setupUi(self):
        self.setFixedHeight(50)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(60, 60, 60))
        self.setPalette(palette)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        # Current date button (left) - styled like a label but clickable
        self.dateBtn = QPushButton(f"Current Date: {self.currentDate.toString('yyyy-MM-dd')}")
        self.dateBtn.setStyleSheet("QPushButton {color: white; font-weight: bold; "
                                   "border: 1px solid #777; padding: 5px 10px; "
                                   "background-color: #555;} "
                                   "QPushButton:hover {background-color: #666;}")
        self.dateBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.dateBtn.clicked.connect(self.showDatePicker)
        layout.addWidget(self.dateBtn)

        # Add spacer
        layout.addStretch()

        # Simulation control buttons - base style
        btnStyle = (
            "QPushButton {color: white; border: none; "
            "font-weight: bold; padding: 8px; min-width: 80px;} "
        )

        # 1 Day Back button
        self.dayBackBtn = QPushButton("◀ 1 Day")
        self.dayBackBtn.setStyleSheet(btnStyle + "QPushButton {background-color: #4a6ea9;} "
                                               "QPushButton:hover {background-color: #5a7eb9;}")
        self.dayBackBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.dayBackBtn)

        # Stop button (red with square symbol) - switched order
        self.stopBtn = QPushButton("■ Stop")
        self.stopBtn.setStyleSheet(btnStyle + "QPushButton {background-color: #b22222;} "
                                             "QPushButton:hover {background-color: #d32f2f;}")
        self.stopBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.stopBtn)

        # Start button (green)
        self.startBtn = QPushButton("▶ Start")
        self.startBtn.setStyleSheet(btnStyle + "QPushButton {background-color: #2e8b57;} "
                                              "QPushButton:hover {background-color: #3ba968;}")
        self.startBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.startBtn)

        # 1 Day Forward button
        self.dayForwardBtn = QPushButton("1 Day ▶")
        self.dayForwardBtn.setStyleSheet(btnStyle + "QPushButton {background-color: #4a6ea9;} "
                                                   "QPushButton:hover {background-color: #5a7eb9;}")
        self.dayForwardBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.dayForwardBtn)

        # Add spacer
        layout.addStretch()

        # Speed control (right)
        self.speedLabel = QLabel("Speed:")
        self.speedLabel.setStyleSheet("color: white;")
        layout.addWidget(self.speedLabel)

        self.speedCombo = QComboBox()
        self.speedCombo.addItems(["0.5x", "1x", "1.5x", "2x", "5x"])
        self.speedCombo.setCurrentIndex(1)  # Default to 1x
        self.speedCombo.setStyleSheet("background-color: #555;")
        self.speedCombo.currentIndexChanged.connect(self.onSpeedChanged)
        layout.addWidget(self.speedCombo)

    def showDatePicker(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Date")
        layout = QVBoxLayout(dialog)

        calendar = QCalendarWidget()
        calendar.setSelectedDate(self.currentDate)
        calendar.clicked.connect(lambda date: self.updateDate(date, dialog))

        layout.addWidget(calendar)
        dialog.setModal(True)
        dialog.exec()

    def updateDate(self, date, dialog):
        self.currentDate = date
        self.dateBtn.setText(f"Current Date: {date.toString('yyyy-MM-dd')}")
        self.dateChanged.emit(date)
        dialog.accept()

    def onSpeedChanged(self, index):
        speedText = self.speedCombo.currentText()
        speedValue = float(speedText.replace('x', ''))
        self.speedChanged.emit(speedValue)
