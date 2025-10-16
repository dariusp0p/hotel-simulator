from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QCursor, QTransform, QBrush, QFont
from PyQt6.QtCore import Qt, QPoint


class SimulatorCanvas(QWidget):
    """Canvas for rendering the hotel layout and handling interactions."""
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(245, 245, 245))
        self.setPalette(palette)

        self.cellSize = 70
        self.gridSize = 10
        self.floorSpacing = 50
        self.floorsPerRow = 2

        self.scaleFactor = 1.0
        self.offset = QPoint(0, 0)
        self.isPanning = False
        self.lastMousePos = QPoint(0, 0)

        self.currentDate = None
        self.availableRooms = set()
        self.unavailableRooms = set()

        self.setMouseTracking(True)
        self.firstPaint = True

    def showEvent(self, event):
        super().showEvent(event)
        self.centerView()

    def resizeEvent(self, event):
        if hasattr(self, 'firstPaint') and self.firstPaint:
            self.centerView()
        super().resizeEvent(event)

    def centerView(self):
        totalWidth, totalHeight = self.calculateDrawingSize()

        centerX = (self.width() - totalWidth * self.scaleFactor) / 2
        centerY = (self.height() - totalHeight * self.scaleFactor) / 2

        self.offset = QPoint(int(centerX), int(centerY))
        self.update()

    def calculateDrawingSize(self):
        floors = self.controller.get_all_floors()
        if not floors:
            return self.floorSpacing * 2, self.floorSpacing * 2

        floors = sorted(floors, key=lambda f: f.level)

        maxWidth = 0
        totalHeight = self.floorSpacing * 2

        currentRowWidth = self.floorSpacing
        maxHeightInRow = 0
        colCount = 0

        for floor in floors:
            floorGrid = self.controller.get_floor_grid(floor.db_id)
            positions = [pos for pos, element in floorGrid.items() if element and pos]

            if not positions:
                continue

            minX = min([pos[0] for pos in positions]) if positions else 0
            minY = min([pos[1] for pos in positions]) if positions else 0
            maxX = max([pos[0] for pos in positions]) if positions else 0
            maxY = max([pos[1] for pos in positions]) if positions else 0

            actualWidth = (maxX - minX + 1) * self.cellSize
            actualHeight = (maxY - minY + 1) * self.cellSize

            if colCount >= self.floorsPerRow:
                maxWidth = max(maxWidth, currentRowWidth)
                currentRowWidth = self.floorSpacing
                totalHeight += maxHeightInRow + self.floorSpacing
                maxHeightInRow = 0
                colCount = 0

            currentRowWidth += actualWidth + self.floorSpacing
            maxHeightInRow = max(maxHeightInRow, actualHeight)
            colCount += 1

        totalHeight += maxHeightInRow + self.floorSpacing
        maxWidth = max(maxWidth, currentRowWidth)

        return maxWidth, totalHeight

    def wheelEvent(self, event):
        mousePos = event.position().toPoint()
        oldScaleFactor = self.scaleFactor

        deltaY = event.angleDelta().y()
        if deltaY == 0:
            return

        zoomPerStep = 1.05
        steps = deltaY / 120.0
        factor = pow(zoomPerStep, steps)

        self.scaleFactor *= factor
        self.scaleFactor = max(0.2, min(self.scaleFactor, 3.0))

        scenePoint = (mousePos - self.offset) / oldScaleFactor

        self.offset = mousePos - scenePoint * self.scaleFactor

        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.isPanning = True
            self.lastMousePos = event.position().toPoint()
            self.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.isPanning:
            self.isPanning = False
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def mouseMoveEvent(self, event):
        if self.isPanning:
            delta = (event.position().toPoint() - self.lastMousePos)
            self.offset += delta
            self.lastMousePos = event.position().toPoint()
            self.update()

    def mapToScene(self, point):
        return (point - self.offset) / self.scaleFactor

    def updateRoomAvailability(self, date):
        self.currentDate = date
        dateString = date.toString("yyyy-MM-dd")
        self.availableRooms, self.unavailableRooms = self.controller.get_rooms_availability_for_date(dateString)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(self.rect(), QColor(245, 245, 245))

        transform = QTransform()
        transform.translate(self.offset.x(), self.offset.y())
        transform.scale(self.scaleFactor, self.scaleFactor)
        painter.setTransform(transform)

        floors = self.controller.get_all_floors()
        floors = sorted(floors, key=lambda f: f.level)

        currentX = self.floorSpacing
        currentY = self.floorSpacing * 2
        maxHeightInRow = 0
        colCount = 0

        for i, floor in enumerate(floors):
            floorGrid = self.controller.get_floor_grid(floor.db_id)

            positions = [pos for pos, element in floorGrid.items() if element and pos]

            if not positions:
                continue

            minX = min([pos[0] for pos in positions])
            minY = min([pos[1] for pos in positions])
            maxX = max([pos[0] for pos in positions])
            maxY = max([pos[1] for pos in positions])

            actualWidth = (maxX - minX + 1) * self.cellSize
            actualHeight = (maxY - minY + 1) * self.cellSize

            if colCount >= self.floorsPerRow:
                currentX = self.floorSpacing
                currentY += maxHeightInRow + self.floorSpacing
                maxHeightInRow = 0
                colCount = 0

            painter.setPen(QColor(0, 0, 0))
            titleFont = painter.font()
            titleFont.setPointSize(14)
            titleFont.setBold(True)
            painter.setFont(titleFont)

            titleY = currentY - 25
            painter.drawText(
                int(currentX),
                int(titleY),
                f"{floor.name} (Level: {floor.level})"
            )

            defaultFont = QFont()
            painter.setFont(defaultFont)

            for pos, element in floorGrid.items():
                if element and pos:
                    adjustedX = currentX + (pos[0] - minX) * self.cellSize
                    adjustedY = currentY + (pos[1] - minY) * self.cellSize

                    if element.type == "room":
                        if hasattr(self, 'currentDate') and self.currentDate:
                            if element.db_id in self.availableRooms:
                                painter.fillRect(adjustedX, adjustedY, self.cellSize, self.cellSize,
                                                 QColor(150, 230, 150))  # Green for available
                            elif element.db_id in self.unavailableRooms:
                                painter.fillRect(adjustedX, adjustedY, self.cellSize, self.cellSize,
                                                 QColor(230, 150, 150))  # Red for unavailable
                            else:
                                painter.fillRect(adjustedX, adjustedY, self.cellSize, self.cellSize,
                                                 QColor(200, 230, 255))  # Default blue
                        else:
                            painter.fillRect(adjustedX, adjustedY, self.cellSize, self.cellSize,
                                             QColor(200, 230, 255))
                    elif element.type == "hallway":
                        painter.fillRect(adjustedX, adjustedY, self.cellSize, self.cellSize,
                                         QColor(220, 220, 220))
                    elif element.type == "staircase":
                        painter.fillRect(adjustedX, adjustedY, self.cellSize, self.cellSize,
                                         QColor(150, 150, 150))

                        painter.setPen(QPen(QColor(80, 80, 80), 2))
                        stepWidth = self.cellSize / 6
                        for j in range(5):
                            yPos = adjustedY + j * stepWidth + stepWidth
                            painter.drawLine(
                                int(adjustedX + stepWidth),
                                int(yPos),
                                int(adjustedX + self.cellSize - stepWidth),
                                int(yPos)
                            )

                    painter.setPen(QPen(QColor(100, 100, 100), 1))
                    painter.drawRect(adjustedX, adjustedY, self.cellSize, self.cellSize)

                    if element.type == "room":
                        painter.setPen(QColor(0, 0, 0))
                        roomNumber = getattr(element, 'number', '?')
                        capacity = getattr(element, 'capacity', '?')
                        price = getattr(element, 'price_per_night', '?')

                        currentFont = painter.font()

                        boldFont = QFont(currentFont)
                        boldFont.setBold(True)

                        painter.setFont(boldFont)
                        painter.drawText(adjustedX + 5, adjustedY + 20, f"Room {roomNumber}")
                        painter.setFont(currentFont)

                        painter.drawText(adjustedX + 5, adjustedY + 40, f"{capacity} Beds")
                        painter.drawText(adjustedX + 5, adjustedY + 60, f"${price}")

            currentX += actualWidth + self.floorSpacing
            maxHeightInRow = max(maxHeightInRow, actualHeight)
            colCount += 1

        if hasattr(self, 'firstPaint') and self.firstPaint:
            self.firstPaint = False
