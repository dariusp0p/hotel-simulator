from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QSizePolicy,
    QGraphicsBlurEffect,
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class AppButton(QWidget):
    def __init__(self, line1: str, line2: str):
        super().__init__()

        self.base_text = f"{line1}\n{line2}" if line2 else line1
        self.locked = True

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.button = QPushButton(self.base_text)
        self.button.setEnabled(False)
        self.button.setStyleSheet(
            """
            QPushButton {
                background-color: #777;
                color: black;
                border-radius: 12px;
                font-size: 14pt;
                padding: 30px 10px;
            }
            """
        )
        self.button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.layout.addWidget(self.button)

        self.lock_icon = QLabel(self)
        self.lock_icon.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.lock_icon.setStyleSheet("background: transparent;")

        pixmap = QPixmap("src/ui/assets/lock_icon.png")
        if pixmap.isNull():
            print(f'The path: "src/ui/lock_icon.png" does not contain the image.')
        elif not pixmap.hasAlphaChannel():
            print("The image is not transparent. Use a PNG image with a alpha channel.")
        else:
            self.lock_icon.setPixmap(
                pixmap.scaled(
                    70,
                    70,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

        self.lock_icon.setFixedSize(70, 70)
        self.lock_icon.setVisible(True)
        self.lock_icon.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        x = self.button.x() + (self.button.width() - self.lock_icon.width()) // 2
        y = self.button.y() + (self.button.height() - self.lock_icon.height()) // 2
        self.lock_icon.move(x, y)

    def lock(self):
        self.locked = True
        self.button.setEnabled(False)
        self.button.setStyleSheet(
            """
            QPushButton {
                background-color: #777;
                color: black;
                border-radius: 12px;
                font-size: 16pt;
                padding: 30px 10px;
            }
            """
        )
        self.lock_icon.setVisible(True)
        self.lock_icon.raise_()

        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(4)
        self.button.setGraphicsEffect(blur)

    def unlock(self):
        self.locked = False
        self.button.setEnabled(True)
        self.button.setStyleSheet(
            """
            QPushButton {
                background-color: #333;
                color: white;
                border-radius: 12px;
                font-size: 16pt;
                padding: 30px 10px;
            }
            QPushButton:hover {
                background-color: #444;
            }
            """
        )
        self.lock_icon.setVisible(False)
        self.button.setGraphicsEffect(None)

    def is_locked(self):
        return self.locked

    def connect(self, func):
        self.button.clicked.connect(func)
