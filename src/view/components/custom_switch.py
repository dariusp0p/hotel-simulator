from PyQt6.QtWidgets import QAbstractButton
from PyQt6.QtCore import Qt, QPropertyAnimation, pyqtProperty
from PyQt6.QtGui import QPainter, QColor, QBrush


class CustomSwitch(QAbstractButton):
    """A custom toggle switch widget."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self._margin = 3
        self._handleRadius = 12
        self._bgColor = QColor("#777")
        self._checkedColor = QColor("#00aa00")
        self._handleColor = QColor("white")
        self._offset = self._margin
        self._anim = QPropertyAnimation(self, b"offset", self)
        self._anim.setDuration(120)

        self.setFixedSize(50, 26)

    def hitButton(self, pos):
        return self.contentsRect().contains(pos)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        radius = rect.height() // 2

        painter.setBrush(
            QBrush(self._checkedColor if self.isChecked() else self._bgColor)
        )
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        handleRadius = radius - self._margin
        diameter = 2 * handleRadius
        x = self._offset
        y = (self.height() - diameter) // 2
        painter.drawEllipse(int(x), int(y), int(diameter), int(diameter))

        painter.setBrush(QBrush(self._handleColor))
        painter.drawEllipse(int(x), int(y), int(diameter), int(diameter))

    def resizeEvent(self, event):
        self._offset = (
            self._margin
            if not self.isChecked()
            else self.width() - 2 * self._handleRadius - self._margin
        )
        self.update()

    def nextCheckState(self):
        self.setChecked(not self.isChecked())

    def setChecked(self, checked):
        super().setChecked(checked)
        start = self._offset
        end = (
            self.width() - self._handleRadius * 2 + self._margin / 2
            if checked
            else self._margin
        )
        self._anim.stop()
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)
        self._anim.start()

    def getOffset(self):
        return self._offset

    def setOffset(self, value):
        self._offset = value
        self.update()

    offset = pyqtProperty(float, fget=getOffset, fset=setOffset)
