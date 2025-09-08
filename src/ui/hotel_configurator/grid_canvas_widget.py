from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QTransform, QWheelEvent, QColor, QPen

from src.ui.hotel_configurator.floor_element_widget import FloorElementWidget



class GridCanvas(QWidget):
    elementDeleteRequested = pyqtSignal(object)
    elementMoved = pyqtSignal(int, tuple)  # Signal to emit element_id and new position# Signal to request element deletion

    def __init__(self, parent=None):
        super().__init__(parent)
        # Grid properties
        self.grid_size = 10  # 10x10 grid
        self.cell_size = 50  # Default cell size in pixels
        self.scale_factor = 1.0
        self.offset = QPoint(0, 0)
        self.last_mouse_pos = QPoint(0, 0)
        self.is_panning = False
        self.is_dragging = False
        self.drag_offset = QPoint(0, 0)

        self.hovered_element = None
        self.setMouseTracking(True)

        # New properties for floor elements
        self.elements = []  # List of FloorElementWidgets
        self.selected_element = None

        # Enable mouse tracking for dragging
        self.setMouseTracking(True)

        # Set focus policy to receive keyboard events
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Fill background
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
        painter.setPen(QPen(QColor(150, 150, 150)))
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = col * self.cell_size
                y = row * self.cell_size
                painter.drawText(
                    x + 5, y + 15,
                    f"{col},{row}"
                )

        # Draw floor elements
        for element in self.elements:
            # Pass drag_offset only for the selected element
            if element == self.selected_element and self.is_dragging:
                element.draw(painter, self.cell_size, self.drag_offset)
            else:
                element.draw(painter, self.cell_size)

    # File: src/ui/hotel_configurator/grid_canvas_widget.py
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

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Get the mouse position
            pos = event.position().toPoint()

            # Check if the user clicked on an element
            for element in self.elements:
                if element.position == self.mapPositionToGrid(pos):
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
        grid_pos = self.mapPositionToGrid(pos)

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
                grid_pos = self.mapPositionToGrid(event.position().toPoint())
                if grid_pos:
                    self.selected_element.position = grid_pos

                    # Update the backend with the new position
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
        # Reset hover state when mouse leaves the widget
        if self.hovered_element:
            self.hovered_element.hovered = False
            self.hovered_element = None
            self.update()



    # Add this method for zooming functionality
    def wheelEvent(self, event: QWheelEvent):
        # Get the angle delta (how much the wheel was turned)
        delta = event.angleDelta().y()

        # Determine zoom factor based on wheel direction
        zoom_factor = 1.1 if delta > 0 else 0.9

        # Apply zoom limits
        if 0.2 <= self.scale_factor * zoom_factor <= 3.0:
            # Get the position before zoom
            old_pos = event.position()

            # Convert to scene coordinates
            transform = QTransform()
            transform.translate(self.offset.x(), self.offset.y())
            transform.scale(self.scale_factor, self.scale_factor)

            inverse_transform, _ = transform.inverted()
            scene_pos = inverse_transform.map(old_pos)

            # Apply zoom
            self.scale_factor *= zoom_factor

            # Adjust offset to keep the point under mouse cursor fixed
            new_transform = QTransform()
            new_transform.translate(self.offset.x(), self.offset.y())
            new_transform.scale(self.scale_factor, self.scale_factor)

            new_scene_pos = new_transform.map(scene_pos)
            delta_pos = new_scene_pos - old_pos

            self.offset -= delta_pos.toPoint()

            # Redraw
            self.update()

    def select_element(self, element):
        # Deselect previous selection
        if self.selected_element:
            self.selected_element.selected = False

        self.selected_element = element

        # Select new element
        if element:
            element.selected = True

        self.update()

    def mapPositionToGrid(self, pos):
        """Map screen position to grid position"""
        # Inverse transform the point to get grid coordinates
        transform = QTransform()
        transform.translate(self.offset.x(), self.offset.y())
        transform.scale(self.scale_factor, self.scale_factor)

        # Check if transform is invertible
        inverse_transform, invertible = transform.inverted()
        if not invertible:
            return None

        # Apply inverse transform
        grid_pos = inverse_transform.map(pos)

        # Calculate grid cell
        grid_x = int(grid_pos.x() / self.cell_size)
        grid_y = int(grid_pos.y() / self.cell_size)

        # Check if within grid bounds
        if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
            return grid_x, grid_y
        return None



