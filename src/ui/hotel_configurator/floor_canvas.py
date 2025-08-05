from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGraphicsScene,
    QGraphicsView,
    QPushButton,
    QGraphicsRectItem,
    QGraphicsSimpleTextItem,
    QGraphicsItem,
    QGraphicsProxyWidget,
    QDialog,
    QLabel,
    QLineEdit,
)
from PyQt6.QtGui import QFont, QBrush, QColor
from PyQt6.QtCore import QPointF


def safe_get(data, key, default=None):
    if isinstance(data, dict):
        return data.get(key, default)
    return getattr(data, key, default)


class ElementItem(QGraphicsRectItem):
    def __init__(self, element_data, on_edit=None, on_delete=None):
        super().__init__(0, 0, 100, 60)
        self.setBrush(QBrush(QColor("#e0e0e0")))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setZValue(1)

        self.element_data = element_data
        self.on_edit = on_edit
        self.on_delete = on_delete

        self.label = QGraphicsSimpleTextItem(self)
        self.label.setFont(QFont("Arial", 10))
        self.label.setPos(5, 5)
        self.update_label()

        if safe_get(self.element_data, "element_type") == "room":
            self.edit_btn = QPushButton("✎")
            self.edit_btn.setFixedSize(20, 20)
            self.edit_btn.clicked.connect(self.handle_edit)
            self.proxy_edit = QGraphicsProxyWidget(self)
            self.proxy_edit.setWidget(self.edit_btn)
            self.proxy_edit.setPos(5, 35)
        else:
            self.proxy_edit = None

        self.delete_btn = QPushButton("✕")
        self.delete_btn.setFixedSize(20, 20)
        self.delete_btn.setStyleSheet("color: red;")
        self.delete_btn.clicked.connect(self.handle_delete)
        self.proxy_delete = QGraphicsProxyWidget(self)
        self.proxy_delete.setWidget(self.delete_btn)
        self.proxy_delete.setPos(75, 5)

    def update_label(self):
        name = safe_get(
            self.element_data, "name", safe_get(self.element_data, "element_id", "")
        )
        cap = safe_get(self.element_data, "capacity", 0)
        self.label.setText(f"{name}\nCap: {cap}")

    def handle_edit(self):
        if self.on_edit:
            self.on_edit(self)

    def handle_delete(self):
        if self.on_delete:
            self.on_delete(self)


class ElementEditDialog(QDialog):
    def __init__(self, name, capacity):
        super().__init__()
        self.setWindowTitle("Edit Room")
        self.setFixedSize(250, 120)

        layout = QVBoxLayout()
        self.name_input = QLineEdit(name)
        self.cap_input = QLineEdit(str(capacity))

        layout.addWidget(QLabel("Name"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Capacity"))
        layout.addWidget(self.cap_input)

        btn = QPushButton("Save")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)
        self.setLayout(layout)

    def get_data(self):
        return self.name_input.text().strip(), int(self.cap_input.text().strip())


class FloorCanvas(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)

        self.elements = []

    def load_elements(self, element_list):
        self.scene.clear()
        self.elements.clear()
        for el in element_list:
            item = ElementItem(
                element_data=el,
                on_edit=self.edit_element,
                on_delete=self.remove_element,
            )
            x, y = safe_get(el, "position", (0, 0))
            item.setPos(x, y)
            self.scene.addItem(item)
            self.elements.append(item)

    def add_element(self, element_data):
        item = ElementItem(
            element_data=element_data,
            on_edit=self.edit_element,
            on_delete=self.remove_element,
        )
        item.setPos(50, 50)
        self.scene.addItem(item)
        self.elements.append(item)

    def remove_element(self, item):
        self.scene.removeItem(item)
        self.elements.remove(item)

    def edit_element(self, item):
        data = item.element_data
        name = safe_get(data, "name", safe_get(data, "element_id", ""))
        cap = safe_get(data, "capacity", 0)

        dialog = ElementEditDialog(name, cap)
        if dialog.exec():
            name, cap = dialog.get_data()
            if hasattr(data, "__dict__"):
                data.name = name
                data.capacity = cap
            elif isinstance(data, dict):
                data["name"] = name
                data["capacity"] = cap
            item.update_label()
