import sys
from collections import defaultdict, namedtuple
from PyQt6.QtWidgets import (
    QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem,
    QGraphicsLineItem, QGraphicsItem
)
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen
from PyQt6.QtCore import Qt, QPointF


TILE_SIZE = 50
GRID_WIDTH = 6
GRID_HEIGHT = 6


Room = namedtuple("Room", ["id", "x", "y", "type", "status"])


class FloorPlanGraph:
    def __init__(self):
        self.nodes = {}  # room_id -> Room
        self.adjacency = defaultdict(set)  # room_id -> connected ids

    def add_room(self, room_id, x, y, type_, status):
        self.nodes[room_id] = Room(room_id, x, y, type_, status)

    def move_room(self, room_id, x, y):
        room = self.nodes[room_id]
        self.nodes[room_id] = room._replace(x=x, y=y)

    def clear_connections(self):
        self.adjacency = defaultdict(set)

    def connect_rooms(self, room1_id, room2_id):
        self.adjacency[room1_id].add(room2_id)
        self.adjacency[room2_id].add(room1_id)


class RoomItem(QGraphicsRectItem):
    def __init__(self, scene, graph, room_id, x, y):
        super().__init__(0, 0, TILE_SIZE, TILE_SIZE)
        self.scene = scene
        self.graph = graph
        self.room_id = room_id
        self.setBrush(QBrush(QColor(100, 200, 250)))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setZValue(0)  # Rooms behind lines
        self.setPos(x * TILE_SIZE, y * TILE_SIZE)
        self.graph.add_room(room_id, x, y, "room", "free")

    def mouseReleaseEvent(self, event):
        new_pos = self.pos()
        snapped_x = round(new_pos.x() / TILE_SIZE)
        snapped_y = round(new_pos.y() / TILE_SIZE)
        self.setPos(QPointF(snapped_x * TILE_SIZE, snapped_y * TILE_SIZE))
        self.graph.move_room(self.room_id, snapped_x, snapped_y)
        self.scene.update_connections()
        super().mouseReleaseEvent(event)


class FloorPlanScene(QGraphicsScene):
    def __init__(self, graph):
        super().__init__(0, 0, GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE)
        self.graph = graph
        self.room_items = {}
        self.connection_lines = []

        self.draw_grid()
        self.create_rooms()

    def draw_grid(self):
        pen_color = QColor(200, 200, 200)
        pen = QPen(pen_color)
        for x in range(GRID_WIDTH + 1):
            self.addLine(x * TILE_SIZE, 0, x * TILE_SIZE, GRID_HEIGHT * TILE_SIZE, pen)
        for y in range(GRID_HEIGHT + 1):
            self.addLine(0, y * TILE_SIZE, GRID_WIDTH * TILE_SIZE, y * TILE_SIZE, pen)

    def create_rooms(self):
        self.add_room(1, 0, 0)
        self.add_room(2, 3, 0)
        self.add_room(3, 0, 3)
        self.update_connections()

    def add_room(self, room_id, x, y):
        room = RoomItem(self, self.graph, room_id, x, y)
        self.addItem(room)
        self.room_items[room_id] = room

    def update_connections(self):
        # Clear visual lines
        for line in self.connection_lines:
            self.removeItem(line)
        self.connection_lines.clear()

        # Clear graph connections
        self.graph.clear_connections()

        # Recalculate based on adjacency
        for id1, room1 in self.graph.nodes.items():
            for id2, room2 in self.graph.nodes.items():
                if id1 == id2:
                    continue
                dx = abs(room1.x - room2.x)
                dy = abs(room1.y - room2.y)
                if (dx == 1 and dy == 0) or (dx == 0 and dy == 1):
                    self.graph.connect_rooms(id1, id2)

        # Draw visual connections
        pen = QPen(QColor(255, 0, 0))  # Red color
        pen.setWidth(3)  # Thicker lines
        for room_id, neighbors in self.graph.adjacency.items():
            for neighbor_id in neighbors:
                # Avoid drawing duplicates
                if room_id > neighbor_id:
                    continue
                p1 = self.room_center(self.room_items[room_id])
                p2 = self.room_center(self.room_items[neighbor_id])
                line = QGraphicsLineItem(p1.x(), p1.y(), p2.x(), p2.y())
                line.setPen(pen)
                line.setZValue(1)  # Above rooms
                self.addItem(line)
                self.connection_lines.append(line)

    def room_center(self, room_item):
        rect = room_item.rect()
        pos = room_item.pos()
        return QPointF(pos.x() + rect.width() / 2, pos.y() + rect.height() / 2)


class FloorPlanView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setFixedSize(GRID_WIDTH * TILE_SIZE + 2, GRID_HEIGHT * TILE_SIZE + 2)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)


def main():
    app = QApplication(sys.argv)
    graph = FloorPlanGraph()
    scene = FloorPlanScene(graph)
    view = FloorPlanView(scene)
    view.setWindowTitle("Hotel Floor Plan - Red Thick Connections On Top")
    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()