from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QLineEdit, QSpinBox, QDialog, QDialogButtonBox, QMessageBox,
    QMainWindow, QHBoxLayout
)
from PyQt6.QtCore import Qt

from src.view.components.top_bar import TopBar
from src.view.reservation_manager.components.left_panel import ReservationLeftPanel
from src.view.reservation_manager.components.right_panel import ReservationRightPanel

from src.controller.dto import MakeReservationRequest, EditReservationRequest, DeleteReservationRequest


class ReservationManagerWindow(QMainWindow):
    """Reservation Manager window."""
    def __init__(self, onBack, controller):
        super().__init__()
        self.onBack = onBack
        self.controller = controller

        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Reservation Manager")
        self.resize(1200, 800)

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)

        self.mainWidget.setObjectName("ReservationManagerCentral")
        self.mainWidget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.mainWidget.setStyleSheet(
            "#ReservationManagerCentral { background-color: rgb(245, 245, 245); }"
        )
        self.topBar = TopBar([
            {"label": "← Back", "callback": self.handleBack},
            {"label": "↩ Undo", "callback": self.undoAction},
            {"label": "↪ Redo", "callback": self.redoAction},
        ])
        self.updateUndoRedoButtons()

        self.leftPanel = ReservationLeftPanel(
            controller=self.controller,
            makeReservationClick=self.makeReservationClick,
            parent=self
        )

        self.rightPanel = ReservationRightPanel(
            controller=self.controller,
            editReservationClick=self.editReservationClick,
            deleteReservationClick=self.deleteReservationClick,
            parent=self
        )

        mainLayout = QVBoxLayout(self.mainWidget)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(0)

        mainLayout.addWidget(self.topBar)

        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(160, 10, 160, 0)
        contentLayout.setSpacing(10)
        contentLayout.addWidget(self.leftPanel, stretch=2)
        contentLayout.addWidget(self.rightPanel, stretch=1)

        mainLayout.addLayout(contentLayout)

    # Handlers
    def handleBack(self):
        if self.onBack:
            self.onBack()

    def undoAction(self):
        if self.controller.can_undo():
            self.controller.undo()
            self.rightPanel.resetAllFilters()
            self.rightPanel.populateReservationsList(self.controller.get_all_reservations())
        self.updateUndoRedoButtons()

    def redoAction(self):
        if self.controller.can_redo():
            self.controller.redo()
            self.rightPanel.resetAllFilters()
            self.rightPanel.populateReservationsList(self.controller.get_all_reservations())
        self.updateUndoRedoButtons()

    def updateUndoRedoButtons(self):
        self.topBar.setButtonEnabled("↩ Undo", self.controller.can_undo())
        self.topBar.setButtonEnabled("↪ Redo", self.controller.can_redo())

    # CRUD
    def makeReservationClick(self):
        if not self.leftPanel.checkInDate or not self.leftPanel.checkOutDate:
            QMessageBox.warning(self, "Warning", "Please select check-in and check-out dates")
            return

        selectedRoom = self.leftPanel.availableRooms.selectedItems()
        if not selectedRoom:
            QMessageBox.warning(self, "Warning", "Please select a room")
            return

        guestName = self.leftPanel.nameInput.text().strip()
        if not guestName:
            QMessageBox.warning(self, "Warning", "Please enter guest name")
            return

        selectedRoomId = selectedRoom[0].data(Qt.ItemDataRole.UserRole).db_id

        try:
            req = MakeReservationRequest(
                room_id=selectedRoomId,
                guest_name=guestName,
                number_of_guests=self.leftPanel.guestSpin.value(),
                check_in_date=self.leftPanel.checkInDate.toString("yyyy-MM-dd"),
                check_out_date=self.leftPanel.checkOutDate.toString("yyyy-MM-dd")
            )
            self.controller.make_reservation(req)
            self.updateUndoRedoButtons()

            self.rightPanel.resetFilters()
            self.rightPanel.populateReservationsList(self.controller.get_all_reservations())
            QMessageBox.information(self, "Success", "Reservation created successfully!")
            self.leftPanel.nameInput.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to make reservation: {str(e)}")

    def editReservationClick(self):
        selectedItem = self.rightPanel.reservationList.currentItem()
        reservation = selectedItem.data(Qt.ItemDataRole.UserRole)

        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Reservation")

        layout = QVBoxLayout()

        roomInput = QLineEdit(reservation.room_number)
        guestNameInput = QLineEdit(reservation.guest_name)
        guestCountInput = QSpinBox()
        guestCountInput.setValue(reservation.number_of_guests)
        guestCountInput.setMinimum(1)
        guestCountInput.setMaximum(8)
        checkInInput = QLineEdit(reservation.check_in_date.strftime("%Y-%m-%d"))
        checkOutInput = QLineEdit(reservation.check_out_date.strftime("%Y-%m-%d"))

        layout.addWidget(QLabel("Room Number:"))
        layout.addWidget(roomInput)
        layout.addWidget(QLabel("Guest Name:"))
        layout.addWidget(guestNameInput)
        layout.addWidget(QLabel("Number of Guests:"))
        layout.addWidget(guestCountInput)
        layout.addWidget(QLabel("Check-in Date (YYYY-MM-DD):"))
        layout.addWidget(checkInInput)
        layout.addWidget(QLabel("Check-out Date (YYYY-MM-DD):"))
        layout.addWidget(checkOutInput)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        layout.addWidget(buttons)

        def confirm():
            if not all([
                roomInput.text().strip(),
                guestNameInput.text().strip(),
                checkInInput.text().strip(),
                checkOutInput.text().strip()
            ]):
                QMessageBox.warning(self, "Warning", "All fields must be filled out.")
                return

            try:
                roomId = self.controller.get_room_by_number(roomInput.text().strip()).db_id
                req = EditReservationRequest(
                    reservation_id=reservation.reservation_id,
                    room_id=roomId,
                    guest_name=guestNameInput.text().strip(),
                    number_of_guests=guestCountInput.value(),
                    check_in_date=checkInInput.text().strip(),
                    check_out_date=checkOutInput.text().strip()
                )
                self.controller.edit_reservation(req)
                self.updateUndoRedoButtons()

                self.rightPanel.resetAllFilters()
                self.rightPanel.populateReservationsList(self.controller.get_all_reservations())
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

    def deleteReservationClick(self):
        selectedItem = self.rightPanel.reservationList.currentItem()
        reservation = selectedItem.data(Qt.ItemDataRole.UserRole)

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete reservation {reservation.reservation_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                req = DeleteReservationRequest(reservation_id=reservation.reservation_id)
                self.controller.delete_reservation(req)
                self.updateUndoRedoButtons()
                self.rightPanel.resetAllFilters()
                self.rightPanel.populateReservationsList(self.controller.get_all_reservations())
                QMessageBox.information(self, "Success", "Reservation deleted successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete reservation: {str(e)}")
