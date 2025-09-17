from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QInputDialog, QMessageBox
)
from PyQt6.QtCore import Qt
import random

from src.ui.components.top_bar import TopBar
from src.ui.hotel_configurator.components.side_bar import SideBar
from src.ui.hotel_configurator.components.hot_bar import HotBar
from src.ui.hotel_configurator.components.grid_canvas_widget import GridCanvas



class HotelConfiguratorWindow(QMainWindow):
    def __init__(self, on_back, controller):
        super().__init__()
        self.on_back = on_back
        self.controller = controller

        self.selected_floor = None

        self.setup_ui()


    def setup_ui(self):
        self.setWindowTitle("Hotel Configurator")
        self.resize(1200, 800)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.grid_canvas = GridCanvas()
        self.grid_canvas.elementDeleteRequested.connect(self.confirm_delete_element)
        self.grid_canvas.elementMoved.connect(self.on_element_moved)
        self.grid_canvas.roomSelected.connect(self.on_room_selected)

        self.top_bar = TopBar([
            {"label": "← Back", "callback": self.handle_back},
            {"label": "↩ Undo", "callback": self.undo_action},
            {"label": "↪ Redo", "callback": self.redo_action},
        ])

        self.side_bar = SideBar(
            controller=self.controller,
            on_floor_selected=self.on_floor_selected,
            on_floors_reordered=self.on_floors_reordered,
            on_add_floor=self.on_add_floor,
            on_remove_floor=self.on_remove_floor,
            on_update_floor_name=self.on_update_floor_name,
            on_update_room=self.update_room
        )

        self.hot_bar = HotBar(
            add_element_callback=self.add_element
        )

        self.layout = QVBoxLayout(self.main_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.grid_canvas)

        self.top_bar.setParent(self.main_widget)
        self.side_bar.setParent(self.main_widget)
        self.hot_bar.setParent(self.main_widget)

        self.resizeEvent(None)



    def handle_back(self):
        if self.on_back:
            self.on_back()

    def undo_action(self):
        pass

    def redo_action(self):
        pass

    def resizeEvent(self, event):
        margin = 10

        self.top_bar.setGeometry(
            margin,
            margin,
            self.width() - 2 * margin,
            self.top_bar.height()
        )

        top_margin = self.top_bar.height() + 2 * margin

        self.side_bar.setGeometry(
            margin,
            top_margin,
            self.side_bar.width(),
            self.height() - top_margin - margin
        )

        self.hot_bar.setGeometry(
            self.side_bar.width() + 2 * margin,
            self.height() - self.hot_bar.height() - margin,
            self.width() - self.side_bar.width() - 3 * margin,
            self.hot_bar.height()
        )



    # Floor CRUD
    def on_floor_selected(self, item):
        self.grid_canvas.select_element(None)
        self.selected_floor = item.data(Qt.ItemDataRole.UserRole)
        self.side_bar.floor_name_edit.setText(self.selected_floor.name)
        self.side_bar.floor_name_edit.setPlaceholderText(self.selected_floor.name)
        try:
            floor_grid = self.controller.get_floor_grid(self.selected_floor.name)
            connections = self.controller.get_floor_connections(self.selected_floor.name)
            self.grid_canvas.set_floor_elements(floor_grid, connections)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load floor elements: {str(e)}")
            self.grid_canvas.clear_floor_elements()

    def on_add_floor(self):
        floor_name, ok = QInputDialog.getText(
            self, "Add New Floor", "Enter floor name:"
        )

        if not ok:
            return

        if not floor_name:
            QMessageBox.warning(self, "Warning", "Please enter floor name")
            return

        try:
            self.grid_canvas.select_element(None)
            self.controller.add_floor(floor_name, self.side_bar.floor_list.count())
            self.side_bar.populate_floor_list()
            QMessageBox.information(self, "Success", "Floor added successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add floor: {str(e)}")
            return

    def on_floors_reordered(self):
        updates = []
        for i in range(self.side_bar.floor_list.count()):
            item = self.side_bar.floor_list.item(i)
            floor = item.data(Qt.ItemDataRole.UserRole)
            new_level = self.side_bar.floor_list.count() - 1 - i
            if floor.level != new_level:
                updates.append((floor.db_id, new_level))

        for floor_id, level in updates:
            try:
                self.controller.update_floor_level(floor_id, level)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update floor order: {str(e)}")
                return

        self.side_bar.populate_floor_list()

    def on_update_floor_name(self):
        if not self.selected_floor:
            QMessageBox.warning(self, "Warning", "Please select a floor first")
            return

        new_name = self.side_bar.floor_name_edit.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Warning", "Please enter floor name")
            return

        old_name = self.selected_floor.name
        if new_name == old_name:
            return

        try:
            self.controller.rename_floor(old_name, new_name)
            self.side_bar.populate_floor_list()
            QMessageBox.information(self, "Success", "Floor renamed successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to rename floor: {str(e)}")

    def on_remove_floor(self):
        selected_floor = self.selected_floor
        num_rooms, num_reservations = self.controller.get_floor_number_of_rooms(selected_floor.db_id)
        if num_rooms > 0:
            reply = QMessageBox.question(
                self,
                "Delete Floor",
                f"This floor contains {num_rooms} room(s) and {num_reservations} reservation(s). Deleting it will remove all rooms and their reservations. Continue?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        try:
            self.controller.remove_floor(selected_floor.db_id)
            self.side_bar.populate_floor_list()
            self.grid_canvas.clear_floor_elements()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to remove floor: {str(e)}")
            return



    def find_first_free_position(self):
        floor_grid = self.controller.get_floor_grid(self.selected_floor.name)

        grid_size = self.grid_canvas.grid_size
        for x in range(grid_size):
            for y in range(grid_size):
                if (x, y) not in floor_grid or floor_grid[(x, y)] is None:
                    return (x, y)
        return None

    def find_random_free_position(self):
        floor_grid = self.controller.get_floor_grid(self.selected_floor.name)

        free_positions = []
        grid_size = self.grid_canvas.grid_size
        for x in range(grid_size):
            for y in range(grid_size):
                if (x, y) not in floor_grid or floor_grid[(x, y)] is None:
                    free_positions.append((x, y))

        if not free_positions:
            return None

        return random.choice(free_positions)



    def on_room_selected(self, room):
        self._selected_room = room
        self.side_bar.display_room_details(room)

    def add_element(self, element_type):
        if not self.selected_floor:
            QMessageBox.warning(self, "Warning", "Please select a floor first")
            return

        position = self.find_first_free_position()
        if position:
            try:
                if element_type == "room":
                    element_data = {
                        "type": "room",
                        "floor_id": self.selected_floor.db_id,
                        "position": position,
                        "number": "1",
                        "capacity": 2,
                        "price_per_night": 100
                    }
                elif element_type == "hallway":
                    element_data = {
                        "type": "hallway",
                        "floor_id": self.selected_floor.db_id,
                        "position": position,
                    }
                elif element_type == "staircase":
                    element_data = {
                        "type": "staircase",
                        "floor_id": self.selected_floor.db_id,
                        "position": position,
                    }
                else:
                    raise ValueError("Invalid element type")
                self.controller.add_element(element_data)
                self.selected_floor = self.controller.get_floor(self.selected_floor.db_id)
                floor_grid = self.controller.get_floor_grid(self.selected_floor.name)
                connections = self.controller.get_floor_connections(self.selected_floor.name)
                self.grid_canvas.set_floor_elements(floor_grid, connections)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add room: {str(e)}")
        else:
            QMessageBox.warning(self, "Warning", "No free space available on this floor")

    def add_hallway(self):
        if not self.selected_floor:
            QMessageBox.warning(self, "Warning", "Please select a floor first")
            return

        position = self.find_first_free_position()
        if position:
            try:
                element_data = {
                    "type": "hallway",
                    "floor_id": self.selected_floor.db_id,
                    "position": position,
                }
                self.controller.add_element(element_data)
                floor_grid = self.controller.get_floor_grid(self.selected_floor.name)
                connections = self.controller.get_floor_connections(self.selected_floor.name)
                self.grid_canvas.set_floor_elements(floor_grid, connections)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add hallway: {str(e)}")
        else:
            QMessageBox.warning(self, "Warning", "No free space available on this floor")

    def add_staircase(self):
        if not self.selected_floor:
            QMessageBox.warning(self, "Warning", "Please select a floor first")
            return

        position = self.find_first_free_position()
        if position:
            try:
                element_data = {
                    "type": "staircase",
                    "floor_id": self.selected_floor.db_id,
                    "position": position,
                }
                self.controller.add_element(element_data)
                floor_grid = self.controller.get_floor_grid(self.selected_floor.name)
                connections = self.controller.get_floor_connections(self.selected_floor.name)
                self.grid_canvas.set_floor_elements(floor_grid, connections)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add staircase: {str(e)}")
        else:
            QMessageBox.warning(self, "Warning", "No free space available on this floor")

    def update_room(self):
        if not hasattr(self, '_selected_room') or not self._selected_room:
            QMessageBox.warning(self, "Warning", "Please select a room first")
            return

        try:
            number = self.side_bar.room_number_edit.text()
            capacity_text = self.side_bar.room_capacity_edit.text()
            price_text = self.side_bar.room_price_edit.text()

            if not number:
                QMessageBox.warning(self, "Warning", "Room number cannot be empty")
                return
            try:
                capacity = int(capacity_text)
                if capacity <= 0:
                    raise ValueError("Capacity must be positive")
            except ValueError:
                QMessageBox.warning(self, "Warning", "Capacity must be a positive number")
                return
            try:
                price = float(price_text)
                if price < 0:
                    raise ValueError("Price cannot be negative")
            except ValueError:
                QMessageBox.warning(self, "Warning", "Price must be a valid number")
                return

            self.controller.edit_room(self._selected_room.element_id, number, capacity, price)

            floor_grid = self.controller.get_floor_grid(self.selected_floor.name)
            connections = self.controller.get_floor_connections(self.selected_floor.name)
            self.grid_canvas.set_floor_elements(floor_grid, connections)
            self.grid_canvas.select_element(None)
            self.grid_canvas.update()

            QMessageBox.information(self, "Success", "Room updated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update room: {str(e)}")

    def on_element_moved(self, element_id, new_position):
        self.controller.move_element(element_id, new_position)
        floor_grid = self.controller.get_floor_grid(self.selected_floor.name)
        connections = self.controller.get_floor_connections(self.selected_floor.name)
        self.grid_canvas.set_floor_elements(floor_grid, connections)
        self.grid_canvas.update()

    def confirm_delete_element(self, element_widget):
        element_id = element_widget.element_id
        element = self.selected_floor.elements.get(element_id)

        if not element:
            QMessageBox.critical(self, "Error", "Failed to find the corresponding FloorElement.")
            return

        element_type = element.type.capitalize()

        if element.type == "room":
            num_reservations = self.controller.get_room_number_of_reservations(element.db_id)
            if num_reservations > 0:
                reply = QMessageBox.question(
                    self,
                    "Delete Room",
                    f"This room has {num_reservations} reservation(s). Deleting it will remove all reservations. Continue?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                if reply != QMessageBox.StandardButton.Yes:
                    return

        try:
            self.controller.remove_element(element)
            floor_grid = self.controller.get_floor_grid(self.selected_floor.name)
            connections = self.controller.get_floor_connections(self.selected_floor.name)
            self.grid_canvas.set_floor_elements(floor_grid, connections)
            self.grid_canvas.select_element(None)
            self.grid_canvas.update()
            if element.type == "room":
                QMessageBox.information(self, "Success", f"Room successfully deleted!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete {element_type.lower()}: {str(e)}")

