from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QLabel,
    QLineEdit,
    QDialog,
    QSizePolicy,
    QSpacerItem,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from prototypes.floor_canvas import FloorCanvas


class AddFloorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Floor")
        self.setFixedSize(300, 120)

        layout = QVBoxLayout()
        self.label = QLabel("Name")
        self.name_input = QLineEdit()
        self.add_btn = QPushButton("Add Floor")
        self.add_btn.clicked.connect(self.accept)

        layout.addWidget(self.label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.add_btn)
        self.setLayout(layout)

    def get_name(self):
        return self.name_input.text().strip()


class EditFloorDialog(QDialog):
    def __init__(self, current_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Floor")
        self.setFixedSize(300, 120)

        layout = QVBoxLayout()
        self.label = QLabel("Name")
        self.name_input = QLineEdit()
        self.name_input.setText(current_name)
        self.edit_btn = QPushButton("Edit Floor")
        self.edit_btn.clicked.connect(self.accept)

        layout.addWidget(self.label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.edit_btn)
        self.setLayout(layout)

    def get_new_name(self):
        return self.name_input.text().strip()


class HotelConfiguratorPage(QWidget):
    def __init__(self, on_back=None, controller=None):
        super().__init__()
        self.controller = controller.hotel_service
        self.on_back = on_back

        self.setStyleSheet("background-color: #bfbfbf;")

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # Sidebar
        self.sidebar_layout = QVBoxLayout()
        self.top_bar = QHBoxLayout()
        self.back_btn = QPushButton("← Back")
        self.back_btn.setFixedHeight(40)
        self.back_btn.setStyleSheet(
            "padding: 6px; font-weight: bold; background-color: #444; color: white;"
        )
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.clicked.connect(self.handle_back_click)
        self.top_bar.addWidget(self.back_btn)
        self.top_bar.addStretch()
        self.sidebar_layout.addLayout(self.top_bar)

        self.sidebar_layout.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        )
        self.floor_label = QLabel("Floors")
        self.floor_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.sidebar_layout.addWidget(self.floor_label)

        self.floor_list = QListWidget()
        self.floor_list.setMaximumHeight(300)
        self.sidebar_layout.addWidget(self.floor_list)

        self.floor_buttons_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.edit_btn = QPushButton("Edit")
        self.remove_btn = QPushButton("Remove")
        for btn in [self.add_btn, self.edit_btn, self.remove_btn]:
            self.floor_buttons_layout.addWidget(btn)
        self.sidebar_layout.addLayout(self.floor_buttons_layout)
        self.sidebar_layout.addStretch()

        self.add_btn.clicked.connect(self.handle_add_floor)
        self.edit_btn.clicked.connect(self.handle_edit_floor)
        self.remove_btn.clicked.connect(self.handle_remove_floor)
        self.floor_list.currentItemChanged.connect(self.handle_floor_selection_changed)

        # Canvas
        self.central_layout = QVBoxLayout()
        self.canvas = FloorCanvas()
        self.hotbar_layout = QHBoxLayout()

        self.room_btn = QPushButton("Room")
        self.hallway_btn = QPushButton("Hallway")
        self.staircase_btn = QPushButton("Staircase")

        for btn in [self.room_btn, self.hallway_btn, self.staircase_btn]:
            self.hotbar_layout.addWidget(btn)

        self.central_layout.addWidget(self.canvas)
        self.central_layout.addLayout(self.hotbar_layout)

        self.room_btn.clicked.connect(lambda: self.handle_add_element("room"))
        self.hallway_btn.clicked.connect(lambda: self.handle_add_element("hallway"))
        self.staircase_btn.clicked.connect(lambda: self.handle_add_element("staircase"))

        self.main_layout.addLayout(self.sidebar_layout, 1)
        self.main_layout.addLayout(self.central_layout, 3)

        self.load_floors()

    def handle_add_floor(self):
        dialog = AddFloorDialog(self)
        if dialog.exec():
            name = dialog.get_name()
            if name:
                try:
                    self.controller.add_floor(name)
                    self.floor_list.addItem(name)
                except Exception as e:
                    print("Error:", e)

    def handle_edit_floor(self):
        current_item = self.floor_list.currentItem()
        if not current_item:
            return

        old_name = current_item.text()
        dialog = EditFloorDialog(old_name, self)
        if dialog.exec():
            new_name = dialog.get_new_name()
            if new_name and new_name != old_name:
                try:
                    self.controller.rename_floor(old_name, new_name)
                    current_item.setText(new_name)
                except Exception as e:
                    print("Error:", e)

    def handle_remove_floor(self):
        current_item = self.floor_list.currentItem()
        if not current_item:
            return

        name = current_item.text()
        try:
            self.controller.remove_floor(name)
            self.floor_list.takeItem(self.floor_list.currentRow())
        except Exception as e:
            print("Error:", e)

    def handle_back_click(self):
        if self.on_back:
            self.on_back()

    def handle_floor_selection_changed(self):
        current_item = self.floor_list.currentItem()
        if current_item:
            floor_name = current_item.text()
            elements = self.controller.get_floor_grid(floor_name)
            self.canvas.load_elements(elements)

    def handle_add_element(self, element_type):
        current_item = self.floor_list.currentItem()
        if not current_item:
            return

        floor_name = current_item.text()
        floor_id = self.controller.get_floor_id(floor_name)

        element_data = {
            "element_type": element_type,
            "floor_id": floor_id,
            "floor_name": floor_name,
            "name": f"{element_type.capitalize()} X",
            "capacity": 0 if element_type != "room" else 2,
            "position": (50, 50),
        }

        self.controller.add_element(element_data)
        self.handle_floor_selection_changed()  # <-- UI refresh din controller (persistență reală)

    def load_floors(self):
        self.floor_list.clear()
        try:
            floors = self.controller.get_floors()
            for name in sorted(floors):
                self.floor_list.addItem(name)
        except Exception as e:
            print("Error loading floors:", e)
