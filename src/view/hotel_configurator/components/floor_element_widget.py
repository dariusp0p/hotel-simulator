from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QColor, QPen, QFont


class FloorElementWidget:
    """Widget representing a floor element (room, staircase, hallway) in the hotel configurator."""
    def __init__(self, elementType, position, elementId=None, number=None, capacity=None, pricePerNight=None):
        self.elementType = elementType
        self.position = position
        self.elementId = elementId
        self.number = number
        self.capacity = capacity
        self.pricePerNight = pricePerNight

        self.selected = False
        self.hovered = False

    def drawBackground(self, painter, cellSize, pos=None):
        if not self.position or not isinstance(self.position, tuple) or len(self.position) != 2:
            print(f"Invalid position for element: {self}")
            return

        if pos is not None:
            x = int(pos.x() - cellSize / 2)
            y = int(pos.y() - cellSize / 2)
        else:
            x = int(self.position[0] * cellSize)
            y = int(self.position[1] * cellSize)

        if self.elementType == "room":
            backgroundColor = QColor(173, 216, 230)  # Light blue
        elif self.elementType == "staircase":
            backgroundColor = QColor(255, 249, 196)  # Light yellow
        elif self.elementType == "hallway":
            backgroundColor = QColor(211, 211, 211)  # Light gray
        else:
            backgroundColor = QColor(255, 192, 203)  # Light pink (unknown element)

        if self.selected:
            borderWidth = 3
            borderColor = QColor(255, 0, 0)  # Red
        else:
            borderWidth = 1
            borderColor = QColor(50, 50, 50)  # Dark gray

        painter.setPen(QPen(borderColor, borderWidth))
        painter.fillRect(x, y, cellSize, cellSize, backgroundColor)
        painter.drawRect(x, y, cellSize, cellSize)

    def drawText(self, painter, cellSize, pos=None):
        if not self.position or not isinstance(self.position, tuple) or len(self.position) != 2:
            print(f"Invalid position for element: {self}")
            return

        if pos is not None:
            x = int(pos.x() - cellSize / 2)
            y = int(pos.y() - cellSize / 2)
        else:
            x = int(self.position[0] * cellSize)
            y = int(self.position[1] * cellSize)

        if self.elementType == "room":
            textColor = QColor(0, 0, 100)
        elif self.elementType == "staircase":
            textColor = QColor(120, 90, 0)
        elif self.elementType == "hallway":
            textColor = QColor(50, 50, 50)
        else:
            textColor = QColor(100, 0, 0)

        painter.setPen(textColor)
        font = QFont("Arial", 10)
        font.setBold(True)
        painter.setFont(font)

        if self.elementType == "room":
            painter.drawText(
                QRectF(x, y, cellSize, cellSize / 2),
                Qt.AlignmentFlag.AlignCenter,
                self.elementType.capitalize() + f" {self.number}"
            )
            painter.drawText(
                QRectF(x, y + 2 * cellSize / 4, cellSize, cellSize / 4),
                Qt.AlignmentFlag.AlignCenter,
                f"Cap: {self.capacity}"
            )
            painter.drawText(
                QRectF(x, y + 3 * cellSize / 4, cellSize, cellSize / 4),
                Qt.AlignmentFlag.AlignCenter,
                f"Price: {self.pricePerNight}"
            )
        else:
            painter.drawText(
                QRectF(x, y, cellSize, cellSize),
                Qt.AlignmentFlag.AlignCenter,
                self.elementType.capitalize()
            )

        if self.hovered:
            xBtnSize = cellSize / 4
            xBtnX = int(self.position[0] * cellSize + cellSize - xBtnSize - 2)
            xBtnY = int(self.position[1] * cellSize + 2)

            painter.setPen(QPen(QColor(0, 0, 0), 2))
            margin = 4
            painter.drawLine(
                QPointF(xBtnX + margin, xBtnY + margin),
                QPointF(xBtnX + xBtnSize - margin, xBtnY + xBtnSize - margin)
            )
            painter.drawLine(
                QPointF(xBtnX + xBtnSize - margin, xBtnY + margin),
                QPointF(xBtnX + margin, xBtnY + xBtnSize - margin)
            )

    def isDeleteButtonClicked(self, point, cellSize, offset, scaleFactor):
        if not self.hovered:
            return False

        localX = (point.x() - offset.x()) / scaleFactor - self.position[0] * cellSize
        localY = (point.y() - offset.y()) / scaleFactor - self.position[1] * cellSize

        xBtnSize = cellSize / 4
        xBtnX = cellSize - xBtnSize - 2
        xBtnY = 2

        clicked = (xBtnX <= localX <= xBtnX + xBtnSize and
                   xBtnY <= localY <= xBtnY + xBtnSize)
        return clicked
