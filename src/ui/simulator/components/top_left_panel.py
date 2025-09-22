from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QGroupBox,
                             QGridLayout, QDateEdit, QSlider, QPushButton, QHBoxLayout)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QFont

from src.service import controller


class TopLeftPanel(QWidget):
    def __init__(self, parent=None, controller=None, generate_reservations_callback=None):
        super().__init__(parent)
        self.generate_reservations_callback = generate_reservations_callback
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(60, 60, 60))
        self.setPalette(palette)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)  # Reduced spacing overall

        # Hotel Stats Section
        stats_title = QLabel("Hotel Statistics")
        stats_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        stats_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_title.setStyleSheet("color: white;")

        stats_separator = QFrame()
        stats_separator.setFrameShape(QFrame.Shape.HLine)
        stats_separator.setFrameShadow(QFrame.Shadow.Sunken)
        stats_separator.setStyleSheet("background-color: #777;")

        layout.addWidget(stats_title)
        layout.addWidget(stats_separator)

        # Stats content
        stats_content = QWidget()
        grid_layout = QGridLayout(stats_content)
        grid_layout.setContentsMargins(0, 0, 0, 0)  # Remove internal margins
        grid_layout.setSpacing(8)

        # Create labels with placeholders
        label_style = "color: white;"
        value_style = "color: #aaa; font-weight: bold;"

        # Row 1: Floors
        floors_label = QLabel("Floors:")
        floors_label.setStyleSheet(label_style)
        self.floors_value = QLabel("0")
        self.floors_value.setStyleSheet(value_style)

        # Row 2: Rooms
        rooms_label = QLabel("Total Rooms:")
        rooms_label.setStyleSheet(label_style)
        self.rooms_value = QLabel("0")
        self.rooms_value.setStyleSheet(value_style)

        # Row 3: Reservations
        reservations_label = QLabel("Total Reservations:")
        reservations_label.setStyleSheet(label_style)
        self.reservations_value = QLabel("0")
        self.reservations_value.setStyleSheet(value_style)

        # Row 4: Income
        income_label = QLabel("Generated Income:")
        income_label.setStyleSheet(label_style)
        self.income_value = QLabel("$0")
        self.income_value.setStyleSheet(value_style)

        # Add to grid
        grid_layout.addWidget(floors_label, 0, 0)
        grid_layout.addWidget(self.floors_value, 0, 1)
        grid_layout.addWidget(rooms_label, 1, 0)
        grid_layout.addWidget(self.rooms_value, 1, 1)
        grid_layout.addWidget(reservations_label, 2, 0)
        grid_layout.addWidget(self.reservations_value, 2, 1)
        grid_layout.addWidget(income_label, 3, 0)
        grid_layout.addWidget(self.income_value, 3, 1)

        layout.addWidget(stats_content)

        # Add spacing between sections
        layout.addSpacing(15)

        # Reservation Generator Section
        gen_title = QLabel("Reservation Generator")
        gen_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        gen_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gen_title.setStyleSheet("color: white;")

        gen_separator = QFrame()
        gen_separator.setFrameShape(QFrame.Shape.HLine)
        gen_separator.setFrameShadow(QFrame.Shadow.Sunken)
        gen_separator.setStyleSheet("background-color: #777;")

        layout.addWidget(gen_title)
        layout.addWidget(gen_separator)

        # Rest of the code remains unchanged

        # Generator content
        gen_content = QWidget()
        gen_layout = QVBoxLayout(gen_content)
        gen_layout.setContentsMargins(0, 0, 0, 0)  # Remove internal margins
        gen_layout.setSpacing(10)

        # Date range selectors
        date_label_style = "color: white;"
        date_edit_style = "background-color: #555; color: white;"

        # From date
        from_layout = QHBoxLayout()
        from_label = QLabel("From:")
        from_label.setStyleSheet(date_label_style)
        from_date = QDateEdit()
        from_date.setDate(QDate.currentDate())
        from_date.setCalendarPopup(True)
        from_date.setStyleSheet(date_edit_style)
        from_layout.addWidget(from_label)
        from_layout.addWidget(from_date, 1)

        # To date
        to_layout = QHBoxLayout()
        to_label = QLabel("To:")
        to_label.setStyleSheet(date_label_style)
        to_date = QDateEdit()
        to_date.setDate(QDate.currentDate().addDays(7))
        to_date.setCalendarPopup(True)
        to_date.setStyleSheet(date_edit_style)
        to_layout.addWidget(to_label)
        to_layout.addWidget(to_date, 1)

        # Occupancy slider
        occupancy_layout = QHBoxLayout()
        occupancy_label = QLabel("Occupancy:")
        occupancy_label.setStyleSheet(date_label_style)
        occupancy_value = QLabel("50%")
        occupancy_value.setStyleSheet(date_label_style)
        occupancy_layout.addWidget(occupancy_label)
        occupancy_layout.addWidget(occupancy_value)

        occupancy_slider = QSlider(Qt.Orientation.Horizontal)
        occupancy_slider.setMinimum(0)
        occupancy_slider.setMaximum(100)
        occupancy_slider.setValue(50)
        occupancy_slider.setStyleSheet("QSlider::handle:horizontal {background-color: #4a6ea9;}")
        occupancy_slider.valueChanged.connect(lambda value: occupancy_value.setText(f"{value}%"))

        # Generate button
        generate_btn = QPushButton("Generate Reservations")
        generate_btn.setStyleSheet(
            "QPushButton {background-color: #2e8b57; color: white; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #3ba968;}"
        )
        self.from_date = from_date
        self.to_date = to_date
        self.occupancy_slider = occupancy_slider
        generate_btn.clicked.connect(lambda: self._handle_generate_btn_click())

        gen_layout.addLayout(from_layout)
        gen_layout.addLayout(to_layout)
        gen_layout.addLayout(occupancy_layout)
        gen_layout.addWidget(occupancy_slider)
        gen_layout.addWidget(generate_btn)

        layout.addWidget(gen_content)
        layout.addStretch()

    def _handle_generate_btn_click(self):
        if self.generate_reservations_callback:
            from_date = self.from_date.date()
            to_date = self.to_date.date()
            occupancy = self.occupancy_slider.value()

            self.generate_reservations_callback(from_date, to_date, occupancy)

    def update_stats(self):
        if not self.controller:
            return

        # Update floors count
        floors = self.controller.get_all_floors()
        self.floors_value.setText(str(len(floors)))

        # Get room count
        total_rooms = self.controller.get_total_rooms_count()
        self.rooms_value.setText(str(total_rooms))

        # Get reservations count
        reservations = self.controller.get_all_reservations()
        self.reservations_value.setText(str(len(reservations)))

        # Get total income
        total_income = self.controller.get_total_reservations_income()
        self.income_value.setText(f"${total_income:,.2f}")