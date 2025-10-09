from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QCursor, QTransform, QBrush, QFont
from PyQt6.QtCore import Qt, QPoint


class SimulatorCanvas(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(245, 245, 245))
        self.setPalette(palette)

        self.cell_size = 70
        self.grid_size = 10
        self.floor_spacing = 50
        self.floors_per_row = 2

        self.scale_factor = 1.0
        self.offset = QPoint(0, 0)
        self.is_panning = False
        self.last_mouse_pos = QPoint(0, 0)

        self.current_date = None
        self.available_rooms = set()
        self.unavailable_rooms = set()

        self.setMouseTracking(True)
        self.first_paint = True

    def showEvent(self, event):
        super().showEvent(event)
        self.centerView()

    def resizeEvent(self, event):
        if hasattr(self, 'first_paint') and self.first_paint:
            self.centerView()
        super().resizeEvent(event)

    def centerView(self):
        total_width, total_height = self.calculateDrawingSize()

        center_x = (self.width() - total_width * self.scale_factor) / 2
        center_y = (self.height() - total_height * self.scale_factor) / 2

        self.offset = QPoint(int(center_x), int(center_y))
        self.update()

    def calculateDrawingSize(self):
        floors = self.controller.get_all_floors()
        if not floors:
            return self.floor_spacing * 2, self.floor_spacing * 2

        floors = sorted(floors, key=lambda f: f.level)

        max_width = 0
        total_height = self.floor_spacing * 2

        current_row_width = self.floor_spacing
        max_height_in_row = 0
        col_count = 0

        for floor in floors:
            floor_grid = self.controller.get_floor_grid(floor.db_id)
            positions = [pos for pos, element in floor_grid.items() if element and pos]

            if not positions:
                continue

            min_x = min([pos[0] for pos in positions]) if positions else 0
            min_y = min([pos[1] for pos in positions]) if positions else 0
            max_x = max([pos[0] for pos in positions]) if positions else 0
            max_y = max([pos[1] for pos in positions]) if positions else 0

            actual_width = (max_x - min_x + 1) * self.cell_size
            actual_height = (max_y - min_y + 1) * self.cell_size

            if col_count >= self.floors_per_row:
                max_width = max(max_width, current_row_width)
                current_row_width = self.floor_spacing
                total_height += max_height_in_row + self.floor_spacing
                max_height_in_row = 0
                col_count = 0

            current_row_width += actual_width + self.floor_spacing
            max_height_in_row = max(max_height_in_row, actual_height)
            col_count += 1

        total_height += max_height_in_row + self.floor_spacing
        max_width = max(max_width, current_row_width)

        return max_width, total_height


    def wheelEvent(self, event):
        mouse_pos = event.position().toPoint()
        old_scale_factor = self.scale_factor

        delta_y = event.angleDelta().y()
        if delta_y == 0:
            return

        zoom_per_step = 1.05
        steps = delta_y / 120.0
        factor = pow(zoom_per_step, steps)

        self.scale_factor *= factor
        self.scale_factor = max(0.2, min(self.scale_factor, 3.0))

        scene_point = (mouse_pos - self.offset) / old_scale_factor

        self.offset = mouse_pos - scene_point * self.scale_factor

        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_panning = True
            self.last_mouse_pos = event.position().toPoint()
            self.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.is_panning:
            self.is_panning = False
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def mouseMoveEvent(self, event):
        if self.is_panning:
            delta = (event.position().toPoint() - self.last_mouse_pos)
            self.offset += delta
            self.last_mouse_pos = event.position().toPoint()
            self.update()

    def mapToScene(self, point):
        return (point - self.offset) / self.scale_factor

    def update_room_availability(self, date):
        self.current_date = date
        date_string = date.toString("yyyy-MM-dd")
        self.available_rooms, self.unavailable_rooms = self.controller.get_rooms_availability_for_date(date_string)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(self.rect(), QColor(245, 245, 245))

        transform = QTransform()
        transform.translate(self.offset.x(), self.offset.y())
        transform.scale(self.scale_factor, self.scale_factor)
        painter.setTransform(transform)

        floors = self.controller.get_all_floors()
        floors = sorted(floors, key=lambda f: f.level)

        current_x = self.floor_spacing
        current_y = self.floor_spacing * 2
        max_height_in_row = 0
        col_count = 0

        for i, floor in enumerate(floors):
            floor_grid = self.controller.get_floor_grid(floor.db_id)

            positions = [pos for pos, element in floor_grid.items() if element and pos]

            if not positions:
                continue

            min_x = min([pos[0] for pos in positions])
            min_y = min([pos[1] for pos in positions])
            max_x = max([pos[0] for pos in positions])
            max_y = max([pos[1] for pos in positions])

            actual_width = (max_x - min_x + 1) * self.cell_size
            actual_height = (max_y - min_y + 1) * self.cell_size

            if col_count >= self.floors_per_row:
                current_x = self.floor_spacing
                current_y += max_height_in_row + self.floor_spacing
                max_height_in_row = 0
                col_count = 0

            painter.setPen(QColor(0, 0, 0))
            title_font = painter.font()
            title_font.setPointSize(14)
            title_font.setBold(True)
            painter.setFont(title_font)

            title_y = current_y - 25
            painter.drawText(
                int(current_x),
                int(title_y),
                f"{floor.name} (Level: {floor.level})"
            )

            default_font = QFont()
            painter.setFont(default_font)

            for pos, element in floor_grid.items():
                if element and pos:
                    adjusted_x = current_x + (pos[0] - min_x) * self.cell_size
                    adjusted_y = current_y + (pos[1] - min_y) * self.cell_size

                    if element.type == "room":
                        if hasattr(self, 'current_date') and self.current_date:
                            if element.db_id in self.available_rooms:
                                painter.fillRect(adjusted_x, adjusted_y, self.cell_size, self.cell_size,
                                                 QColor(150, 230, 150))  # Green for available
                            elif element.db_id in self.unavailable_rooms:
                                painter.fillRect(adjusted_x, adjusted_y, self.cell_size, self.cell_size,
                                                 QColor(230, 150, 150))  # Red for unavailable
                            else:
                                painter.fillRect(adjusted_x, adjusted_y, self.cell_size, self.cell_size,
                                                 QColor(200, 230, 255))  # Default blue
                        else:
                            painter.fillRect(adjusted_x, adjusted_y, self.cell_size, self.cell_size,
                                             QColor(200, 230, 255))
                    elif element.type == "hallway":
                        painter.fillRect(adjusted_x, adjusted_y, self.cell_size, self.cell_size,
                                         QColor(220, 220, 220))
                    elif element.type == "staircase":
                        painter.fillRect(adjusted_x, adjusted_y, self.cell_size, self.cell_size,
                                         QColor(150, 150, 150))

                        painter.setPen(QPen(QColor(80, 80, 80), 2))
                        step_width = self.cell_size / 6
                        for j in range(5):
                            y_pos = adjusted_y + j * step_width + step_width
                            painter.drawLine(
                                int(adjusted_x + step_width),
                                int(y_pos),
                                int(adjusted_x + self.cell_size - step_width),
                                int(y_pos)
                            )

                    painter.setPen(QPen(QColor(100, 100, 100), 1))
                    painter.drawRect(adjusted_x, adjusted_y, self.cell_size, self.cell_size)

                    if element.type == "room":
                        painter.setPen(QColor(0, 0, 0))
                        room_number = getattr(element, 'number', '?')
                        capacity = getattr(element, 'capacity', '?')
                        price = getattr(element, 'price_per_night', '?')

                        current_font = painter.font()

                        bold_font = QFont(current_font)
                        bold_font.setBold(True)

                        painter.setFont(bold_font)
                        painter.drawText(adjusted_x + 5, adjusted_y + 20, f"Room {room_number}")
                        painter.setFont(current_font)

                        painter.drawText(adjusted_x + 5, adjusted_y + 40, f"{capacity} Beds")
                        painter.drawText(adjusted_x + 5, adjusted_y + 60, f"${price}")

            current_x += actual_width + self.floor_spacing
            max_height_in_row = max(max_height_in_row, actual_height)
            col_count += 1

        if hasattr(self, 'first_paint') and self.first_paint:
            self.first_paint = False
