from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, QPushButton, QCalendarWidget,
    QListWidget, QListWidgetItem, QMessageBox, QDialog, QDialogButtonBox, QLabel, QFrame, QSizePolicy
)
from datetime import datetime


class ReservationRightPanel(QWidget):
    """Right panel for managing reservations."""
    def __init__(self, controller, editReservationClick, deleteReservationClick, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.editReservationClick = editReservationClick
        self.deleteReservationClick = deleteReservationClick

        self.setupUi()

    def setupUi(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(60, 60, 60))
        self.setPalette(palette)

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(10)

        # Search Section Title
        searchTitle = QLabel("Search Reservations")
        searchTitle.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        searchTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        searchTitle.setStyleSheet("color: white;")
        searchSeparator = QFrame()
        searchSeparator.setFrameShape(QFrame.Shape.HLine)
        searchSeparator.setFrameShadow(QFrame.Shadow.Sunken)
        searchSeparator.setStyleSheet("background-color: #777;")

        # Search Inputs
        directRow = QHBoxLayout()
        self.directSearchBar = QLineEdit()
        self.directSearchBar.setPlaceholderText("Direct search...")
        self.directSearchBar.setStyleSheet(
            "QLineEdit {background-color: #444; color: white; border: 1px solid #666; padding: 5px;}"
        )
        self.directSearchBar.textChanged.connect(self._onDirectChange)
        self.directSearchBtn = QPushButton("Search")
        self.directSearchBtn.setEnabled(False)
        self.directSearchBtn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        self.directSearchBtn.clicked.connect(self._directSearch)
        directRow.addWidget(self.directSearchBar)
        directRow.addWidget(self.directSearchBtn)

        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search...")
        self.searchBar.setStyleSheet(
            "QLineEdit {background-color: #444; color: white; border: 1px solid #666; padding: 5px;}"
        )
        self.searchBar.textChanged.connect(self._onFilterChange)

        dateRow = QHBoxLayout()
        self.fromBtn = QPushButton("From")
        self.toBtn = QPushButton("To")
        self.clearFiltersBtn = QPushButton("X")
        for btn in [self.fromBtn, self.toBtn, self.clearFiltersBtn]:
            btn.setMinimumHeight(36)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.setStyleSheet(
                "QPushButton {background-color: #555; color: white; border: none; padding: 6px; font-weight: bold;}"
                "QPushButton:hover {background-color: #666;}"
            )
        self.clearFiltersBtn.setStyleSheet(
            "QPushButton {background-color: #a94a4a; color: white; border: none; font-weight: bold;}"
            "QPushButton:hover {background-color: #b95a5a;}"
        )
        self.fromBtn.clicked.connect(lambda: self.openDatePicker("from"))
        self.toBtn.clicked.connect(lambda: self.openDatePicker("to"))
        self.clearFiltersBtn.clicked.connect(self.resetAllFilters)
        dateRow.addWidget(self.fromBtn)
        dateRow.addWidget(self.toBtn)
        dateRow.addWidget(self.clearFiltersBtn)

        # Reservation List Title
        listTitle = QLabel("Reservations")
        listTitle.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        listTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        listTitle.setStyleSheet("color: white;")
        listSeparator = QFrame()
        listSeparator.setFrameShape(QFrame.Shape.HLine)
        listSeparator.setFrameShadow(QFrame.Shadow.Sunken)
        listSeparator.setStyleSheet("background-color: #777;")

        self.reservationList = QListWidget()
        self.reservationList.setStyleSheet(
            "QListWidget {background-color: #444; color: white; border: 1px solid #666; padding: 5px;}"
        )
        self.reservationList.itemSelectionChanged.connect(self._onSelectionChange)

        # Actions
        actions = QHBoxLayout()
        self.editBtn = QPushButton("Edit")
        self.deleteBtn = QPushButton("Delete")
        self.editBtn.setEnabled(False)
        self.deleteBtn.setEnabled(False)
        self.editBtn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        self.deleteBtn.setStyleSheet(
            "QPushButton {background-color: #a94a4a; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #b95a5a;}"
        )
        self.editBtn.clicked.connect(self.editReservationClick)
        self.deleteBtn.clicked.connect(self.deleteReservationClick)
        actions.addWidget(self.editBtn)
        actions.addWidget(self.deleteBtn)

        # Assemble layout
        mainLayout.addWidget(searchTitle)
        mainLayout.addWidget(searchSeparator)
        mainLayout.addLayout(directRow)
        mainLayout.addWidget(self.searchBar)
        mainLayout.addLayout(dateRow)
        mainLayout.addWidget(listTitle)
        mainLayout.addWidget(listSeparator)
        mainLayout.addWidget(self.reservationList)
        mainLayout.addLayout(actions)

        self.refresh()

    def refresh(self):
        reservations = self.controller.get_all_reservations()
        self.populateReservationsList(reservations)

    def populateReservationsList(self, reservations):
        self.reservationList.clear()
        for r in reservations:
            text = (
                f"{r.reservation_id} | Room {r.room_number} | "
                f"{r.guest_name} | {r.check_in_date} | {r.check_out_date} | {r.number_of_guests}"
            )
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, r)
            self.reservationList.addItem(item)

    def _onSelectionChange(self):
        has = bool(self.reservationList.selectedItems())
        self.editBtn.setEnabled(has)
        self.deleteBtn.setEnabled(has)

    def _onDirectChange(self):
        self.directSearchBtn.setEnabled(bool(self.directSearchBar.text().strip()))

    def _directSearch(self):
        self.resetFilters()
        s = self.directSearchBar.text().strip()
        res = self.controller.reservation_direct_search(s)
        if not res:
            QMessageBox.information(self, "No Results", "No reservations found.")
            return
        self.populateReservationsList(res)

    def _onFilterChange(self):
        self.directSearchBar.clear()
        s = self.searchBar.text().strip()
        fromDate = None
        toDate = None
        if self.fromBtn.text() != "From":
            fromDate = datetime.strptime(self.fromBtn.text().split(" ")[1].strip(), "%Y-%m-%d").date()
        if self.toBtn.text() != "To":
            toDate = datetime.strptime(self.toBtn.text().split(" ")[1].strip(), "%Y-%m-%d").date()
        res = self.controller.reservation_search(s, fromDate, toDate)
        self.populateReservationsList(res)

    def resetFilters(self):
        self.fromBtn.setText("From")
        self.toBtn.setText("To")
        self.searchBar.setText("")
        self.populateReservationsList(self.controller.get_all_reservations())

    def resetAllFilters(self):
        self.directSearchBar.clear()
        self.resetFilters()

    def openDatePicker(self, which):
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
            selectedDate = calendar.selectedDate()
            if which == "from":
                self.fromBtn.setText(f"From {selectedDate.toString('yyyy-MM-dd')}")
            else:
                self.toBtn.setText(f"To {selectedDate.toString('yyyy-MM-dd')}")

            dialog.accept()
            self._onFilterChange()

        def reject():
            dialog.reject()

        buttons.accepted.connect(accept)
        buttons.rejected.connect(reject)

        dialog.setLayout(layout)
        dialog.exec()
