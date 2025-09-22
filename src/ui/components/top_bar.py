from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor



class TopBar(QWidget):
    def __init__(self, buttons_config, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(60, 60, 60))
        self.setPalette(palette)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        back_button_config = next((btn for btn in buttons_config if btn['label'] == "← Back"), None)
        if back_button_config:
            back_button = QPushButton(back_button_config['label'])
            back_button.setFixedSize(80, 40)
            back_button.setStyleSheet(
                "QPushButton {background-color: #333; color: white; border: none; font-weight: bold; padding: 8px;} "
                "QPushButton:hover {background-color: #555;}"
            )
            back_button.setCursor(Qt.CursorShape.PointingHandCursor)
            back_button.clicked.connect(back_button_config['callback'])
            layout.addWidget(back_button)
        else:
            layout.addSpacerItem(QSpacerItem(80, 40, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))

        layout.addStretch()

        for config in buttons_config:
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

    def set_button_enabled(self, button: str, enabled: bool):
        for b in self.findChildren(QPushButton):
            if b.text() == button:
                b.setEnabled(enabled)