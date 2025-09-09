from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QTransform, QWheelEvent, QColor, QPen

from src.ui.hotel_configurator.components.floor_element_widget import FloorElementWidget



class GridCanvas(QWidget):
    elementDeleteRequested = pyqtSignal(object)
    elementMoved = pyqtSignal(int, tuple)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_size = 10
        self.cell_size = 50
        self.scale_factor = 1.0
        self.offset = QPoint(
            (self.width() - self.grid_size * self.cell_size) // 2,
            (self.height() - self.grid_size * self.cell_size) // 2
        )

        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.last_mouse_pos = QPoint(0, 0)
        self.is_panning = False
        self.is_dragging = False
        self.drag_offset = QPoint(0, 0)
        self.hovered_element = None

        self.elements = []
        self.selected_element = None

    def set_floor_elements(self, elements_dict):
        """Set floor elements from a dictionary where keys are positions and values are elements"""
        self.elements = []
        for pos, element in elements_dict.items():
            if element and pos:  # Ensure element and position are not None
                if not isinstance(pos, tuple) or len(pos) != 2 or not all(isinstance(coord, int) for coord in pos):
                    print(f"Invalid position: {pos}")
                    continue
                if element.position is None:  # Additional check for element position
                    print(f"Element has no position: {element}")
                    continue
                element_widget = FloorElementWidget(
                    element_type=element.type,
                    position=pos,
                    element_id=element.db_id,
                    number=getattr(element, 'number', None),
                    capacity=getattr(element, 'capacity', None)
                )
                self.elements.append(element_widget)
        self.update()

    def clear_elements(self):
        """Clear all elements from the grid"""
        self.elements = []
        self.selected_element = None
        self.update()

    def select_element(self, element):
        # if self.selected_element:
        #     self.selected_element.selected = False
        for el in self.elements:
            el.selected = False
        self.selected_element = element
        if element:
            element.selected = True
        self.update()



    def map_position_to_grid(self, pos):
        transform = QTransform()
        transform.translate(self.offset.x(), self.offset.y())
        transform.scale(self.scale_factor, self.scale_factor)

        inverse_transform, invertible = transform.inverted()
        if not invertible:
            return None

        grid_pos = inverse_transform.map(pos)

        grid_x = int(grid_pos.x() / self.cell_size)
        grid_y = int(grid_pos.y() / self.cell_size)

        if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
            return grid_x, grid_y
        return None


    # EVENTS
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(self.rect(), QColor(245, 245, 245))

        # Apply zoom and pan transformations
        transform = QTransform()
        transform.translate(self.offset.x(), self.offset.y())
        transform.scale(self.scale_factor, self.scale_factor)
        painter.setTransform(transform)

        # Calculate grid dimensions
        grid_width = self.grid_size * self.cell_size
        grid_height = self.grid_size * self.cell_size

        # Draw the grid background
        painter.fillRect(0, 0, grid_width, grid_height, QColor(255, 255, 255))

        # Draw grid border
        painter.setPen(QPen(QColor(50, 50, 50), 2))
        painter.drawRect(0, 0, grid_width, grid_height)

        # Draw grid lines
        painter.setPen(QPen(QColor(200, 200, 200)))

        # Draw vertical lines
        for i in range(1, self.grid_size):
            x = i * self.cell_size
            painter.drawLine(x, 0, x, grid_height)

        # Draw horizontal lines
        for i in range(1, self.grid_size):
            y = i * self.cell_size
            painter.drawLine(0, y, grid_width, y)

        # Draw cell coordinates (for debugging)
        # painter.setPen(QPen(QColor(150, 150, 150)))
        # for row in range(self.grid_size):
        #     for col in range(self.grid_size):
        #         x = col * self.cell_size
        #         y = row * self.cell_size
        #         painter.drawText(x + 5, y + 15, f"{col},{row}")

        for element in self.elements:
            if element != self.selected_element:
                element.draw(painter, self.cell_size)
        if self.is_dragging:
            mouse_pos = self.last_mouse_pos
            transform = QTransform()
            transform.translate(self.offset.x(), self.offset.y())
            transform.scale(self.scale_factor, self.scale_factor)
            inverse_transform, _ = transform.inverted()
            scene_pos = inverse_transform.map(mouse_pos)
            self.selected_element.draw(painter, self.cell_size, scene_pos)


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position().toPoint()

            # Check if the user clicked on an element
            for element in self.elements:
                if element.position == self.map_position_to_grid(pos):
                    # Check if the delete button was clicked
                    if element.is_delete_button_clicked(pos, self.cell_size, self.offset, self.scale_factor):
                        self.elementDeleteRequested.emit(element)
                        return

                    # Otherwise, select the element for dragging
                    self.selected_element = element
                    self.is_dragging = True
                    self.last_mouse_pos = pos
                    self.setCursor(Qt.CursorShape.ClosedHandCursor)
                    return

            # If no element is clicked, enable panning
            self.is_panning = True
            self.last_mouse_pos = pos
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        pos = event.position().toPoint()
        grid_pos = self.map_position_to_grid(pos)

        # Check if the mouse is over an element
        hovered_element = None
        for element in self.elements:
            if element.position == grid_pos:
                hovered_element = element
                break

        # Update hover state
        if self.hovered_element != hovered_element:
            if self.hovered_element:
                self.hovered_element.hovered = False
            self.hovered_element = hovered_element
            if self.hovered_element:
                self.hovered_element.hovered = True
            self.update()
        if self.hovered_element and self.is_dragging:
            self.hovered_element.hovered = False
            self.hovered_element = None
            self.update()


        # Handle dragging
        if self.is_dragging and self.selected_element:
            # Validate position
            if not self.selected_element.position or not isinstance(self.selected_element.position, tuple) or len(
                    self.selected_element.position) != 2:
                self.is_dragging = False
                self.selected_element = None
                self.setCursor(Qt.CursorShape.ArrowCursor)
                return

            # Calculate the delta movement
            delta = event.position().toPoint() - self.last_mouse_pos
            self.last_mouse_pos = event.position().toPoint()

            # Update drag offset for smooth visual movement
            self.drag_offset += delta

            # Update visually without changing the grid position yet
            self.update()

        # Handle panning
        elif self.is_panning:
            delta = event.position().toPoint() - self.last_mouse_pos
            self.offset += delta
            self.last_mouse_pos = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.is_dragging and self.selected_element:
                # Snap the element to the nearest grid cell
                grid_pos = self.map_position_to_grid(event.position().toPoint())

                position_is_free = True
                if grid_pos:
                    for element in self.elements:
                        # Skip checking against the element being dragged
                        if element == self.selected_element:
                            continue

                        # Check if position is already occupied
                        if element.position == grid_pos:
                            position_is_free = False
                            break

                if grid_pos and position_is_free:
                    self.selected_element.position = grid_pos
                    self.elementMoved.emit(self.selected_element.element_id, grid_pos)

                # Reset drag offset
                self.drag_offset = QPoint(0, 0)
                self.is_dragging = False
                self.selected_element = None
                self.setCursor(Qt.CursorShape.ArrowCursor)
                self.update()
            elif self.is_panning:
                self.is_panning = False
                self.setCursor(Qt.CursorShape.ArrowCursor)

    def leaveEvent(self, event):
        if self.hovered_element:
            self.hovered_element.hovered = False
            self.hovered_element = None
            self.update()

    def wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta().y()
        zoom_factor = 1.1 if delta > 0 else 0.9

        if 0.2 <= self.scale_factor * zoom_factor <= 3.0:
            old_pos = event.position()

            transform = QTransform()
            transform.translate(self.offset.x(), self.offset.y())
            transform.scale(self.scale_factor, self.scale_factor)

            inverse_transform, _ = transform.inverted()
            scene_pos = inverse_transform.map(old_pos)

            self.scale_factor *= zoom_factor

            new_transform = QTransform()
            new_transform.translate(self.offset.x(), self.offset.y())
            new_transform.scale(self.scale_factor, self.scale_factor)

            new_scene_pos = new_transform.map(scene_pos)
            delta_pos = new_scene_pos - old_pos

            self.offset -= delta_pos.toPoint()

            self.update()

    def resizeEvent(self, event):
        self.offset = QPoint(
            (self.width() - self.grid_size * self.cell_size) // 2,
            (self.height() - self.grid_size * self.cell_size) // 2
        )
        self.update()

