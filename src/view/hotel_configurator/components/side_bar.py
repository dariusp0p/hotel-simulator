from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QLineEdit, QListWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

from src.view.hotel_configurator.components.floor_list_widget import FloorListWidget


class SideBar(QWidget):
    """A sidebar for managing floors and rooms in the hotel configurator."""
    def __init__(self, controller, onFloorSelected, onFloorsReordered, onAddFloor, onRemoveFloor,
                 onUpdateFloorName, onUpdateRoom, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.onFloorSelected = onFloorSelected
        self.onFloorsReordered = onFloorsReordered
        self.onAddFloor = onAddFloor
        self.onRemoveFloor = onRemoveFloor
        self.onUpdateFloorName = onUpdateFloorName
        self.onUpdateRoom = onUpdateRoom

        self.setupUi()

    def setupUi(self):
        self.setFixedWidth(250)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(60, 60, 60))
        self.setPalette(palette)

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(10)

        # Upper section (Floors)
        upperSection = QWidget()
        upperLayout = QVBoxLayout(upperSection)
        upperLayout.setContentsMargins(0, 0, 0, 0)
        upperLayout.setSpacing(5)

        floorsTitle = QLabel("Floors")
        floorsTitle.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        floorsTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        floorsTitle.setStyleSheet("color: white;")

        floorsSeparator = QFrame()
        floorsSeparator.setFrameShape(QFrame.Shape.HLine)
        floorsSeparator.setFrameShadow(QFrame.Shadow.Sunken)
        floorsSeparator.setStyleSheet("background-color: #777;")

        self.floorList = FloorListWidget()
        self.floorList.itemClicked.connect(self.onFloorSelected)
        self.floorList.floorsReordered.connect(self.onFloorsReordered)

        buttonsContainer = QWidget()
        buttonsLayout = QHBoxLayout(buttonsContainer)
        buttonsLayout.setContentsMargins(0, 5, 0, 0)
        buttonsLayout.setSpacing(10)

        addFloorBtn = QPushButton("Add")
        addFloorBtn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        addFloorBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        addFloorBtn.clicked.connect(self.onAddFloor)

        removeFloorBtn = QPushButton("Remove")
        removeFloorBtn.setStyleSheet(
            "QPushButton {background-color: #a94a4a; color: white; border: none; font-weight: bold; padding: 8px;} "
            "QPushButton:hover {background-color: #b95a5a;}"
        )
        removeFloorBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        removeFloorBtn.clicked.connect(self.onRemoveFloor)

        buttonsLayout.addWidget(addFloorBtn)
        buttonsLayout.addWidget(removeFloorBtn)

        upperLayout.addWidget(floorsTitle)
        upperLayout.addWidget(floorsSeparator)
        upperLayout.addWidget(self.floorList, 1)
        upperLayout.addWidget(buttonsContainer)

        # Lower section (Selected Floor + Selected Room)
        lowerSection = QWidget()
        lowerLayout = QVBoxLayout(lowerSection)
        lowerLayout.setContentsMargins(0, 0, 0, 0)
        lowerLayout.setSpacing(5)

        # Selected Floor Section
        selectedFloorTitle = QLabel("Selected Floor")
        selectedFloorTitle.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        selectedFloorTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        selectedFloorTitle.setStyleSheet("color: white;")

        selectedFloorSeparator = QFrame()
        selectedFloorSeparator.setFrameShape(QFrame.Shape.HLine)
        selectedFloorSeparator.setFrameShadow(QFrame.Shadow.Sunken)
        selectedFloorSeparator.setStyleSheet("background-color: #777;")

        self.selectedFloorPanel = QWidget()
        self.selectedFloorPanel.setStyleSheet("background-color: #555;")
        selectedFloorLayout = QVBoxLayout(self.selectedFloorPanel)

        nameEditContainer = QWidget()
        nameEditLayout = QHBoxLayout(nameEditContainer)
        nameEditLayout.setContentsMargins(0, 0, 0, 0)

        self.floorNameEdit = QLineEdit()
        self.floorNameEdit.setStyleSheet(
            "background-color: #444; color: white; border: 1px solid #666; padding: 5px;")
        self.floorNameEdit.setPlaceholderText("Floor name")

        updateNameBtn = QPushButton("Update")
        updateNameBtn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; padding: 5px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        updateNameBtn.clicked.connect(self.onUpdateFloorName)

        nameEditLayout.addWidget(self.floorNameEdit)
        nameEditLayout.addWidget(updateNameBtn)

        selectedFloorLayout.addWidget(nameEditContainer)
        selectedFloorLayout.addStretch()

        lowerLayout.addWidget(selectedFloorTitle)
        lowerLayout.addWidget(selectedFloorSeparator)
        lowerLayout.addWidget(self.selectedFloorPanel, 1)

        # Selected Room Section
        selectedRoomTitle = QLabel("Selected Room")
        selectedRoomTitle.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        selectedRoomTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        selectedRoomTitle.setStyleSheet("color: white;")

        selectedRoomSeparator = QFrame()
        selectedRoomSeparator.setFrameShape(QFrame.Shape.HLine)
        selectedRoomSeparator.setFrameShadow(QFrame.Shadow.Sunken)
        selectedRoomSeparator.setStyleSheet("background-color: #777;")

        self.selectedRoomPanel = QWidget()
        self.selectedRoomPanel.setStyleSheet("background-color: #555;")
        selectedRoomLayout = QVBoxLayout(self.selectedRoomPanel)

        roomNumberContainer = QWidget()
        roomNumberLayout = QHBoxLayout(roomNumberContainer)
        roomNumberLayout.setContentsMargins(0, 0, 0, 0)

        self.roomNumberEdit = QLineEdit()
        self.roomNumberEdit.setStyleSheet(
            "background-color: #444; color: white; border: 1px solid #666; padding: 5px;")
        self.roomNumberEdit.setPlaceholderText("Room number")

        roomNumberLayout.addWidget(QLabel("Number:"))
        roomNumberLayout.addWidget(self.roomNumberEdit)

        roomCapacityContainer = QWidget()
        roomCapacityLayout = QHBoxLayout(roomCapacityContainer)
        roomCapacityLayout.setContentsMargins(0, 0, 0, 0)

        self.roomCapacityEdit = QLineEdit()
        self.roomCapacityEdit.setStyleSheet(
            "background-color: #444; color: white; border: 1px solid #666; padding: 5px;")
        self.roomCapacityEdit.setPlaceholderText("Capacity")

        roomCapacityLayout.addWidget(QLabel("Capacity:"))
        roomCapacityLayout.addWidget(self.roomCapacityEdit)

        roomPriceContainer = QWidget()
        roomPriceLayout = QHBoxLayout(roomPriceContainer)
        roomPriceLayout.setContentsMargins(0, 0, 0, 0)

        self.roomPriceEdit = QLineEdit()
        self.roomPriceEdit.setStyleSheet(
            "background-color: #444; color: white; border: 1px solid #666; padding: 5px;")
        self.roomPriceEdit.setPlaceholderText("Price per night")

        roomPriceLayout.addWidget(QLabel("Price:"))
        roomPriceLayout.addWidget(self.roomPriceEdit)

        updateRoomBtn = QPushButton("Update")
        updateRoomBtn.setStyleSheet(
            "QPushButton {background-color: #4a6ea9; color: white; border: none; padding: 5px;} "
            "QPushButton:hover {background-color: #5a7eb9;}"
        )
        updateRoomBtn.clicked.connect(self.onUpdateRoom)

        selectedRoomLayout.addWidget(roomNumberContainer)
        selectedRoomLayout.addWidget(roomCapacityContainer)
        selectedRoomLayout.addWidget(roomPriceContainer)
        selectedRoomLayout.addWidget(updateRoomBtn)

        lowerLayout.addWidget(selectedRoomTitle)
        lowerLayout.addWidget(selectedRoomSeparator)
        lowerLayout.addWidget(self.selectedRoomPanel, 1)

        # Add sections to main layout
        mainLayout.addWidget(upperSection, 1)
        mainLayout.addWidget(lowerSection, 1)

        self.populateFloorList()

    def populateFloorList(self):
        self.floorList.clear()
        floors = self.controller.get_all_floors()
        for floor in floors:
            item = QListWidgetItem(floor.name)
            item.setData(Qt.ItemDataRole.UserRole, floor)
            self.floorList.addItem(item)

    def displayRoomDetails(self, room):
        if room:
            self.roomNumberEdit.setText(str(room.number))
            self.roomCapacityEdit.setText(str(room.capacity))
            self.roomPriceEdit.setText(str(room.pricePerNight))
        else:
            self.roomNumberEdit.clear()
            self.roomCapacityEdit.clear()
            self.roomPriceEdit.clear()
