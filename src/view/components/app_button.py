from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QSizePolicy,
    QGraphicsBlurEffect,
)


class AppButton(QWidget):
    """A large button with lock/unlock functionality."""
    def __init__(self, line1: str, line2: str):
        super().__init__()

        self.baseText = f"{line1}\n{line2}" if line2 else line1
        self.locked = True

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.button = QPushButton(self.baseText)
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

        self.lockIcon = QLabel(self)
        self.lockIcon.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.lockIcon.setStyleSheet("background: transparent;")

        pixmap = QPixmap("src/view/assets/lock_icon.png")
        if pixmap.isNull():
            print(f'The path: "src/ui/lock_icon.png" does not contain the image.')
        elif not pixmap.hasAlphaChannel():
            print("The image is not transparent. Use a PNG image with a alpha channel.")
        else:
            self.lockIcon.setPixmap(
                pixmap.scaled(
                    70,
                    70,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

        self.lockIcon.setFixedSize(70, 70)
        self.lockIcon.setVisible(True)
        self.lockIcon.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        x = self.button.x() + (self.button.width() - self.lockIcon.width()) // 2
        y = self.button.y() + (self.button.height() - self.lockIcon.height()) // 2
        self.lockIcon.move(x, y)

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
        self.lockIcon.setVisible(True)
        self.lockIcon.raise_()

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
        self.lockIcon.setVisible(False)
        self.button.setGraphicsEffect(None)

    def isLocked(self):
        return self.locked

    def connect(self, func):
        self.button.clicked.connect(func)
