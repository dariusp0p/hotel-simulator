from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QLineEdit, QListWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

from src.view.hotel_configurator.components.floor_list_widget import FloorListWidget



class SideBar(QWidget):
    def __init__(self, controller, on_floor_selected, on_floors_reordered, on_add_floor, on_remove_floor,
                 on_update_floor_name, on_update_room, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.on_floor_selected = on_floor_selected
        self.on_floors_reordered = on_floors_reordered
        self.on_add_floor = on_add_floor
        self.on_remove_floor = on_remove_floor
        self.on_update_floor_name = on_update_floor_name
        self.on_update_room = on_update_room

        self.setup_ui()


    def setup_ui(self):
        self.setFixedWidth(250)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(60, 60, 60))
        self.setPalette(palette)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)


        # Upper section (Floors)
        upper_section = QWidget()
        upper_layout = QVBoxLayout(upper_section)
        upper_layout.setContentsMargins(0, 0, 0, 0)
        upper_layout.setSpacing(5)

        floors_title = QLabel("Floors")
        floors_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        floors_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        floors_title.setStyleSheet("color: white;")

        floors_separator = QFrame()
        floors_separator.setFrameShape(QFrame.Shape.HLine)
        floors_separator.setFrameShadow(QFrame.Shadow.Sunken)
        floors_separator.setStyleSheet("background-color: #777;")

        self.floor_list = FloorListWidget()
        self.floor_list.itemClicked.connect(self.on_floor_selected)
        self.floor_list.floorsReordered.connect(self.on_floors_reordered)

        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 5, 0, 0)
        buttons_layout.setSpacing(10)

        add_floor_btn = QPushButton("Add")
        add_floor_btn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        add_floor_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_floor_btn.clicked.connect(self.on_add_floor)

        remove_floor_btn = QPushButton("Remove")
        remove_floor_btn.setStyleSheet(
            "QPushButton {background-color: #a94a4a; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #b95a5a;}"
        )
        remove_floor_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_floor_btn.clicked.connect(self.on_remove_floor)

        buttons_layout.addWidget(add_floor_btn)
        buttons_layout.addWidget(remove_floor_btn)

        upper_layout.addWidget(floors_title)
        upper_layout.addWidget(floors_separator)
        upper_layout.addWidget(self.floor_list, 1)
        upper_layout.addWidget(buttons_container)


        # Lower section (Selected Floor + Selected Room)
        lower_section = QWidget()
        lower_layout = QVBoxLayout(lower_section)
        lower_layout.setContentsMargins(0, 0, 0, 0)
        lower_layout.setSpacing(5)

        # Selected Floor Section
        selected_floor_title = QLabel("Selected Floor")
        selected_floor_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        selected_floor_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        selected_floor_title.setStyleSheet("color: white;")

        selected_floor_separator = QFrame()
        selected_floor_separator.setFrameShape(QFrame.Shape.HLine)
        selected_floor_separator.setFrameShadow(QFrame.Shadow.Sunken)
        selected_floor_separator.setStyleSheet("background-color: #777;")

        self.selected_floor_panel = QWidget()
        self.selected_floor_panel.setStyleSheet("background-color: #555;")
        selected_floor_layout = QVBoxLayout(self.selected_floor_panel)

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

        lower_layout.addWidget(selected_floor_title)
        lower_layout.addWidget(selected_floor_separator)
        lower_layout.addWidget(self.selected_floor_panel, 1)

        # Selected Room Section
        selected_room_title = QLabel("Selected Room")
        selected_room_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        selected_room_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        selected_room_title.setStyleSheet("color: white;")

        selected_room_separator = QFrame()
        selected_room_separator.setFrameShape(QFrame.Shape.HLine)
        selected_room_separator.setFrameShadow(QFrame.Shadow.Sunken)
        selected_room_separator.setStyleSheet("background-color: #777;")

        self.selected_room_panel = QWidget()
        self.selected_room_panel.setStyleSheet("background-color: #555;")
        selected_room_layout = QVBoxLayout(self.selected_room_panel)

        room_number_container = QWidget()
        room_number_layout = QHBoxLayout(room_number_container)
        room_number_layout.setContentsMargins(0, 0, 0, 0)

        self.room_number_edit = QLineEdit()
        self.room_number_edit.setStyleSheet(
            "background-color: #444; color: white; border: 1px solid #666; padding: 5px;")
        self.room_number_edit.setPlaceholderText("Room number")

        room_number_layout.addWidget(QLabel("Number:"))
        room_number_layout.addWidget(self.room_number_edit)

        room_capacity_container = QWidget()
        room_capacity_layout = QHBoxLayout(room_capacity_container)
        room_capacity_layout.setContentsMargins(0, 0, 0, 0)

        self.room_capacity_edit = QLineEdit()
        self.room_capacity_edit.setStyleSheet(
            "background-color: #444; color: white; border: 1px solid #666; padding: 5px;")
        self.room_capacity_edit.setPlaceholderText("Capacity")

        room_capacity_layout.addWidget(QLabel("Capacity:"))
        room_capacity_layout.addWidget(self.room_capacity_edit)

        room_price_container = QWidget()
        room_price_layout = QHBoxLayout(room_price_container)
        room_price_layout.setContentsMargins(0, 0, 0, 0)

        self.room_price_edit = QLineEdit()
        self.room_price_edit.setStyleSheet(
            "background-color: #444; color: white; border: 1px solid #666; padding: 5px;")
        self.room_price_edit.setPlaceholderText("Price per night")

        room_price_layout.addWidget(QLabel("Price:"))
        room_price_layout.addWidget(self.room_price_edit)

        update_room_btn = QPushButton("Update")
        update_room_btn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; padding: 5px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        update_room_btn.clicked.connect(self.on_update_room)

        selected_room_layout.addWidget(room_number_container)
        selected_room_layout.addWidget(room_capacity_container)
        selected_room_layout.addWidget(room_price_container)
        selected_room_layout.addWidget(update_room_btn)

        lower_layout.addWidget(selected_room_title)
        lower_layout.addWidget(selected_room_separator)
        lower_layout.addWidget(self.selected_room_panel, 1)


        # Add sections to main layout
        main_layout.addWidget(upper_section, 1)
        main_layout.addWidget(lower_section, 1)

        self.populate_floor_list()


    def populate_floor_list(self):
        self.floor_list.clear()
        floors = self.controller.get_all_floors()
        for floor in floors:
            item = QListWidgetItem(floor.name)
            item.setData(Qt.ItemDataRole.UserRole, floor)
            self.floor_list.addItem(item)

    def display_room_details(self, room):
        if room:
            self.room_number_edit.setText(str(room.number))
            self.room_capacity_edit.setText(str(room.capacity))
            self.room_price_edit.setText(str(room.price_per_night))
        else:
            self.room_number_edit.clear()
            self.room_capacity_edit.clear()
            self.room_price_edit.clear()
