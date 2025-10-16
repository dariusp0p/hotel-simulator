from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class TopBar(QWidget):
    """A top bar with dynamic buttons."""
    def __init__(self, buttonsConfig, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(60, 60, 60))
        self.setPalette(palette)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        backButtonConfig = next((btn for btn in buttonsConfig if btn['label'] == "← Back"), None)
        if backButtonConfig:
            backButton = QPushButton(backButtonConfig['label'])
            backButton.setFixedSize(80, 40)
            backButton.setStyleSheet(
                "QPushButton {background-color: #333; color: white; border: none; font-weight: bold; padding: 8px;} "
                "QPushButton:hover {background-color: #555;}"
            )
            backButton.setCursor(Qt.CursorShape.PointingHandCursor)
            backButton.clicked.connect(backButtonConfig['callback'])
            layout.addWidget(backButton)
        else:
            layout.addSpacerItem(QSpacerItem(80, 40, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))

        layout.addStretch()

        for config in buttonsConfig:
            if config['label'] not in ["← Back"]:
                button = QPushButton(config['label'])
                button.setFixedSize(80, 40)
                button.setStyleSheet(
                    "QPushButton {background-color: #333; color: white; border: none; font-weight: bold; padding: 8px;} "
                    "QPushButton:hover {background-color: #555;}"
                    "QPushButton:disabled {background-color: #888; color: #ccc;}"
                )
                button.setCursor(Qt.CursorShape.PointingHandCursor)
                button.clicked.connect(config['callback'])
                layout.addWidget(button)

    def setButtonEnabled(self, button: str, enabled: bool):
        for b in self.findChildren(QPushButton):
            if b.text() == button:
                b.setEnabled(enabled)
