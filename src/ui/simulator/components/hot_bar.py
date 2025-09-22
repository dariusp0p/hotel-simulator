from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QLabel,
                             QComboBox, QCalendarWidget, QVBoxLayout, QDialog)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QColor, QFont


class HotBar(QWidget):
    date_changed = pyqtSignal(QDate)
    speed_changed = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_date = QDate.currentDate()
        self.setup_ui()

    def setup_ui(self):
        self.setFixedHeight(50)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(60, 60, 60))
        self.setPalette(palette)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        # Current date button (left) - styled like a label but clickable
        self.date_btn = QPushButton(f"Current Date: {self.current_date.toString('yyyy-MM-dd')}")
        self.date_btn.setStyleSheet("QPushButton {color: white; font-weight: bold; "
                                    "border: 1px solid #777; padding: 5px 10px; "
                                    "background-color: #555;} "
                                    "QPushButton:hover {background-color: #666;}")
        self.date_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.date_btn.clicked.connect(self.show_date_picker)
        layout.addWidget(self.date_btn)

        # Add spacer
        layout.addStretch()

        # Simulation control buttons - base style
        btn_style = (
            "QPushButton {color: white; border: none; "
            "font-weight: bold; padding: 8px; min-width: 80px;} "
        )

        # 1 Day Back button
        self.day_back_btn = QPushButton("◀ 1 Day")
        self.day_back_btn.setStyleSheet(btn_style + "QPushButton {background-color: #4a6ea9;} "
                                                    "QPushButton:hover {background-color: #5a7eb9;}")
        self.day_back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.day_back_btn)

        # Stop button (red with square symbol) - switched order
        self.stop_btn = QPushButton("■ Stop")
        self.stop_btn.setStyleSheet(btn_style + "QPushButton {background-color: #b22222;} "
                                                "QPushButton:hover {background-color: #d32f2f;}")
        self.stop_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.stop_btn)

        # Start button (green)
        self.start_btn = QPushButton("▶ Start")
        self.start_btn.setStyleSheet(btn_style + "QPushButton {background-color: #2e8b57;} "
                                                 "QPushButton:hover {background-color: #3ba968;}")
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.start_btn)

        # 1 Day Forward button
        self.day_forward_btn = QPushButton("1 Day ▶")
        self.day_forward_btn.setStyleSheet(btn_style + "QPushButton {background-color: #4a6ea9;} "
                                                       "QPushButton:hover {background-color: #5a7eb9;}")
        self.day_forward_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.day_forward_btn)

        # Add spacer
        layout.addStretch()

        # Speed control (right)
        self.speed_label = QLabel("Speed:")
        self.speed_label.setStyleSheet("color: white;")
        layout.addWidget(self.speed_label)

        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["0.5x", "1x", "1.5x", "2x", "5x"])
        self.speed_combo.setCurrentIndex(1)  # Default to 1x
        self.speed_combo.setStyleSheet("background-color: #555;")
        self.speed_combo.currentIndexChanged.connect(self.on_speed_changed)
        layout.addWidget(self.speed_combo)

    def show_date_picker(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Date")
        layout = QVBoxLayout(dialog)

        calendar = QCalendarWidget()
        calendar.setSelectedDate(self.current_date)
        calendar.clicked.connect(lambda date: self.update_date(date, dialog))

        layout.addWidget(calendar)
        dialog.setModal(True)
        dialog.exec()

    def update_date(self, date, dialog):
        self.current_date = date
        self.date_btn.setText(f"Current Date: {date.toString('yyyy-MM-dd')}")
        self.date_changed.emit(date)
        dialog.accept()

    def on_speed_changed(self, index):
        speed_text = self.speed_combo.currentText()
        speed_value = float(speed_text.replace('x', ''))
        self.speed_changed.emit(speed_value)