from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QLineEdit, QSpinBox, QDialog, QDialogButtonBox, QMessageBox,
    QMainWindow, QHBoxLayout
)
from PyQt6.QtCore import Qt

from src.ui.components.top_bar import TopBar
from src.ui.reservation_manager.components.left_panel import ReservationLeftPanel
from src.ui.reservation_manager.components.right_panel import ReservationRightPanel

from src.service.dto import MakeReservationRequest, EditReservationRequest, DeleteReservationRequest



class ReservationManagerWindow(QMainWindow):
    def __init__(self, on_back, controller):
        super().__init__()
        self.on_back = on_back
        self.controller = controller

        self.setup_ui()


    def setup_ui(self):
        self.setWindowTitle("Reservation Manager")
        self.resize(1200, 800)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.main_widget.setObjectName("ReservationManagerCentral")
        self.main_widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.main_widget.setStyleSheet(
            "#ReservationManagerCentral { background-color: rgb(245, 245, 245); }"
        )
        self.top_bar = TopBar([
            {"label": "← Back", "callback": self.handle_back},
            {"label": "↩ Undo", "callback": self.undo_action},
            {"label": "↪ Redo", "callback": self.redo_action},
        ])
        self.update_undo_redo_buttons()

        self.left_panel = ReservationLeftPanel(
            controller=self.controller,
            make_reservation_click=self.make_reservation_click,
            parent=self
        )

        self.right_panel = ReservationRightPanel(
            controller=self.controller,
            edit_reservation_click=self.edit_reservation_click,
            delete_reservation_click=self.delete_reservation_click,
            parent=self
        )

        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.top_bar)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(160, 10, 160, 0)
        content_layout.setSpacing(10)
        content_layout.addWidget(self.left_panel, stretch=2)
        content_layout.addWidget(self.right_panel, stretch=1)

        main_layout.addLayout(content_layout)






    # Handlers
    def handle_back(self):
        if self.on_back:
            self.on_back()

    def undo_action(self):
        if self.controller.can_undo():
            self.controller.undo()
            self.right_panel.reset_all_filters()
            self.right_panel.populate_reservations_list(self.controller.get_all_reservations())
        self.update_undo_redo_buttons()

    def redo_action(self):
        pass
        if self.controller.can_redo():
            self.controller.redo()
            self.right_panel.reset_all_filters()
            self.right_panel.populate_reservations_list(self.controller.get_all_reservations())
        self.update_undo_redo_buttons()

    def update_undo_redo_buttons(self):
        self.top_bar.set_button_enabled("↩ Undo", self.controller.can_undo())
        self.top_bar.set_button_enabled("↪ Redo", self.controller.can_redo())

    # CRUD
    def make_reservation_click(self):
        if not self.left_panel.check_in_date or not self.left_panel.check_out_date:
            QMessageBox.warning(self, "Warning", "Please select check-in and check-out dates")
            return

        selected_room = self.left_panel.available_rooms.selectedItems()
        if not selected_room:
            QMessageBox.warning(self, "Warning", "Please select a room")
            return

        guest_name = self.left_panel.name_input.text().strip()
        if not guest_name:
            QMessageBox.warning(self, "Warning", "Please enter guest name")
            return

        selected_room_id = selected_room[0].data(Qt.ItemDataRole.UserRole).db_id

        try:
            req = MakeReservationRequest(
                room_id=selected_room_id,
                guest_name=guest_name,
                number_of_guests=self.left_panel.guest_spin.value(),
                check_in_date=self.left_panel.check_in_date.toString("yyyy-MM-dd"),
                check_out_date=self.left_panel.check_out_date.toString("yyyy-MM-dd")
            )
            self.controller.make_reservation(req)
            self.update_undo_redo_buttons()

            self.right_panel.reset_filters()
            self.right_panel.populate_reservations_list(self.controller.get_all_reservations())
            QMessageBox.information(self, "Success", "Reservation created successfully!")
            self.left_panel.name_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to make reservation: {str(e)}")


    def edit_reservation_click(self):
        selected_item = self.right_panel.reservation_list.currentItem()
        reservation = selected_item.data(Qt.ItemDataRole.UserRole)

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
                room_id = self.controller.get_room_by_number(room_input.text().strip()).db_id
                req = EditReservationRequest(
                    reservation_id=reservation.reservation_id,
                    room_id=room_id,
                    guest_name=guest_name_input.text().strip(),
                    number_of_guests=guest_count_input.value(),
                    check_in_date=check_in_input.text().strip(),
                    check_out_date=check_out_input.text().strip()
                )
                self.controller.edit_reservation(req)
                self.update_undo_redo_buttons()

                self.right_panel.reset_all_filters()
                self.right_panel.populate_reservations_list(self.controller.get_all_reservations())
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


    def delete_reservation_click(self):
        selected_item = self.right_panel.reservation_list.currentItem()
        reservation = selected_item.data(Qt.ItemDataRole.UserRole)

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
                self.update_undo_redo_buttons()
                self.right_panel.reset_all_filters()
                self.right_panel.populate_reservations_list(self.controller.get_all_reservations())
                QMessageBox.information(self, "Success", "Reservation deleted successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete reservation: {str(e)}")