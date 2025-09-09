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
    def __init__(self, on_back=None, controller=None):
        super().__init__()
        self.on_back = on_back
        self.controller = controller

        self.setWindowTitle("Hotel Configurator")
        self.resize(1200, 800)

        self.selected_floor = None

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.grid_canvas = GridCanvas()
        self.grid_canvas.elementDeleteRequested.connect(self.confirm_delete_element)
        self.grid_canvas.elementMoved.connect(self.on_element_moved)

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
            add_room_callback=self.add_room,
            add_hallway_callback=self.add_hallway,
            add_staircase_callback=self.add_staircase
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
        self.selected_floor = item.data(Qt.ItemDataRole.UserRole)
        self.side_bar.floor_name_edit.setText(self.selected_floor.name)
        self.side_bar.floor_name_edit.setPlaceholderText(self.selected_floor.name)
        try:
            floor_grid = self.controller.get_floor_grid(self.selected_floor.name)
            self.grid_canvas.set_floor_elements(floor_grid)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load floor elements: {str(e)}")
            self.grid_canvas.clear_elements()

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
            self.controller.add_floor(floor_name, self.side_bar.floor_list.count())
            self.side_bar.populate_floor_list()
            QMessageBox.information(self, "Success", "Floor added successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add floor: {str(e)}")
            return

    def on_floors_reordered(self):
        for i in range(self.side_bar.floor_list.count()):
            item = self.side_bar.floor_list.item(i)
            floor = item.data(Qt.ItemDataRole.UserRole)
            new_level = self.side_bar.floor_list.count() - 1 - i

            if floor.level != new_level:
                try:
                    self.controller.update_floor_level(floor.db_id, new_level)
                    floor.level = new_level
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to update floor order: {str(e)}")
                    self.side_bar.populate_floor_list()
                    return

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
            self.selected_floor.name = new_name
            self.side_bar.populate_floor_list()
            QMessageBox.information(self, "Success", "Floor renamed successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to rename floor: {str(e)}")

    def on_remove_floor(self):
        selected_floor = self.selected_floor
        print(selected_floor.db_id, selected_floor.name)
        try:
            self.controller.remove_floor(selected_floor.db_id)
            self.side_bar.populate_floor_list()
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



    def add_room(self):
        if not self.selected_floor:
            QMessageBox.warning(self, "Warning", "Please select a floor first")
            return

        position = self.find_first_free_position()
        if position:
            try:
                element_data = {
                    "type": "room",
                    "floor_id": self.selected_floor.db_id,
                    "position": position,
                    "number": "Nr.",
                    "capacity": 2,
                    "price_per_night": 100
                }
                self.controller.hotel_service.add_element(element_data)
                floor_grid = self.controller.get_floor_grid(self.selected_floor.name)
                self.grid_canvas.set_floor_elements(floor_grid)
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
                self.controller.hotel_service.add_element(element_data)
                floor_grid = self.controller.get_floor_grid(self.selected_floor.name)
                self.grid_canvas.set_floor_elements(floor_grid)
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
                self.controller.hotel_service.add_element(element_data)
                floor_grid = self.controller.get_floor_grid(self.selected_floor.name)
                self.grid_canvas.set_floor_elements(floor_grid)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add staircase: {str(e)}")
        else:
            QMessageBox.warning(self, "Warning", "No free space available on this floor")

    def update_room(self, element_widget, number, capacity, price_per_night):
        pass

    def on_element_moved(self, element_id, new_position):
        self.controller.hotel_service.move_element(element_id, new_position)
        floor_grid = self.controller.get_floor_grid(self.selected_floor.name)
        print("UPDATED GRID")
        print(f"Updated grid contains {len(floor_grid)} elements")
        for pos, elem in floor_grid.items():
            print(f"Position {pos}: Element {elem.db_id}")

        self.grid_canvas.set_floor_elements(floor_grid)
        self.grid_canvas.update()

    def confirm_delete_element(self, element_widget):
        element_id = element_widget.element_id
        element = self.selected_floor.elements.get(element_id)

        if not element:
            QMessageBox.critical(
                self,
                "Error",
                "Failed to find the corresponding FloorElement."
            )
            return

        element_type = element.type.capitalize()

        reply = QMessageBox.question(
            self,
            f"Delete {element_type}",
            f"Are you sure you want to delete this {element_type.lower()}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.controller.hotel_service.remove_element(element)

                floor_grid = self.controller.get_floor_grid(self.selected_floor.name)
                self.grid_canvas.set_floor_elements(floor_grid)
                self.grid_canvas.update()
                QMessageBox.information(self, "Success", f"{element_type} successfully deleted!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete {element_type.lower()}: {str(e)}")

