from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QLabel,
    QLineEdit,
    QGraphicsView,
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


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

        # =========================
        # Sidebar (Stânga)
        # =========================
        # Sidebar (Stânga)
        self.sidebar_layout = QVBoxLayout()

        # Top bar cu ← Back
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

        # Titlu Floors
        self.floor_label = QLabel("Floors")
        self.floor_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.floor_label.setStyleSheet("background-color: transparent;")
        self.sidebar_layout.addWidget(self.floor_label)

        # Listă etaje
        self.floor_list = QListWidget()
        self.floor_list.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.floor_list.setMaximumHeight(300)  # se oprește pe la jumate
        self.sidebar_layout.addWidget(self.floor_list)
        self.floor_list.setStyleSheet(
            """
            QListWidget::item {
                font-size: 14px;
                border: 1px solid #999;
                margin: 4px;
                padding: 6px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #444;
                color: white;
            }
        """
        )
        self.load_floors()

        # Butoane Add / Edit / Remove
        self.floor_buttons_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.edit_btn = QPushButton("Edit")
        self.remove_btn = QPushButton("Remove")

        for btn in [self.add_btn, self.edit_btn, self.remove_btn]:
            self.floor_buttons_layout.addWidget(btn)

        self.sidebar_layout.addLayout(self.floor_buttons_layout)

        # Spacer jos
        self.sidebar_layout.addStretch()

        # Conectare
        self.add_btn.clicked.connect(self.handle_add_floor)
        self.edit_btn.clicked.connect(self.handle_edit_floor)
        self.remove_btn.clicked.connect(self.handle_remove_floor)

        # =========================
        # Zona Centrală (Dreapta)
        # =========================
        self.central_layout = QVBoxLayout()

        self.canvas_view = QGraphicsView()
        self.hotbar_layout = QHBoxLayout()

        self.room_btn = QPushButton("Room")
        self.hallway_btn = QPushButton("Hallway")
        self.staircase_btn = QPushButton("Staircase")

        for btn in [self.hallway_btn, self.room_btn, self.staircase_btn]:
            self.hotbar_layout.addWidget(btn)

        self.central_layout.addWidget(self.canvas_view)
        self.central_layout.addLayout(self.hotbar_layout)

        # =========================
        # Combinare finală
        # =========================
        self.main_layout.addLayout(self.sidebar_layout, 1)
        self.main_layout.addLayout(self.central_layout, 3)

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

    def load_floors(self):
        self.floor_list.clear()
        try:
            floors = self.controller.get_floors()

            def extract_sort_key(name):
                name = name.lower()
                if name == "ground floor":
                    return 0
                if "floor" in name:
                    try:
                        return -int(name.split("floor")[1].strip())
                    except:
                        return -999
                if "basement" in name:
                    try:
                        return 100 + int(name.split("basement")[1].strip())
                    except:
                        return 999
                return 999

            sorted_names = sorted(floors, key=extract_sort_key)

            for floor_name in sorted_names:
                self.floor_list.addItem(floor_name)

        except Exception as e:
            print("Error loading floors:", e)


def handle_remove_floor(self):
    current_item = self.floor_list.currentItem()
    if not current_item:
        return

    floor_name = current_item.text()
    try:
        self.controller.remove_floor(floor_name)
        self.floor_list.takeItem(self.floor_list.row(current_item))
    except Exception as e:
        print("Error:", e)


def handle_edit_floor(self):
    current_item = self.floor_list.currentItem()
    if not current_item:
        return  # nimic selectat

    old_name = current_item.text()

    # Deschide un dialog pentru a introduce un nume nou
    dialog = EditFloorDialog(old_name, self)
    if dialog.exec():
        new_name = dialog.get_new_name()
        if new_name and new_name != old_name:
            try:
                self.controller.rename_floor(old_name, new_name)
                current_item.setText(new_name)
            except Exception as e:
                print("Error:", e)
