from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QTransform, QWheelEvent, QColor, QPen

from src.view.hotel_configurator.components.floor_element_widget import FloorElementWidget


class GridCanvas(QWidget):
    """Canvas widget for displaying and interacting with the hotel floor grid."""
    elementDeleteRequested = pyqtSignal(object)
    elementMoved = pyqtSignal(int, tuple)
    roomSelected = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.gridSize = 10
        self.cellSize = 50
        self.scaleFactor = 1.0
        self.offset = QPoint(
            (self.width() - self.gridSize * self.cellSize) // 2,
            (self.height() - self.gridSize * self.cellSize) // 2
        )

        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.lastMousePos = QPoint(0, 0)
        self.isPanning = False
        self.isDragging = False
        self.dragOffset = QPoint(0, 0)
        self.hoveredElement = None

        self.elements = []
        self.connections = []
        self.elementPositions = {}

        self.selectedElement = None

    def setFloorElements(self, elementsDict, connections=None):
        self.elements = []
        self.elementPositions = {}
        for pos, element in elementsDict.items():
            if element and pos:
                if not isinstance(pos, tuple) or len(pos) != 2 or not all(isinstance(coord, int) for coord in pos):
                    continue
                if element.position is None:
                    continue
                elementWidget = FloorElementWidget(
                    elementType=element.type,
                    position=pos,
                    elementId=element.db_id,
                    number=getattr(element, 'number', None),
                    capacity=getattr(element, 'capacity', None),
                    pricePerNight=getattr(element, 'price_per_night', None)
                )
                self.elements.append(elementWidget)
                self.elementPositions[element.db_id] = pos
        self.connections = connections or []
        self.update()

    def clearFloorElements(self):
        self.elements = []
        self.connections = []
        self.selectedElement = None
        self.update()

    def selectElement(self, element):
        for el in self.elements:
            el.selected = False

        self.selectedElement = element

        if element:
            element.selected = True
            if element.elementType == "room":
                self.roomSelected.emit(element)
            else:
                self.roomSelected.emit(None)
        self.update()

    def mapPositionToGrid(self, pos):
        transform = QTransform()
        transform.translate(self.offset.x(), self.offset.y())
        transform.scale(self.scaleFactor, self.scaleFactor)

        inverseTransform, invertible = transform.inverted()
        if not invertible:
            return None

        gridPos = inverseTransform.map(pos)

        gridX = int(gridPos.x() / self.cellSize)
        gridY = int(gridPos.y() / self.cellSize)

        if 0 <= gridX < self.gridSize and 0 <= gridY < self.gridSize:
            return gridX, gridY
        return None

    # Events
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(self.rect(), QColor(245, 245, 245))

        transform = QTransform()
        transform.translate(self.offset.x(), self.offset.y())
        transform.scale(self.scaleFactor, self.scaleFactor)
        painter.setTransform(transform)

        gridWidth = self.gridSize * self.cellSize
        gridHeight = self.gridSize * self.cellSize

        painter.fillRect(0, 0, gridWidth, gridHeight, QColor(255, 255, 255))

        painter.setPen(QPen(QColor(50, 50, 50), 2))
        painter.drawRect(0, 0, gridWidth, gridHeight)

        painter.setPen(QPen(QColor(200, 200, 200)))

        for i in range(1, self.gridSize):
            x = i * self.cellSize
            painter.drawLine(x, 0, x, gridHeight)

        for i in range(1, self.gridSize):
            y = i * self.cellSize
            painter.drawLine(0, y, gridWidth, y)

        # Draw cell coordinates (for debugging)
        # painter.setPen(QPen(QColor(150, 150, 150)))
        # for row in range(self.gridSize):
        #     for col in range(self.gridSize):
        #         x = col * self.cellSize
        #         y = row * self.cellSize
        #         painter.drawText(x + 5, y + 15, f"{col},{row}")

        for element in self.elements:
            if element != self.selectedElement:
                element.drawBackground(painter, self.cellSize)
        if self.selectedElement:
            if not self.isDragging:
                self.selectedElement.drawBackground(painter, self.cellSize)

        if hasattr(self, 'connections'):
            pen = QPen(QColor(255, 150, 150), 2)
            painter.setPen(pen)
            for id1, id2 in self.connections:
                pos1 = self.elementPositions.get(id1)
                pos2 = self.elementPositions.get(id2)
                if pos1 and pos2:
                    x1 = pos1[0] * self.cellSize + self.cellSize // 2
                    y1 = pos1[1] * self.cellSize + self.cellSize // 2
                    x2 = pos2[0] * self.cellSize + self.cellSize // 2
                    y2 = pos2[1] * self.cellSize + self.cellSize // 2
                    painter.drawLine(x1, y1, x2, y2)

        for element in self.elements:
            if element != self.selectedElement:
                element.drawText(painter, self.cellSize)
        if self.selectedElement:
            if self.isDragging:
                mousePos = self.lastMousePos
                transform = QTransform()
                transform.translate(self.offset.x(), self.offset.y())
                transform.scale(self.scaleFactor, self.scaleFactor)
                inverseTransform, _ = transform.inverted()
                scenePos = inverseTransform.map(mousePos)
                self.selectedElement.drawBackground(painter, self.cellSize, scenePos)
                self.selectedElement.drawText(painter, self.cellSize, scenePos)
            else:
                self.selectedElement.drawText(painter, self.cellSize)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position().toPoint()
            gridPos = self.mapPositionToGrid(pos)

            clickedOnElement = False
            for element in self.elements:
                if element.position == gridPos:
                    if element.isDeleteButtonClicked(pos, self.cellSize, self.offset, self.scaleFactor):
                        self.elementDeleteRequested.emit(element)
                        return

                    self.selectElement(element)
                    self.isDragging = True
                    self.lastMousePos = pos
                    self.setCursor(Qt.CursorShape.ClosedHandCursor)
                    clickedOnElement = True
                    break

            if not clickedOnElement:
                self.selectElement(None)
                self.isPanning = True
                self.lastMousePos = pos
                self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        pos = event.position().toPoint()
        gridPos = self.mapPositionToGrid(pos)

        hoveredElement = None
        for element in self.elements:
            if element.position == gridPos:
                hoveredElement = element
                break

        if self.hoveredElement != hoveredElement:
            if self.hoveredElement:
                self.hoveredElement.hovered = False
            self.hoveredElement = hoveredElement
            if self.hoveredElement:
                self.hoveredElement.hovered = True
            self.update()
        if self.hoveredElement and self.isDragging:
            self.hoveredElement.hovered = False
            self.hoveredElement = None
            self.update()

        if self.isDragging and self.selectedElement:
            if not self.selectedElement.position or not isinstance(self.selectedElement.position, tuple) or len(
                    self.selectedElement.position) != 2:
                self.isDragging = False
                self.selectedElement = None
                self.setCursor(Qt.CursorShape.ArrowCursor)
                return

            delta = event.position().toPoint() - self.lastMousePos
            self.lastMousePos = event.position().toPoint()
            self.dragOffset += delta
            self.update()

        elif self.isPanning:
            delta = event.position().toPoint() - self.lastMousePos
            self.offset += delta
            self.lastMousePos = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.isDragging and self.selectedElement:
                gridPos = self.mapPositionToGrid(event.position().toPoint())
                positionIsFree = True
                if gridPos:
                    for element in self.elements:
                        if element == self.selectedElement:
                            continue
                        if element.position == gridPos:
                            positionIsFree = False
                            break
                if gridPos and positionIsFree:
                    self.selectedElement.position = gridPos
                    self.elementMoved.emit(self.selectedElement.elementId, gridPos)

                self.dragOffset = QPoint(0, 0)
                self.isDragging = False
                self.setCursor(Qt.CursorShape.ArrowCursor)
                self.update()
            elif self.isPanning:
                self.isPanning = False
                self.setCursor(Qt.CursorShape.ArrowCursor)

    def leaveEvent(self, event):
        if self.hoveredElement:
            self.hoveredElement.hovered = False
            self.hoveredElement = None
            self.update()

    def wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta().y()
        zoomFactor = 1.1 if delta > 0 else 0.9

        if 0.2 <= self.scaleFactor * zoomFactor <= 3.0:
            oldPos = event.position()

            transform = QTransform()
            transform.translate(self.offset.x(), self.offset.y())
            transform.scale(self.scaleFactor, self.scaleFactor)

            inverseTransform, _ = transform.inverted()
            scenePos = inverseTransform.map(oldPos)

            self.scaleFactor *= zoomFactor

            newTransform = QTransform()
            newTransform.translate(self.offset.x(), self.offset.y())
            newTransform.scale(self.scaleFactor, self.scaleFactor)

            newScenePos = newTransform.map(scenePos)
            deltaPos = newScenePos - oldPos

            self.offset -= deltaPos.toPoint()
            self.update()

    def resizeEvent(self, event):
        self.offset = QPoint(
            (self.width() - self.gridSize * self.cellSize) // 2,
            (self.height() - self.gridSize * self.cellSize) // 2
        )
        self.update()
