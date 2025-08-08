from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QTransform, QWheelEvent, QColor, QPen

from src.ui.hotel_configurator.floor_element_widget import FloorElementWidget



class GridCanvas(QWidget):
    elementDeleteRequested = pyqtSignal(object)  # Signal to request element deletion

    def __init__(self, parent=None):
        super().__init__(parent)
        # Grid properties
        self.grid_size = 10  # 10x10 grid
        self.cell_size = 50  # Default cell size in pixels
        self.scale_factor = 1.0
        self.offset = QPoint(0, 0)
        self.last_mouse_pos = QPoint(0, 0)
        self.is_panning = False

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
            element.draw(painter, self.cell_size)

    def set_floor_elements(self, elements_dict):
        """Set floor elements from a dictionary where keys are positions and values are elements"""
        self.elements = []
        for pos, element in elements_dict.items():
            if element:  # Check if there is an element at this position
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
            self.is_panning = True
            self.last_mouse_pos = event.position().toPoint()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            self.setMouseTracking(True)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Always reset panning state
            self.is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)

            # Handle click logic
            if (event.position().toPoint() - self.last_mouse_pos).manhattanLength() < 3:
                pos = event.position().toPoint()

                # Transform the point to grid coordinates
                transform = QTransform()
                transform.translate(self.offset.x(), self.offset.y())
                transform.scale(self.scale_factor, self.scale_factor)

                inverse_transform, invertible = transform.inverted()
                if not invertible:
                    return

                grid_pos = inverse_transform.map(pos)

                for element in self.elements:
                    if element.is_delete_button_clicked(grid_pos, self.cell_size * self.scale_factor):
                        print("Delete button clicked for element:", element.element_id)
                        self.elementDeleteRequested.emit(element)
                        return  # Stop after handling the delete
                    elif element.position == self.mapPositionToGrid(pos):
                        self.select_element(element)
                        return

                self.select_element(None)

    def mouseMoveEvent(self, event):
        if self.is_panning:
            delta = event.position().toPoint() - self.last_mouse_pos
            self.offset += delta
            self.last_mouse_pos = event.position().toPoint()
            self.update()
        else:
            # Get the mouse position in grid coordinates
            pos = event.position().toPoint()
            transformed_pos = self.mapPositionToGrid(pos)

            # Reset hover state for all elements
            for element in self.elements:
                element.hovered = False

            self.hovered_element = None

            # Check if the mouse is over a valid grid position
            if transformed_pos:
                grid_x, grid_y = transformed_pos

                # Find the element at the grid position
                for element in self.elements:
                    if element.position == (grid_x, grid_y):
                        element.hovered = True
                        self.hovered_element = element
                        break  # Stop after finding the first hovered element

            # Debugging: Log hover state for all elements
            self.update()  # Redraw the grid  # Redraw the grid  # Redraw to show hover effects  # Redraw to show hover effects  # Redraw to show hover effects

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



