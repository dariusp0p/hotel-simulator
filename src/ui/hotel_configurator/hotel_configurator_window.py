from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QListWidget, QListWidgetItem,
    QInputDialog, QMessageBox, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont

from src.ui.hotel_configurator.grid_canvas_widget import GridCanvas



class FloorListWidget(QListWidget):
    floorsReordered = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Enable drag and drop
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

        # Style
        self.setStyleSheet("""
            QListWidget {
                background-color: #555;
                color: white;
                border: none;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #666;
            }
            QListWidget::item:selected {
                background-color: #4a6ea9;
            }
            QListWidget::item:hover {
                background-color: #666;
            }
        """)

    def dropEvent(self, event):
        # Call parent implementation to handle the visual reordering
        super().dropEvent(event)
        # Emit signal that floors have been reordered
        self.floorsReordered.emit()












class HotelConfiguratorWindow(QMainWindow):
    def __init__(self, on_back=None, controller=None):
        super().__init__()
        self.on_back = on_back
        self.controller = controller

        self.setWindowTitle("Hotel Configurator")
        self.resize(1200, 800)

        self.selected_floor = None

        # Create main widget
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Create the grid canvas
        self.grid_canvas = GridCanvas()

        self.grid_canvas.elementDeleteRequested.connect(self.confirm_delete_element)

        # Create top bar
        self.top_bar = self.create_top_bar()

        # Create side bar
        self.side_bar = self.create_side_bar()

        self.hot_bar = self.create_hot_bar()

        # Set layout
        self.layout = QVBoxLayout(self.main_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.grid_canvas)

        # Position top bar and side bar over the grid
        self.top_bar.setParent(self.main_widget)
        self.side_bar.setParent(self.main_widget)
        self.hot_bar.setParent(self.main_widget)

        # Update UI layout when resized
        self.resizeEvent(None)

    def create_top_bar(self):
        top_bar = QWidget()
        top_bar.setFixedHeight(50)
        top_bar.setAutoFillBackground(True)

        # Style the top bar
        palette = top_bar.palette()
        palette.setColor(top_bar.backgroundRole(), QColor(60, 60, 60))
        top_bar.setPalette(palette)

        # Layout
        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(10, 5, 10, 5)

        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setFixedSize(80, 40)
        back_btn.setStyleSheet(
            "QPushButton {background-color: #333; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #555;}"
        )
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(self.handle_back)

        # Undo button
        undo_btn = QPushButton("↩ Undo")
        undo_btn.setFixedSize(80, 40)
        undo_btn.setStyleSheet(
            "QPushButton {background-color: #333; color: white; border: none; padding: 8px;} "
            "QPushButton:hover {background-color: #555;}"
        )
        undo_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Redo button
        redo_btn = QPushButton("↪ Redo")
        redo_btn.setFixedSize(80, 40)
        redo_btn.setStyleSheet(
            "QPushButton {background-color: #333; color: white; border: none; padding: 8px;} "
            "QPushButton:hover {background-color: #555;}"
        )
        redo_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Title
        title = QLabel("Hotel Configurator")
        title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")

        # Add widgets to layout
        layout.addWidget(back_btn)
        layout.addWidget(undo_btn)
        layout.addWidget(redo_btn)
        layout.addSpacing(20)
        layout.addWidget(title)
        layout.addStretch()

        return top_bar

    def create_side_bar(self):
        side_bar = QWidget()
        side_bar.setFixedWidth(250)
        side_bar.setAutoFillBackground(True)

        # Style the side bar to match top and hot bars
        palette = side_bar.palette()
        palette.setColor(side_bar.backgroundRole(), QColor(60, 60, 60))
        side_bar.setPalette(palette)

        # Main layout for side bar
        main_layout = QVBoxLayout(side_bar)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Create upper section (Floors)
        upper_section = QWidget()
        upper_layout = QVBoxLayout(upper_section)
        upper_layout.setContentsMargins(0, 0, 0, 0)
        upper_layout.setSpacing(5)

        # Floors title
        floors_title = QLabel("Floors")
        floors_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        floors_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        floors_title.setStyleSheet("color: white;")

        # Add separator after title
        floors_separator = QFrame()
        floors_separator.setFrameShape(QFrame.Shape.HLine)
        floors_separator.setFrameShadow(QFrame.Shadow.Sunken)
        floors_separator.setStyleSheet("background-color: #777;")

        # Create floor list widget
        self.floor_list = FloorListWidget()
        self.floor_list.itemClicked.connect(self.on_floor_selected)
        self.floor_list.floorsReordered.connect(self.on_floors_reordered)

        # Create buttons container
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 5, 0, 0)
        buttons_layout.setSpacing(10)

        # Add floor button
        add_floor_btn = QPushButton("Add")
        add_floor_btn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        add_floor_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_floor_btn.clicked.connect(self.on_add_floor)

        # Remove floor button
        remove_floor_btn = QPushButton("Remove")
        remove_floor_btn.setStyleSheet(
            "QPushButton {background-color: #a94a4a; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #b95a5a;}"
        )
        remove_floor_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_floor_btn.clicked.connect(self.on_remove_floor)

        # Add buttons to layout
        buttons_layout.addWidget(add_floor_btn)
        buttons_layout.addWidget(remove_floor_btn)

        # Add widgets to upper layout
        upper_layout.addWidget(floors_title)
        upper_layout.addWidget(floors_separator)
        upper_layout.addWidget(self.floor_list, 1)
        upper_layout.addWidget(buttons_container)

        # Create lower section (Selected Floor)
        lower_section = QWidget()
        lower_layout = QVBoxLayout(lower_section)
        lower_layout.setContentsMargins(0, 0, 0, 0)
        lower_layout.setSpacing(5)

        # Selected Floor title
        selected_floor_title = QLabel("Selected Floor")
        selected_floor_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        selected_floor_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        selected_floor_title.setStyleSheet("color: white;")

        # Add separator after title
        selected_floor_separator = QFrame()
        selected_floor_separator.setFrameShape(QFrame.Shape.HLine)
        selected_floor_separator.setFrameShadow(QFrame.Shadow.Sunken)
        selected_floor_separator.setStyleSheet("background-color: #777;")

        # Selected floor content
        self.selected_floor_panel = QWidget()
        self.selected_floor_panel.setStyleSheet("background-color: #555;")
        selected_floor_layout = QVBoxLayout(self.selected_floor_panel)

        # Name edit section
        name_edit_container = QWidget()
        name_edit_layout = QHBoxLayout(name_edit_container)
        name_edit_layout.setContentsMargins(0, 0, 0, 0)

        self.floor_name_edit = QLineEdit()
        self.floor_name_edit.setStyleSheet(
            "background-color: #444; color: white; border: 1px solid #666; padding: 5px;")
        self.floor_name_edit.setPlaceholderText("Floor name")

        update_name_btn = QPushButton("Update")
        update_name_btn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; padding: 5px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        update_name_btn.clicked.connect(self.on_update_floor_name)

        name_edit_layout.addWidget(self.floor_name_edit)
        name_edit_layout.addWidget(update_name_btn)

        selected_floor_layout.addWidget(name_edit_container)
        selected_floor_layout.addStretch()

        # Add widgets to lower layout
        lower_layout.addWidget(selected_floor_title)
        lower_layout.addWidget(selected_floor_separator)
        lower_layout.addWidget(self.selected_floor_panel, 1)

        # Add both sections to main layout
        main_layout.addWidget(upper_section, 1)
        main_layout.addWidget(lower_section, 1)

        # Populate floor list
        self.populate_floor_list()

        return side_bar

    def create_hot_bar(self):
        hot_bar = QWidget()
        hot_bar.setFixedHeight(60)
        hot_bar.setAutoFillBackground(True)

        # Style the hot bar
        palette = hot_bar.palette()
        palette.setColor(hot_bar.backgroundRole(), QColor(60, 60, 60))
        hot_bar.setPalette(palette)

        # Layout
        layout = QHBoxLayout(hot_bar)
        layout.setContentsMargins(10, 5, 10, 5)

        # Add stretch before buttons to center them
        layout.addStretch()

        # Add Room button
        add_room_btn = QPushButton("Add Room")
        add_room_btn.setFixedHeight(40)
        add_room_btn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        add_room_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_room_btn.clicked.connect(self.add_room)

        # Add Hallway button
        add_hallway_btn = QPushButton("Add Hallway")
        add_hallway_btn.setFixedHeight(40)
        add_hallway_btn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        add_hallway_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_hallway_btn.clicked.connect(self.add_hallway)

        # Add Staircase button
        add_staircase_btn = QPushButton("Add Staircase")
        add_staircase_btn.setFixedHeight(40)
        add_staircase_btn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        add_staircase_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_staircase_btn.clicked.connect(self.add_staircase)

        # Add widgets to layout
        layout.addWidget(add_room_btn)
        layout.addWidget(add_hallway_btn)
        layout.addWidget(add_staircase_btn)

        # Add stretch after buttons to center them
        layout.addStretch()

        return hot_bar

    def resizeEvent(self, event):
        margin = 10

        # Position the top bar
        self.top_bar.setGeometry(
            margin,
            margin,
            self.width() - 2 * margin,
            self.top_bar.height()
        )

        # Position the side bar - extend to the bottom with just a small gap
        top_margin = self.top_bar.height() + 2 * margin
        self.side_bar.setGeometry(
            margin,
            top_margin,
            self.side_bar.width(),
            self.height() - top_margin - margin  # Leave just bottom margin
        )

        # Position the hot bar
        self.hot_bar.setGeometry(
            self.side_bar.width() + 2 * margin,
            self.height() - self.hot_bar.height() - margin,
            self.width() - self.side_bar.width() - 3 * margin,
            self.hot_bar.height()
        )

    def handle_back(self):
        if self.on_back:
            self.on_back()

    def populate_floor_list(self):
        self.floor_list.clear()

        floors = self.controller.get_sidebar_floors()
        for floor in floors:
            item = QListWidgetItem(floor.name)
            item.setData(Qt.ItemDataRole.UserRole, floor)
            self.floor_list.addItem(item)

    def on_floor_selected(self, item):
        self.selected_floor = item.data(Qt.ItemDataRole.UserRole)
        # Update the floor name edit field with current name
        self.floor_name_edit.setText(self.selected_floor.name)
        self.floor_name_edit.setPlaceholderText(self.selected_floor.name)

        # Load floor elements from the controller
        try:
            floor_grid = self.controller.get_floor_grid(self.selected_floor.name)
            self.grid_canvas.set_floor_elements(floor_grid)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load floor elements: {str(e)}")
            self.grid_canvas.clear_elements()


    def on_update_floor_name(self):
        if not self.selected_floor:
            QMessageBox.warning(self, "Warning", "Please select a floor first")
            return

        new_name = self.floor_name_edit.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Warning", "Please enter floor name")
            return

        old_name = self.selected_floor.name
        if new_name == old_name:
            return

        try:
            self.controller.rename_floor(old_name, new_name)
            self.selected_floor.name = new_name
            self.populate_floor_list()
            QMessageBox.information(self, "Success", "Floor renamed successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to rename floor: {str(e)}")

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
            self.controller.add_floor(floor_name, self.floor_list.count())
            self.populate_floor_list()
            QMessageBox.information(self, "Success", "Floor added successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add floor: {str(e)}")
            return

    def on_floors_reordered(self):
        # Update the levels of all floors based on their new positions
        for i in range(self.floor_list.count()):
            item = self.floor_list.item(i)
            floor = item.data(Qt.ItemDataRole.UserRole)
            # Set level in reverse order (top item has highest level)
            new_level = self.floor_list.count() - 1 - i

            # Only update if level changed
            if floor.level != new_level:
                try:
                    self.controller.update_floor_level(floor.db_id, new_level)
                    # Update the local floor object
                    floor.level = new_level
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to update floor order: {str(e)}")
                    # Refresh the list to show the correct order
                    self.populate_floor_list()
                    return

    def on_remove_floor(self):
        # Get the currently selected floor and remove it
        selected_floor = self.selected_floor
        print(selected_floor.db_id, selected_floor.name)
        try:
            self.controller.remove_floor(selected_floor.db_id)
            self.populate_floor_list()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to remove floor: {str(e)}")
            return

    def find_random_free_position(self):
        if not self.selected_floor:
            QMessageBox.warning(self, "Warning", "Please select a floor first")
            return None

        # Get current floor grid
        floor_grid = self.controller.get_floor_grid(self.selected_floor.name)

        # Find all free positions
        free_positions = []
        grid_size = self.grid_canvas.grid_size
        for x in range(grid_size):
            for y in range(grid_size):
                if (x, y) not in floor_grid or floor_grid[(x, y)] is None:
                    free_positions.append((x, y))

        # If no free positions, return None
        if not free_positions:
            QMessageBox.warning(self, "Warning", "No free space available on this floor")
            return None

        # Return a random free position
        import random
        return random.choice(free_positions)

    def add_room(self):
        if not self.selected_floor:
            QMessageBox.warning(self, "Warning", "Please select a floor first")
            return

        position = self.find_random_free_position()
        if position:
            # try:
                element_data = {
                    "type": "room",
                    "floor_id": self.selected_floor.db_id,
                    "position": position,
                    "number": "Nr.",
                    "capacity": 2,  # Default capacity for new rooms
                    "price_per_night": 100  # Default price for new rooms
                }
                self.controller.hotel_service.add_element(element_data)
                # Refresh the grid
                floor_grid = self.controller.get_floor_grid(self.selected_floor.name)
                self.grid_canvas.set_floor_elements(floor_grid)
                QMessageBox.information(self, "Success", f"Room added at position {position}")
            # except Exception as e:
                # QMessageBox.critical(self, "Error", f"Failed to add room: {str(e)}")

    def add_hallway(self):
        if not self.selected_floor:
            QMessageBox.warning(self, "Warning", "Please select a floor first")
            return

        position = self.find_random_free_position()
        if position:
            try:
                element_data = {
                    "type": "hallway",
                    "floor_id": self.selected_floor.db_id,
                    "position": position,
                }
                self.controller.hotel_service.add_element(element_data)
                # Refresh the grid
                floor_grid = self.controller.get_floor_grid(self.selected_floor.name)
                self.grid_canvas.set_floor_elements(floor_grid)
                QMessageBox.information(self, "Success", f"Hallway added at position {position}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add hallway: {str(e)}")

    def add_staircase(self):
        """Add a staircase at a random free position"""
        if not self.selected_floor:
            QMessageBox.warning(self, "Warning", "Please select a floor first")
            return

        position = self.find_random_free_position()
        if position:
            try:
                element_data = {
                    "type": "staircase",
                    "floor_id": self.selected_floor.db_id,
                    "position": position,
                }
                self.controller.hotel_service.add_element(element_data)
                # Refresh the grid
                floor_grid = self.controller.get_floor_grid(self.selected_floor.name)
                self.grid_canvas.set_floor_elements(floor_grid)
                QMessageBox.information(self, "Success", f"Staircase added at position {position}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add staircase: {str(e)}")

    def confirm_delete_element(self, element_widget):
        """Show confirmation dialog and delete element if confirmed"""

        element_id = element_widget.element_id
        floor_elements = {e.db_id: e for e in self.selected_floor.elements}
        element = floor_elements.get(element_id)

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
                # Delete the element using the controller
                self.controller.hotel_service.remove_element(element)

                # Refresh the grid to show the updated floor
                floor_grid = self.controller.get_floor_grid(self.selected_floor.name)
                self.grid_canvas.set_floor_elements(floor_grid)
                self.grid_canvas.update()

                QMessageBox.information(
                    self,
                    "Success",
                    f"{element_type} successfully deleted!"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to delete {element_type.lower()}: {str(e)}"
                )