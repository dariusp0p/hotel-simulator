from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QSizePolicy,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor

from src.ui.components.app_button import AppButton
from src.ui.components.custom_switch import CustomSwitch


class MainMenuPage(QWidget):
    def __init__(self, on_reservation_click=None):
        super().__init__()
        self.on_reservation_click = on_reservation_click

        self.setStyleSheet("background-color: #bfbfbf;")

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.init_buttons()
        self.init_user_section()
        self.update_button_states()

    def init_buttons(self):
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setSpacing(20)

        self.reservation_btn = AppButton("Reservation", "Manager")
        self.simulator_btn = AppButton("Simulator", "")
        self.configurator_btn = AppButton("Hotel", "Configurator")

        for btn in [self.reservation_btn, self.simulator_btn, self.configurator_btn]:
            btn.setMinimumSize(240, 330)
            btn.setMaximumSize(400, 550)
            btn.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
            self.buttons_layout.addWidget(btn)

        self.reservation_btn.connect(self.handle_reservation_click)

        outer_layout = QHBoxLayout()
        outer_layout.setContentsMargins(40, 0, 40, 0)
        outer_layout.addLayout(self.buttons_layout)

        self.main_layout.addSpacing(50)
        self.main_layout.addLayout(outer_layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        width = self.width()
        per_btn_width = width // 4

        desired_width = max(240, min(per_btn_width, 400))
        desired_height = int(desired_width / 0.727)

        for btn in [self.reservation_btn, self.simulator_btn, self.configurator_btn]:
            btn.setFixedSize(desired_width, desired_height)

        self.resize_user_section()

    def resize_user_section(self):
        width = self.width()
        per_widget_width = width // 4

        desired_width = max(240, min(per_widget_width, 400))
        desired_height = 35

        self.name_input.setFixedSize(desired_width, desired_height)

        admin_frame = self.admin_switch.parent()
        if isinstance(admin_frame, QWidget):
            admin_frame.setFixedSize(desired_width, desired_height)

        font_size = max(9, min(16, int(width / 90)))
        self.name_input.setStyleSheet(
            f"""
            QLineEdit {{
                color: white;
                background-color: #333;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 6px;
                font-size: {font_size}pt;
            }}
            """
        )
        self.admin_label.setStyleSheet(f"color: white; font-size: {font_size}pt;")

    def init_user_section(self):
        self.user_layout = QHBoxLayout()
        self.user_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_layout.setContentsMargins(0, 0, 0, 0)
        self.user_layout.setSpacing(20)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        self.name_input.textChanged.connect(self.update_button_states)

        palette = self.name_input.palette()
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("white"))
        self.name_input.setPalette(palette)

        self.name_input.setFixedSize(200, 35)
        self.name_input.setStyleSheet(
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

        admin_frame = QFrame()
        admin_layout = QHBoxLayout()
        admin_layout.setContentsMargins(8, 3, 8, 3)
        admin_layout.setSpacing(8)
        admin_frame.setLayout(admin_layout)
        admin_frame.setFixedSize(150, 35)
        admin_frame.setStyleSheet(
            """
            QFrame {
                background-color: #333;
                border-radius: 8px;
            }
            """
        )

        self.admin_label = QLabel("Admin mode")
        self.admin_label.setStyleSheet("color: white; font-size: 11pt;")

        self.admin_switch = CustomSwitch()
        self.admin_switch.toggled.connect(self.update_button_states)

        admin_layout.addWidget(self.admin_label)
        admin_layout.addWidget(self.admin_switch)

        self.user_layout.addWidget(self.name_input)
        self.user_layout.addWidget(admin_frame)

        self.user_container_layout = QHBoxLayout()
        self.user_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_container_layout.setContentsMargins(0, 0, 0, 0)
        self.user_container_layout.addLayout(self.user_layout)

        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(self.user_container_layout)

    def update_button_states(self):
        name_entered = self.name_input.text().strip() != ""
        is_admin = self.admin_switch.isChecked()

        if is_admin:
            self.reservation_btn.unlock()
            self.simulator_btn.unlock()
            self.configurator_btn.unlock()
        else:
            if name_entered:
                self.reservation_btn.unlock()
            else:
                self.reservation_btn.lock()

            self.simulator_btn.lock()
            self.configurator_btn.lock()

    def handle_reservation_click(self):
        if not self.reservation_btn.is_locked() and self.on_reservation_click:
            self.on_reservation_click(self.admin_switch.isChecked())
