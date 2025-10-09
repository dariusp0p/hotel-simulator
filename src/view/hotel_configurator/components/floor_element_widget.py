from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QColor, QPen, QFont


class FloorElementWidget:
    def __init__(self, element_type, position, element_id=None, number=None, capacity=None, price_per_night=None):
        self.element_type = element_type
        self.position = position
        self.element_id = element_id
        self.number = number
        self.capacity = capacity
        self.price_per_night = price_per_night

        self.selected = False
        self.hovered = False


    def draw_background(self, painter, cell_size, pos=None):
        if not self.position or not isinstance(self.position, tuple) or len(self.position) != 2:
            print(f"Invalid position for element: {self}")
            return

        if pos is not None:
            x = int(pos.x() - cell_size / 2)
            y = int(pos.y() - cell_size / 2)
        else:
            x = int(self.position[0] * cell_size)
            y = int(self.position[1] * cell_size)

        if self.element_type == "room":
            background_color = QColor(173, 216, 230)  # Light blue
        elif self.element_type == "staircase":
            background_color = QColor(255, 249, 196)  # Light yellow
        elif self.element_type == "hallway":
            background_color = QColor(211, 211, 211)  # Light gray
        else:
            background_color = QColor(255, 192, 203)  # Light pink (unknown element)

        if self.selected:
            border_width = 3
            border_color = QColor(255, 0, 0)  # Red
        else:
            border_width = 1
            border_color = QColor(50, 50, 50)  # Dark gray

        # Draw the element rectangle
        painter.setPen(QPen(border_color, border_width))
        painter.fillRect(x, y, cell_size, cell_size, background_color)
        painter.drawRect(x, y, cell_size, cell_size)


    def draw_text(self, painter, cell_size, pos=None):
        if not self.position or not isinstance(self.position, tuple) or len(self.position) != 2:
            print(f"Invalid position for element: {self}")
            return

        if pos is not None:
            x = int(pos.x() - cell_size / 2)
            y = int(pos.y() - cell_size / 2)
        else:
            x = int(self.position[0] * cell_size)
            y = int(self.position[1] * cell_size)

        if self.element_type == "room":
            text_color = QColor(0, 0, 100)
        elif self.element_type == "staircase":
            text_color = QColor(120, 90, 0)
        elif self.element_type == "hallway":
            text_color = QColor(50, 50, 50)
        else:
            text_color = QColor(100, 0, 0)

        painter.setPen(text_color)
        font = QFont("Arial", 10)
        font.setBold(True)
        painter.setFont(font)

        # Draw element type
        if self.element_type == "room":
            painter.drawText(
                QRectF(x, y, cell_size, cell_size / 2),
                Qt.AlignmentFlag.AlignCenter,
                self.element_type.capitalize() + f" {self.number}"
            )
            painter.drawText(
                QRectF(x, y + 2 * cell_size / 4, cell_size, cell_size / 4),
                Qt.AlignmentFlag.AlignCenter,
                f"Cap: {self.capacity}"
            )
            painter.drawText(
                QRectF(x, y + 3 * cell_size / 4, cell_size, cell_size / 4),
                Qt.AlignmentFlag.AlignCenter,
                f"Price: {self.price_per_night}"
            )
        else:
            painter.drawText(
                QRectF(x, y, cell_size, cell_size),
                Qt.AlignmentFlag.AlignCenter,
                self.element_type.capitalize()
            )

        # Draw X button when hovered
        if self.hovered:
            x_btn_size = cell_size / 4
            x_btn_x = int(self.position[0] * cell_size + cell_size - x_btn_size - 2)
            x_btn_y = int(self.position[1] * cell_size + 2)

            # X symbol
            painter.setPen(QPen(QColor(0, 0, 0), 2))
            margin = 4
            painter.drawLine(
                QPointF(x_btn_x + margin, x_btn_y + margin),
                QPointF(x_btn_x + x_btn_size - margin, x_btn_y + x_btn_size - margin)
            )
            painter.drawLine(
                QPointF(x_btn_x + x_btn_size - margin, x_btn_y + margin),
                QPointF(x_btn_x + margin, x_btn_y + x_btn_size - margin)
            )


    def is_delete_button_clicked(self, point, cell_size, offset, scale_factor):
        if not self.hovered:
            return False

        local_x = (point.x() - offset.x()) / scale_factor - self.position[0] * cell_size
        local_y = (point.y() - offset.y()) / scale_factor - self.position[1] * cell_size

        x_btn_size = cell_size / 4
        x_btn_x = cell_size - x_btn_size - 2
        x_btn_y = 2

        clicked = (x_btn_x <= local_x <= x_btn_x + x_btn_size and
                   x_btn_y <= local_y <= x_btn_y + x_btn_size)

        return clicked