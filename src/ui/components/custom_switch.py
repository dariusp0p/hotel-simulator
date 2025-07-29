from PyQt6.QtWidgets import QWidget, QAbstractButton
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, pyqtProperty
from PyQt6.QtGui import QPainter, QColor, QBrush


class CustomSwitch(QAbstractButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self._margin = 3
        self._handle_radius = 12
        self._bg_color = QColor("#777")
        self._checked_color = QColor("#00aa00")
        self._handle_color = QColor("white")
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
            QBrush(self._checked_color if self.isChecked() else self._bg_color)
        )
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        handle_radius = radius - self._margin
        diameter = 2 * handle_radius
        x = self._offset
        y = (self.height() - diameter) // 2
        painter.drawEllipse(int(x), int(y), int(diameter), int(diameter))

        painter.setBrush(QBrush(self._handle_color))
        painter.drawEllipse(int(x), int(y), int(diameter), int(diameter))

    def resizeEvent(self, event):
        self._offset = (
            self._margin
            if not self.isChecked()
            else self.width() - 2 * self._handle_radius - self._margin
        )
        self.update()

    def nextCheckState(self):
        self.setChecked(not self.isChecked())

    def setChecked(self, checked):
        super().setChecked(checked)
        start = self._offset
        end = (
            self.width() - self._handle_radius * 2 + self._margin / 2
            if checked
            else self._margin
        )
        self._anim.stop()
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)
        self._anim.start()

    def get_offset(self):
        return self._offset

    def set_offset(self, value):
        self._offset = value
        self.update()

    offset = pyqtProperty(float, fget=get_offset, fset=set_offset)
