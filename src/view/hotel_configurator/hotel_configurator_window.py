import random
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QInputDialog, QMessageBox
)

from src.controller.dto import AddFloorRequest, RenameFloorRequest, UpdateFloorLevelRequest, RemoveFloorRequest, \
    AddElementRequest, EditRoomRequest, MoveElementRequest, RemoveElementRequest
from src.view.components.top_bar import TopBar
from src.view.hotel_configurator.components.side_bar import SideBar
from src.view.hotel_configurator.components.hot_bar import HotBar
from src.view.hotel_configurator.components.grid_canvas_widget import GridCanvas


class HotelConfiguratorWindow(QMainWindow):
    """Window for configuring hotel floors and rooms."""
    def __init__(self, onBack, controller):
        super().__init__()
        self.onBack = onBack
        self.controller = controller

        self.selectedFloor = None
        self.selectedRoom = None

        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Hotel Configurator")
        self.resize(1200, 800)

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)

        self.gridCanvas = GridCanvas()
        self.gridCanvas.elementDeleteRequested.connect(self.handleDeleteElementClick)
        self.gridCanvas.elementMoved.connect(self.handleElementMoved)
        self.gridCanvas.roomSelected.connect(self.handleRoomSelected)

        self.topBar = TopBar([
            {"label": "← Back", "callback": self.handleBack},
            {"label": "↩ Undo", "callback": self.undoAction},
            {"label": "↪ Redo", "callback": self.redoAction},
        ])
        self.updateUndoRedoButtons()

        self.sideBar = SideBar(
            controller=self.controller,
            onFloorSelected=self.handleFloorSelected,
            onFloorsReordered=self.handleFloorsReordered,
            onAddFloor=self.handleAddFloorClick,
            onRemoveFloor=self.handleRemoveFloorClick,
            onUpdateFloorName=self.handleUpdateFloorClick,
            onUpdateRoom=self.handleUpdateRoomClick
        )

        self.hotBar = HotBar(
            addElementCallback=self.handleAddElementClick
        )

        self.layout = QVBoxLayout(self.mainWidget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.gridCanvas)

        self.topBar.setParent(self.mainWidget)
        self.sideBar.setParent(self.mainWidget)
        self.hotBar.setParent(self.mainWidget)

        self.resizeEvent(None)

    def handleBack(self):
        self.onBack()

    def undoAction(self):
        self.controller.undo()
        self.updateUndoRedoButtons()

        self.sideBar.populateFloorList()
        self.ensureSelectedFloorExists()
        floorGrid = self.controller.get_floor_grid(self.selectedFloor.db_id)
        connections = self.controller.get_floor_connections(self.selectedFloor.db_id)
        self.gridCanvas.setFloorElements(floorGrid, connections)
        self.gridCanvas.selectElement(None)
        self.gridCanvas.update()

    def redoAction(self):
        self.controller.redo()
        self.updateUndoRedoButtons()

        self.sideBar.populateFloorList()
        self.ensureSelectedFloorExists()
        floorGrid = self.controller.get_floor_grid(self.selectedFloor.db_id)
        connections = self.controller.get_floor_connections(self.selectedFloor.db_id)
        self.gridCanvas.setFloorElements(floorGrid, connections)
        self.gridCanvas.selectElement(None)
        self.gridCanvas.update()

    def updateUndoRedoButtons(self):
        self.topBar.setButtonEnabled("↩ Undo", self.controller.can_undo())
        self.topBar.setButtonEnabled("↪ Redo", self.controller.can_redo())

    def refreshGrid(self):
        if self.selectedFloor is None:
            self.gridCanvas.setFloorElements({}, [])
            self.gridCanvas.selectElement(None)
            self.gridCanvas.update()
        else:
            floorGrid = self.controller.get_floor_grid(self.selectedFloor.db_id)
            connections = self.controller.get_floor_connections(self.selectedFloor.db_id)
            self.gridCanvas.setFloorElements(floorGrid, connections)
            self.gridCanvas.selectElement(None)
            self.gridCanvas.update()

    def ensureSelectedFloorExists(self):
        floors = self.controller.get_all_floors()
        if not floors:
            self.selectedFloor = None
            self.gridCanvas.clearFloorElements()
            return

        selectedId = getattr(self.selectedFloor, "db_id", None)
        floorIds = [f.db_id for f in floors]
        if selectedId in floorIds:
            return

        sortedFloors = sorted(floors, key=lambda f: f.level, reverse=True)
        self.selectedFloor = sortedFloors[0]
        self.sideBar.floorList.setCurrentRow(0)
        self.handleFloorSelected(self.sideBar.floorList.item(0))

    def resizeEvent(self, event):
        margin = 10

        self.topBar.setGeometry(
            margin,
            margin,
            self.width() - 2 * margin,
            self.topBar.height()
        )

        topMargin = self.topBar.height() + 2 * margin

        self.sideBar.setGeometry(
            margin,
            topMargin,
            self.sideBar.width(),
            self.height() - topMargin - margin
        )

        self.hotBar.setGeometry(
            self.sideBar.width() + 2 * margin,
            self.height() - self.hotBar.height() - margin,
            self.width() - self.sideBar.width() - 3 * margin,
            self.hotBar.height()
        )

    # Floor CRUD
    def handleFloorSelected(self, item):
        self.gridCanvas.selectElement(None)
        self.selectedFloor = item.data(Qt.ItemDataRole.UserRole)
        self.sideBar.floorNameEdit.setText(self.selectedFloor.name)
        self.sideBar.floorNameEdit.setPlaceholderText(self.selectedFloor.name)
        try:
            self.refreshGrid()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load floor elements: {str(e)}")
            self.gridCanvas.clearFloorElements()

    def handleAddFloorClick(self):
        floorName, ok = QInputDialog.getText(
            self, "Add New Floor", "Enter floor name:"
        )

        if not ok:
            return

        if not floorName:
            QMessageBox.warning(self, "Warning", "Please enter floor name")
            return

        try:
            self.gridCanvas.selectElement(None)
            req = AddFloorRequest(name=floorName, level=self.sideBar.floorList.count())
            self.controller.add_floor(req)
            self.updateUndoRedoButtons()
            self.sideBar.populateFloorList()
            QMessageBox.information(self, "Success", "Floor added successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add floor: {str(e)}")
            return

    def handleFloorsReordered(self):
        updates = []
        for i in range(self.sideBar.floorList.count()):
            item = self.sideBar.floorList.item(i)
            floor = item.data(Qt.ItemDataRole.UserRole)
            newLevel = self.sideBar.floorList.count() - 1 - i
            if floor.level != newLevel:
                updates.append((floor.db_id, newLevel))

        for floorId, level in updates:
            try:
                req = UpdateFloorLevelRequest(floor_id=floorId, new_level=level)
                self.controller.update_floor_level(req)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update floor order: {str(e)}")
                return
        self.updateUndoRedoButtons()
        self.sideBar.populateFloorList()

    def handleUpdateFloorClick(self):
        if not self.selectedFloor:
            QMessageBox.warning(self, "Warning", "Please select a floor first")
            return

        newName = self.sideBar.floorNameEdit.text().strip()
        if not newName:
            QMessageBox.warning(self, "Warning", "Please enter floor name")
            return

        oldName = self.selectedFloor.name
        if newName == oldName:
            return

        try:
            req = RenameFloorRequest(floor_id=self.selectedFloor.db_id, new_name=newName)
            self.controller.rename_floor(req)
            self.updateUndoRedoButtons()
            self.sideBar.populateFloorList()
            QMessageBox.information(self, "Success", "Floor renamed successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to rename floor: {str(e)}")

    def handleRemoveFloorClick(self):
        if not self.selectedFloor:
            QMessageBox.warning(self, "Warning", "Please select a floor first")
            return

        numRooms, numReservations = self.controller.get_floor_number_of_rooms(self.selectedFloor.db_id)
        if numRooms > 0:
            reply = QMessageBox.question(
                self,
                "Delete Floor",
                f"This floor contains {numRooms} room(s) and {numReservations} reservation(s). Deleting it will remove all rooms and their reservations. Continue?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        try:
            req = RemoveFloorRequest(floor_id=self.selectedFloor.db_id)
            self.controller.remove_floor(req)
            self.updateUndoRedoButtons()
            self.sideBar.populateFloorList()
            self.gridCanvas.clearFloorElements()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to remove floor: {str(e)}")
            return

    # Element CRUD
    def findFirstFreePosition(self):
        floorGrid = self.controller.get_floor_grid(self.selectedFloor.db_id)

        gridSize = self.gridCanvas.gridSize
        for x in range(gridSize):
            for y in range(gridSize):
                if (x, y) not in floorGrid or floorGrid[(x, y)] is None:
                    return (x, y)
        return None

    def findRandomFreePosition(self):
        floorGrid = self.controller.get_floor_grid(self.selectedFloor.db_id)

        freePositions = []
        gridSize = self.gridCanvas.gridSize
        for x in range(gridSize):
            for y in range(gridSize):
                if (x, y) not in floorGrid or floorGrid[(x, y)] is None:
                    freePositions.append((x, y))

        if not freePositions:
            return None

        return random.choice(freePositions)

    def handleRoomSelected(self, room):
        self.selectedRoom = room
        self.sideBar.displayRoomDetails(room)

    def handleAddElementClick(self, elementType):
        if not self.selectedFloor:
            QMessageBox.warning(self, "Warning", "Please select a floor first")
            return

        position = self.findFirstFreePosition()
        if not position:
            QMessageBox.warning(self, "Warning", "No free space available on this floor")

        try:
            if elementType == "room":
                req = AddElementRequest(
                    type="room", floor_id=self.selectedFloor.db_id,
                    position=position, number="1",
                    capacity=2, price_per_night=100.0
                )
            elif elementType == "hallway":
                req = AddElementRequest(
                    type="hallway", floor_id=self.selectedFloor.db_id,
                    position=position
                )
            elif elementType == "staircase":
                req = AddElementRequest(
                    type="staircase", floor_id=self.selectedFloor.db_id,
                    position=position
                )
            else:
                raise ValueError("Invalid element type")

            self.controller.add_element(req)
            self.updateUndoRedoButtons()
            self.selectedFloor = self.controller.get_floor(self.selectedFloor.db_id)
            self.refreshGrid()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add room: {str(e)}")

    def handleUpdateRoomClick(self):
        if not self.selectedRoom:
            QMessageBox.warning(self, "Warning", "Please select a room first")
            return

        try:
            number = self.sideBar.roomNumberEdit.text()
            capacityText = self.sideBar.roomCapacityEdit.text()
            priceText = self.sideBar.roomPriceEdit.text()

            if not number:
                QMessageBox.warning(self, "Warning", "Room number cannot be empty")
                return
            try:
                capacity = int(capacityText)
                if capacity <= 0:
                    raise ValueError("Capacity must be positive")
            except ValueError:
                QMessageBox.warning(self, "Warning", "Capacity must be a positive number")
                return
            try:
                price = float(priceText)
                if price < 0:
                    raise ValueError("Price cannot be negative")
            except ValueError:
                QMessageBox.warning(self, "Warning", "Price must be a valid number")
                return

            req = EditRoomRequest(self.selectedRoom.elementId, number, capacity, price)
            self.controller.edit_room(req)
            self.updateUndoRedoButtons()
            self.refreshGrid()

            QMessageBox.information(self, "Success", "Room updated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update room: {str(e)}")

    def handleElementMoved(self, elementId, newPosition):
        try:
            req = MoveElementRequest(element_id=elementId, floor_id=self.selectedFloor.db_id, position=newPosition)
            self.controller.move_element(req)
            self.updateUndoRedoButtons()
            self.refreshGrid()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to move element: {str(e)}")
            self.refreshGrid()

    def handleDeleteElementClick(self, elementWidget):
        elementId = elementWidget.elementId
        self.selectedFloor = self.controller.get_floor(self.selectedFloor.db_id)
        element = self.selectedFloor.elements.get(elementId)

        if not element:
            QMessageBox.critical(self, "Error", "Failed to find the corresponding FloorElement.")
            return

        elementType = element.type.capitalize()

        if element.type == "room":
            numReservations = self.controller.get_room_number_of_reservations(element.db_id)
            if numReservations > 0:
                reply = QMessageBox.question(
                    self,
                    "Delete Room",
                    f"This room has {numReservations} reservation(s). Deleting it will remove all reservations. Continue?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                if reply != QMessageBox.StandardButton.Yes:
                    return

        try:
            req = RemoveElementRequest(
                element_id=element.db_id, type=element.type,
                floor_id=self.selectedFloor.db_id, position=element.position
            )
            self.controller.remove_element(req)
            self.updateUndoRedoButtons()
            self.refreshGrid()
            if element.type == "room":
                QMessageBox.information(self, "Success", f"Room successfully deleted!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete {elementType.lower()}: {str(e)}")
