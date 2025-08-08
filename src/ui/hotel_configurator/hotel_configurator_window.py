from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QListWidget, QListWidgetItem,
    QInputDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QPoint, QRectF, QSize, pyqtSignal
from PyQt6.QtGui import QPainter, QTransform, QWheelEvent, QColor, QPen, QFont


class GridCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Grid properties
        self.grid_size = 10  # 10x10 grid
        self.cell_size = 50  # Default cell size in pixels
        self.scale_factor = 1.0
        self.offset = QPoint(0, 0)
        self.last_mouse_pos = QPoint(0, 0)
        self.is_panning = False

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

    def wheelEvent(self, event: QWheelEvent):
        # Calculate zoom factor based on wheel delta
        zoom_factor = 1.1
        if event.angleDelta().y() > 0:
            self.scale_factor *= zoom_factor
        else:
            self.scale_factor /= zoom_factor

        # Limit scale factor to reasonable values
        self.scale_factor = max(0.2, min(5.0, self.scale_factor))

        # Update the canvas
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_panning = True
            self.last_mouse_pos = event.position().toPoint()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def mouseMoveEvent(self, event):
        if self.is_panning:
            delta = event.position().toPoint() - self.last_mouse_pos
            self.offset += delta
            self.last_mouse_pos = event.position().toPoint()
            self.update()

    def reset_view(self):
        self.scale_factor = 1.0
        self.offset = QPoint(0, 0)
        self.update()






class FloorListWidget(QListWidget):
    floorsReordered = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Enable drag and drop
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

        # Style
        self.setStyleSheet("""
            QListWidget {
                background-color: #555;
                color: white;
                border: none;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #666;
            }
            QListWidget::item:selected {
                background-color: #4a6ea9;
            }
            QListWidget::item:hover {
                background-color: #666;
            }
        """)

    def dropEvent(self, event):
        # Call parent implementation to handle the visual reordering
        super().dropEvent(event)
        # Emit signal that floors have been reordered
        self.floorsReordered.emit()












class HotelConfiguratorWindow(QMainWindow):
    def __init__(self, on_back=None, controller=None):
        super().__init__()
        self.on_back = on_back
        self.controller = controller

        self.setWindowTitle("Hotel Configurator")
        self.resize(1200, 800)

        self.selected_floor = None

        # Create main widget
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Create the grid canvas
        self.grid_canvas = GridCanvas()

        # Create top bar
        self.top_bar = self.create_top_bar()

        # Create side bar
        self.side_bar = self.create_side_bar()

        self.hot_bar = self.create_hot_bar()

        # Set layout
        self.layout = QVBoxLayout(self.main_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.grid_canvas)

        # Position top bar and side bar over the grid
        self.top_bar.setParent(self.main_widget)
        self.side_bar.setParent(self.main_widget)
        self.hot_bar.setParent(self.main_widget)

        # Update UI layout when resized
        self.resizeEvent(None)

    def create_top_bar(self):
        top_bar = QWidget()
        top_bar.setFixedHeight(50)
        top_bar.setAutoFillBackground(True)

        # Style the top bar
        palette = top_bar.palette()
        palette.setColor(top_bar.backgroundRole(), QColor(60, 60, 60))
        top_bar.setPalette(palette)

        # Layout
        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(10, 5, 10, 5)

        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setFixedSize(80, 40)
        back_btn.setStyleSheet(
            "QPushButton {background-color: #333; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #555;}"
        )
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(self.handle_back)

        # Undo button
        undo_btn = QPushButton("↩ Undo")
        undo_btn.setFixedSize(80, 40)
        undo_btn.setStyleSheet(
            "QPushButton {background-color: #333; color: white; border: none; padding: 8px;} "
            "QPushButton:hover {background-color: #555;}"
        )
        undo_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Redo button
        redo_btn = QPushButton("↪ Redo")
        redo_btn.setFixedSize(80, 40)
        redo_btn.setStyleSheet(
            "QPushButton {background-color: #333; color: white; border: none; padding: 8px;} "
            "QPushButton:hover {background-color: #555;}"
        )
        redo_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Title
        title = QLabel("Hotel Configurator")
        title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")

        # Add widgets to layout
        layout.addWidget(back_btn)
        layout.addWidget(undo_btn)
        layout.addWidget(redo_btn)
        layout.addSpacing(20)
        layout.addWidget(title)
        layout.addStretch()

        return top_bar

    def create_side_bar(self):
        side_bar = QWidget()
        side_bar.setFixedWidth(250)
        side_bar.setAutoFillBackground(True)

        # Style the side bar to match top and hot bars
        palette = side_bar.palette()
        palette.setColor(side_bar.backgroundRole(), QColor(60, 60, 60))
        side_bar.setPalette(palette)

        # Main layout for side bar
        main_layout = QVBoxLayout(side_bar)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Create upper section (Floors)
        upper_section = QWidget()
        upper_layout = QVBoxLayout(upper_section)
        upper_layout.setContentsMargins(0, 0, 0, 0)
        upper_layout.setSpacing(5)

        # Floors title
        floors_title = QLabel("Floors")
        floors_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        floors_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        floors_title.setStyleSheet("color: white;")

        # Add separator after title
        floors_separator = QFrame()
        floors_separator.setFrameShape(QFrame.Shape.HLine)
        floors_separator.setFrameShadow(QFrame.Shadow.Sunken)
        floors_separator.setStyleSheet("background-color: #777;")

        # Create floor list widget
        self.floor_list = FloorListWidget()
        self.floor_list.itemClicked.connect(self.on_floor_selected)
        self.floor_list.floorsReordered.connect(self.on_floors_reordered)

        # Create buttons container
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 5, 0, 0)
        buttons_layout.setSpacing(10)

        # Add floor button
        add_floor_btn = QPushButton("Add")
        add_floor_btn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        add_floor_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_floor_btn.clicked.connect(self.on_add_floor)

        # Remove floor button
        remove_floor_btn = QPushButton("Remove")
        remove_floor_btn.setStyleSheet(
            "QPushButton {background-color: #a94a4a; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #b95a5a;}"
        )
        remove_floor_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_floor_btn.clicked.connect(self.on_remove_floor)

        # Add buttons to layout
        buttons_layout.addWidget(add_floor_btn)
        buttons_layout.addWidget(remove_floor_btn)

        # Add widgets to upper layout
        upper_layout.addWidget(floors_title)
        upper_layout.addWidget(floors_separator)
        upper_layout.addWidget(self.floor_list, 1)
        upper_layout.addWidget(buttons_container)

        # Create lower section (Selected Floor)
        lower_section = QWidget()
        lower_layout = QVBoxLayout(lower_section)
        lower_layout.setContentsMargins(0, 0, 0, 0)
        lower_layout.setSpacing(5)

        # Selected Floor title
        selected_floor_title = QLabel("Selected Floor")
        selected_floor_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        selected_floor_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        selected_floor_title.setStyleSheet("color: white;")

        # Add separator after title
        selected_floor_separator = QFrame()
        selected_floor_separator.setFrameShape(QFrame.Shape.HLine)
        selected_floor_separator.setFrameShadow(QFrame.Shadow.Sunken)
        selected_floor_separator.setStyleSheet("background-color: #777;")

        # Selected floor content placeholder
        self.selected_floor_panel = QWidget()
        self.selected_floor_panel.setStyleSheet("background-color: #555;")

        # Add widgets to lower layout
        lower_layout.addWidget(selected_floor_title)
        lower_layout.addWidget(selected_floor_separator)
        lower_layout.addWidget(self.selected_floor_panel, 1)

        # Add both sections to main layout
        main_layout.addWidget(upper_section, 1)
        main_layout.addWidget(lower_section, 1)

        # Populate floor list
        self.populate_floor_list()

        return side_bar

    def create_hot_bar(self):
        hot_bar = QWidget()
        hot_bar.setFixedHeight(60)
        hot_bar.setAutoFillBackground(True)

        # Style the hot bar
        palette = hot_bar.palette()
        palette.setColor(hot_bar.backgroundRole(), QColor(60, 60, 60))
        hot_bar.setPalette(palette)

        # Layout
        layout = QHBoxLayout(hot_bar)
        layout.setContentsMargins(10, 5, 10, 5)

        # Add Room button
        add_room_btn = QPushButton("Add Room")
        add_room_btn.setFixedSize(120, 40)
        add_room_btn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        add_room_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Add Hallway button
        add_hallway_btn = QPushButton("Add Hallway")
        add_hallway_btn.setFixedSize(120, 40)
        add_hallway_btn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        add_hallway_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Add Staircase button
        add_staircase_btn = QPushButton("Add Staircase")
        add_staircase_btn.setFixedSize(120, 40)
        add_staircase_btn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        add_staircase_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Add widgets to layout
        layout.addWidget(add_room_btn)
        layout.addWidget(add_hallway_btn)
        layout.addWidget(add_staircase_btn)
        layout.addStretch()

        return hot_bar

    def resizeEvent(self, event):
        margin = 10

        # Position the top bar
        self.top_bar.setGeometry(
            margin,
            margin,
            self.width() - 2 * margin,
            self.top_bar.height()
        )

        # Position the side bar - extend to the bottom with just a small gap
        top_margin = self.top_bar.height() + 2 * margin
        self.side_bar.setGeometry(
            margin,
            top_margin,
            self.side_bar.width(),
            self.height() - top_margin - margin  # Leave just bottom margin
        )

        # Position the hot bar
        self.hot_bar.setGeometry(
            self.side_bar.width() + 2 * margin,
            self.height() - self.hot_bar.height() - margin,
            self.width() - self.side_bar.width() - 3 * margin,
            self.hot_bar.height()
        )

    def handle_back(self):
        if self.on_back:
            self.on_back()

    def populate_floor_list(self):
        self.floor_list.clear()

        floors = self.controller.get_sidebar_floors()
        for floor in floors:
            item = QListWidgetItem(floor.name)
            item.setData(Qt.ItemDataRole.UserRole, floor)
            self.floor_list.addItem(item)

    def on_floor_selected(self, item):
        self.selected_floor = item.data(Qt.ItemDataRole.UserRole)
        # TODO

    def on_add_floor(self):
        floor_name, ok = QInputDialog.getText(
            self, "Add New Floor", "Enter floor name:"
        )

        if not ok:
            return

        if not floor_name:
            QMessageBox.warning(self, "Warning", "Please enter floor name")
            return

        try:
            self.controller.add_floor(floor_name, self.floor_list.count())
            self.populate_floor_list()
            QMessageBox.information(self, "Success", "Floor added successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add floor: {str(e)}")
            return

    def on_floors_reordered(self):
        # Update the levels of all floors based on their new positions
        for i in range(self.floor_list.count()):
            item = self.floor_list.item(i)
            floor = item.data(Qt.ItemDataRole.UserRole)
            # Set level in reverse order (top item has highest level)
            new_level = self.floor_list.count() - 1 - i

            # Only update if level changed
            if floor.level != new_level:
                try:
                    self.controller.update_floor_level(floor.db_id, new_level)
                    # Update the local floor object
                    floor.level = new_level
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to update floor order: {str(e)}")
                    # Refresh the list to show the correct order
                    self.populate_floor_list()
                    return

    def on_remove_floor(self):
        # Get the currently selected floor and remove it
        selected_floor = self.selected_floor
        print(selected_floor.db_id, selected_floor.name)
        try:
            self.controller.remove_floor(selected_floor.db_id)
            self.populate_floor_list()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to remove floor: {str(e)}")
            return
