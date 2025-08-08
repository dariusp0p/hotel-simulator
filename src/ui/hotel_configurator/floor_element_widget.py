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

    def draw(self, painter, cell_size):
        x = self.position[0] * cell_size
        y = self.position[1] * cell_size

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
            x_btn_x = self.position[0] * cell_size + cell_size - x_btn_size - 2
            x_btn_y = self.position[1] * cell_size + 2

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

    def is_delete_button_clicked(self, point, cell_size):
        if not self.hovered:
            print("Element is not hovered.")
            return False

        # Calculate delete button area
        x_btn_size = cell_size / 4
        x_btn_x = self.position[0] * cell_size + cell_size - x_btn_size - 2
        x_btn_y = self.position[1] * cell_size + 2

        # Debugging: Print calculated button area and point
        print(f"Delete button area: ({x_btn_x}, {x_btn_y}, {x_btn_x + x_btn_size}, {x_btn_y + x_btn_size})")
        print(f"Mouse click point: ({point.x()}, {point.y()})")

        # Check if the point is within the delete button area
        clicked = (x_btn_x <= point.x() <= x_btn_x + x_btn_size and
                   x_btn_y <= point.y() <= x_btn_y + x_btn_size)

        print(f"Delete button clicked: {clicked}")
        return clicked