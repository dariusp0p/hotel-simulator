from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QColor, QPen



class FloorElementWidget:
    def __init__(self, element_type, position, element_id=None, number=None, capacity=None):
        self.element_type = element_type
        self.position = position
        self.element_id = element_id
        self.number = number
        self.capacity = capacity
        self.selected = False
        self.hovered = False

    def draw(self, painter, cell_size, drag_offset=None):
        if not self.position or not isinstance(self.position, tuple) or len(self.position) != 2:
            print(f"Invalid position for element: {self}")
            return

        # Apply drag offset for the selected element
        if self.selected and drag_offset:
            x = int(self.position[0] * cell_size) + drag_offset.x()
            y = int(self.position[1] * cell_size) + drag_offset.y()
        else:
            x = int(self.position[0] * cell_size)
            y = int(self.position[1] * cell_size)

        if self.element_type == "room":
            background_color = QColor(173, 216, 230)  # Light blue
            text_color = QColor(0, 0, 100)
        elif self.element_type == "staircase":
            background_color = QColor(152, 251, 152)  # Light green
            text_color = QColor(0, 100, 0)
        elif self.element_type == "hallway":
            background_color = QColor(211, 211, 211)  # Light gray
            text_color = QColor(50, 50, 50)
        else:
            background_color = QColor(255, 192, 203)  # Light pink (unknown element)
            text_color = QColor(100, 0, 0)

        if self.selected:
            border_width = 3
            border_color = QColor(255, 140, 0)  # Orange
        else:
            border_width = 1
            border_color = QColor(50, 50, 50)  # Dark gray

        # Draw the element rectangle
        painter.setPen(QPen(border_color, border_width))
        painter.fillRect(x, y, cell_size, cell_size, background_color)
        painter.drawRect(x, y, cell_size, cell_size)

        # Draw text info
        painter.setPen(text_color)
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)

        # Draw element type
        painter.drawText(
            QRectF(x, y, cell_size, cell_size / 2),
            Qt.AlignmentFlag.AlignCenter,
            self.element_type.capitalize()
        )

        # Draw room number or capacity if available
        if self.number:
            painter.drawText(
                QRectF(x, y + cell_size / 2, cell_size, cell_size / 4),
                Qt.AlignmentFlag.AlignCenter,
                f"#{self.number}"
            )

        if self.capacity and self.element_type == "room":
            painter.drawText(
                QRectF(x, y + 3 * cell_size / 4, cell_size, cell_size / 4),
                Qt.AlignmentFlag.AlignCenter,
                f"Cap: {self.capacity}"
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
            print("Element is not hovered.")
            return False

        # Transform the point to the element's local coordinate system
        local_x = (point.x() - offset.x()) / scale_factor - self.position[0] * cell_size
        local_y = (point.y() - offset.y()) / scale_factor - self.position[1] * cell_size

        # Calculate delete button area
        x_btn_size = cell_size / 4
        x_btn_x = cell_size - x_btn_size - 2
        x_btn_y = 2

        # Debugging: Print calculated button area and transformed point
        print(f"Delete button area: ({x_btn_x}, {x_btn_y}, {x_btn_x + x_btn_size}, {x_btn_y + x_btn_size})")
        print(f"Transformed click point: ({local_x}, {local_y})")

        # Check if the transformed point is within the delete button area
        clicked = (x_btn_x <= local_x <= x_btn_x + x_btn_size and
                   x_btn_y <= local_y <= x_btn_y + x_btn_size)

        print(f"Delete button clicked: {clicked}")
        return clicked