from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont
from typing import Union, TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.attr_box_widgets.motion_types_widget import MotionTypeWidget
    from widgets.attr_box_widgets.start_end_loc_widget import StartEndLocWidget
    from widgets.attr_box_widgets.base_turns_widget import BaseTurnsWidget


class AttrBoxButton(QPushButton):
    def __init__(
        self,
        parent_widget: Union[
            "StartEndLocWidget", "BaseTurnsWidget", "MotionTypeWidget"
        ],
    ) -> None:
        super().__init__(parent_widget)
        self.parent_widget = parent_widget

    def update_attr_box_turns_button_size(self, button_size) -> None:
        self.button_size = button_size
        self.border_radius = button_size / 2
        self.setMinimumSize(button_size, button_size)
        self.setIconSize(QSize(int(button_size * 0.6), int(button_size * 0.6)))
        self.setStyleSheet(self._get_button_style())
        self.setFont(QFont("Arial", int(button_size * 0.3)))

    def _get_button_style(self):
        return (
            f"QPushButton {{"
            f"   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(200, 200, 200, 255));"
            f"   border-radius: {self.border_radius}px;"
            f"   border: 1px solid black;"
            f"   min-width: {self.button_size}px;"
            f"   min-height: {self.button_size}px;"
            f"   max-width: {self.button_size}px;"
            f"   max-height: {self.button_size}px;"
            f"}}"
            f"QPushButton:hover {{"
            f"   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(230, 230, 230, 255), stop:1 rgba(200, 200, 200, 255));"
            f"}}"
            f"QPushButton:pressed {{"
            f"   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(204, 228, 247, 255), stop:1 rgba(164, 209, 247, 255));"
            f"}}"
        )
