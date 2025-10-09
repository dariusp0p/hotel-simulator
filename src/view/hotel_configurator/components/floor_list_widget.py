from PyQt6.QtWidgets import QListWidget
from PyQt6.QtCore import pyqtSignal



class FloorListWidget(QListWidget):
    floorsReordered = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

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
        super().dropEvent(event)
        self.floorsReordered.emit()
