from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QLabel, QSizePolicy, QFrame,
)

from src.view.components.app_button import AppButton
from src.view.components.custom_switch import CustomSwitch
from src.utilities.user import User


class HomeWindow(QWidget):
    """Home screen with navigation buttons and user section."""
    def __init__(self, onReservationManagerClick, onSimulatorClick, onHotelConfiguratorClick):
        super().__init__()
        self.onHotelConfiguratorClick = onHotelConfiguratorClick
        self.onReservationManagerClick = onReservationManagerClick
        self.onSimulatorClick = onSimulatorClick

        self.setupUi()
        self.updateButtonStates()

    def setupUi(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(245, 245, 245))
        self.setPalette(palette)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.setSpacing(20)

        self.hotelConfiguratorBtn = AppButton("Hotel", "Configurator")
        self.reservationManagerBtn = AppButton("Reservation", "Manager")
        self.simulatorBtn = AppButton("Simulator", "")

        for btn in [self.hotelConfiguratorBtn, self.reservationManagerBtn, self.simulatorBtn]:
            btn.setMinimumSize(330, 240)
            btn.setMaximumSize(550, 400)
            btn.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
            self.buttonsLayout.addWidget(btn)

        self.hotelConfiguratorBtn.connect(self.handleHotelConfiguratorClick)
        self.reservationManagerBtn.connect(self.handleReservationManagerClick)
        self.simulatorBtn.connect(self.handleSimulatorClick)

        outerLayout = QHBoxLayout()
        outerLayout.setContentsMargins(40, 0, 40, 0)
        outerLayout.addLayout(self.buttonsLayout)

        self.mainLayout.addSpacing(50)
        self.mainLayout.addLayout(outerLayout)

        self.userLayout = QHBoxLayout()
        self.userLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.userLayout.setContentsMargins(0, 0, 0, 0)
        self.userLayout.setSpacing(20)

        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText("Enter your name")
        self.nameInput.textChanged.connect(self.updateButtonStates)

        palette = self.nameInput.palette()
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("white"))
        self.nameInput.setPalette(palette)

        self.nameInput.setFixedSize(200, 35)
        self.nameInput.setStyleSheet(
            """
            QLineEdit {
                color: white;
                background-color: #333;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 6px;
                font-size: 11pt;
            }
            """
        )

        adminFrame = QFrame()
        adminLayout = QHBoxLayout()
        adminLayout.setContentsMargins(8, 3, 8, 3)
        adminLayout.setSpacing(8)
        adminFrame.setLayout(adminLayout)
        adminFrame.setFixedSize(150, 35)
        adminFrame.setStyleSheet(
            """
            QFrame {
                background-color: #333;
                border-radius: 8px;
            }
            """
        )

        self.adminLabel = QLabel("Admin mode")
        self.adminLabel.setStyleSheet("color: white; font-size: 11pt;")

        self.adminSwitch = CustomSwitch()
        self.adminSwitch.toggled.connect(self.updateButtonStates)

        adminLayout.addWidget(self.adminLabel)
        adminLayout.addWidget(self.adminSwitch)

        self.userLayout.addWidget(self.nameInput)
        self.userLayout.addWidget(adminFrame)

        self.userContainerLayout = QHBoxLayout()
        self.userContainerLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.userContainerLayout.setContentsMargins(0, 0, 0, 0)
        self.userContainerLayout.addLayout(self.userLayout)

        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.userContainerLayout)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        width = self.width()
        perBtnWidth = width // 4

        desiredWidth = max(240, min(perBtnWidth, 400))
        desiredHeight = int(desiredWidth / 0.727)

        for btn in [self.reservationManagerBtn, self.simulatorBtn, self.hotelConfiguratorBtn]:
            btn.setFixedSize(desiredWidth, desiredHeight)

        width = self.width()
        perWidgetWidth = width // 4

        desiredWidth = max(240, min(perWidgetWidth, 400))
        desiredHeight = 35

        self.nameInput.setFixedSize(desiredWidth, desiredHeight)

        adminFrame = self.adminSwitch.parent()
        if isinstance(adminFrame, QWidget):
            adminFrame.setFixedSize(desiredWidth, desiredHeight)

        fontSize = max(9, min(16, int(width / 90)))
        self.nameInput.setStyleSheet(
            f"""
                    QLineEdit {{
                        color: white;
                        background-color: #333;
                        border: 1px solid #555;
                        border-radius: 8px;
                        padding: 6px;
                        font-size: {fontSize}pt;
                    }}
                    """
        )
        self.adminLabel.setStyleSheet(f"color: white; font-size: {fontSize}pt;")

    def updateButtonStates(self):
        username = self.nameInput.text().strip()
        isAdmin = self.adminSwitch.isChecked()

        User.username = username
        User.is_admin = isAdmin

        if isAdmin:
            self.reservationManagerBtn.unlock()
            self.simulatorBtn.unlock()
            self.hotelConfiguratorBtn.unlock()
        else:
            if username:
                self.reservationManagerBtn.unlock()
            else:
                self.reservationManagerBtn.lock()

            self.simulatorBtn.lock()
            self.hotelConfiguratorBtn.lock()

    def handleHotelConfiguratorClick(self):
        self.onHotelConfiguratorClick()

    def handleReservationManagerClick(self):
        if not self.reservationManagerBtn.isLocked():
            self.onReservationManagerClick()

    def handleSimulatorClick(self):
        if not self.simulatorBtn.isLocked():
            self.onSimulatorClick()
