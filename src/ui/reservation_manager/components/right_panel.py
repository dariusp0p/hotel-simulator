from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, QPushButton, QCalendarWidget,
    QListWidget, QListWidgetItem, QMessageBox, QDialog, QDialogButtonBox, QLabel, QFrame, QSizePolicy
)
from datetime import datetime



class ReservationRightPanel(QWidget):
    def __init__(self, controller, edit_reservation_click, delete_reservation_click, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.edit_reservation_click = edit_reservation_click
        self.delete_reservation_click = delete_reservation_click

        self.setup_ui()

    def setup_ui(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(60, 60, 60))
        self.setPalette(palette)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Search Section Title
        search_title = QLabel("Search Reservations")
        search_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        search_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        search_title.setStyleSheet("color: white;")
        search_separator = QFrame()
        search_separator.setFrameShape(QFrame.Shape.HLine)
        search_separator.setFrameShadow(QFrame.Shadow.Sunken)
        search_separator.setStyleSheet("background-color: #777;")

        # Search Inputs
        direct_row = QHBoxLayout()
        self.direct_search_bar = QLineEdit()
        self.direct_search_bar.setPlaceholderText("Direct search...")
        self.direct_search_bar.setStyleSheet(
            "QLineEdit {background-color: #444; color: white; border: 1px solid #666; padding: 5px;}"
        )
        self.direct_search_bar.textChanged.connect(self._on_direct_change)
        self.direct_search_btn = QPushButton("Search")
        self.direct_search_btn.setEnabled(False)
        self.direct_search_btn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        self.direct_search_btn.clicked.connect(self._direct_search)
        direct_row.addWidget(self.direct_search_bar)
        direct_row.addWidget(self.direct_search_btn)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.setStyleSheet(
            "QLineEdit {background-color: #444; color: white; border: 1px solid #666; padding: 5px;}"
        )
        self.search_bar.textChanged.connect(self._on_filter_change)

        date_row = QHBoxLayout()
        self.from_btn = QPushButton("From")
        self.to_btn = QPushButton("To")
        self.clear_filters_btn = QPushButton("X")
        for btn in [self.from_btn, self.to_btn, self.clear_filters_btn]:
            btn.setMinimumHeight(36)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.setStyleSheet(
                "QPushButton {background-color: #555; color: white; border: none; padding: 6px; font-weight: bold;}"
                "QPushButton:hover {background-color: #666;}"
            )
        self.clear_filters_btn.setStyleSheet(
            "QPushButton {background-color: #a94a4a; color: white; border: none; font-weight: bold;}"
            "QPushButton:hover {background-color: #b95a5a;}"
        )
        self.from_btn.clicked.connect(lambda: self.open_date_picker("from"))
        self.to_btn.clicked.connect(lambda: self.open_date_picker("to"))
        self.clear_filters_btn.clicked.connect(self.reset_all_filters)
        date_row.addWidget(self.from_btn)
        date_row.addWidget(self.to_btn)
        date_row.addWidget(self.clear_filters_btn)

        # Reservation List Title
        list_title = QLabel("Reservations")
        list_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        list_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        list_title.setStyleSheet("color: white;")
        list_separator = QFrame()
        list_separator.setFrameShape(QFrame.Shape.HLine)
        list_separator.setFrameShadow(QFrame.Shadow.Sunken)
        list_separator.setStyleSheet("background-color: #777;")

        self.reservation_list = QListWidget()
        self.reservation_list.setStyleSheet(
            "QListWidget {background-color: #444; color: white; border: 1px solid #666; padding: 5px;}"
        )
        self.reservation_list.itemSelectionChanged.connect(self._on_selection_change)

        # Actions
        actions = QHBoxLayout()
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.edit_btn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        self.delete_btn.setStyleSheet(
            "QPushButton {background-color: #a94a4a; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #b95a5a;}"
        )
        self.edit_btn.clicked.connect(self.edit_reservation_click)
        self.delete_btn.clicked.connect(self.delete_reservation_click)
        actions.addWidget(self.edit_btn)
        actions.addWidget(self.delete_btn)

        # Assemble layout
        main_layout.addWidget(search_title)
        main_layout.addWidget(search_separator)
        main_layout.addLayout(direct_row)
        main_layout.addWidget(self.search_bar)
        main_layout.addLayout(date_row)
        main_layout.addWidget(list_title)
        main_layout.addWidget(list_separator)
        main_layout.addWidget(self.reservation_list)
        main_layout.addLayout(actions)

        self.refresh()


    def refresh(self):
        reservations = self.controller.get_all_reservations()
        self.populate_reservations_list(reservations)

    def populate_reservations_list(self, reservations):
        self.reservation_list.clear()
        for r in reservations:
            text = (
                f"{r.reservation_id} | Room {r.room_number} | "
                f"{r.guest_name} | {r.check_in_date} | {r.check_out_date} | {r.number_of_guests}"
            )
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, r)
            self.reservation_list.addItem(item)


    def _on_selection_change(self):
        has = bool(self.reservation_list.selectedItems())
        self.edit_btn.setEnabled(has)
        self.delete_btn.setEnabled(has)

    def _on_direct_change(self):
        self.direct_search_btn.setEnabled(bool(self.direct_search_bar.text().strip()))

    def _direct_search(self):
        self.reset_filters()
        s = self.direct_search_bar.text().strip()
        res = self.controller.reservation_direct_search(s)
        if not res:
            QMessageBox.information(self, "No Results", "No reservations found.")
            return
        self.populate_reservations_list(res)

    def _on_filter_change(self):
        self.direct_search_bar.clear()
        s = self.search_bar.text().strip()
        from_date = None
        to_date = None
        if self.from_btn.text() != "From":
            from_date = datetime.strptime(self.from_btn.text().split(" ")[1].strip(), "%Y-%m-%d").date()
        if self.to_btn.text() != "To":
            to_date = datetime.strptime(self.to_btn.text().split(" ")[1].strip(), "%Y-%m-%d").date()
        res = self.controller.reservation_search(s, from_date, to_date)
        self.populate_reservations_list(res)

    def reset_filters(self):
        self.from_btn.setText("From")
        self.to_btn.setText("To")
        self.search_bar.setText("")
        self.populate_reservations_list(self.controller.get_all_reservations())

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
        calendar.setStyleSheet(
            "QCalendarWidget {background-color: #444; color: white; border: 1px solid #666; border-radius: 4px;}"
            "QCalendarWidget QAbstractItemView {background-color: #444; color: white; selection-background-color: #4a6ea9;}"
            "QCalendarWidget QWidget#qt_calendar_navigationbar {background-color: #555; color: white;}"
        )
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
            self._on_filter_change()

        def reject():
            dialog.reject()

        buttons.accepted.connect(accept)
        buttons.rejected.connect(reject)

        dialog.setLayout(layout)
        dialog.exec()
