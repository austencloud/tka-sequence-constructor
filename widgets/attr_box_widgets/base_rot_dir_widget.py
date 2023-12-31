from PyQt6.QtWidgets import (
    QLabel,
)
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING, Union
from widgets.attr_box_widgets.base_attr_box_widget import (
    BaseAttrBoxWidget,
)

if TYPE_CHECKING:
    from widgets.graph_editor_tab.graph_editor_header_widget import (
        GraphEditorHeaderWidget,
    )
    from widgets.ig_tab.ig_filter_tab.by_motion_type.ig_motion_type_header_widget import (
        IGMotionTypeHeaderWidget,
    )
    from widgets.ig_tab.ig_filter_tab.by_motion_type.ig_motion_type_attr_box import (
        IGMotionTypeAttrBox,
    )
    from widgets.graph_editor_tab.graph_editor_attr_box import (
        GraphEditorAttrBox,
    )
from constants import BLUE, HEX_BLUE, HEX_RED, RED
from PyQt6.QtWidgets import QFrame, QVBoxLayout


class BaseRotDirWidget(BaseAttrBoxWidget):
    def __init__(
        self: Union["GraphEditorHeaderWidget", "IGMotionTypeHeaderWidget"],
        attr_box: Union["GraphEditorAttrBox", "IGMotionTypeAttrBox"],
    ) -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.header_label = self._setup_header_label()

        self.setMinimumWidth(self.attr_box.width())

    def create_separator(self) -> QFrame:
        separator = QFrame(self)
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Raised)
        separator.setStyleSheet("color: #000000;")  # You can adjust the color as needed
        separator.setMaximumWidth(self.attr_box.width())
        return separator

    def _setup_main_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove all content margins
        self.layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

    def _setup_header_label(self) -> QLabel:
        text = "Left" if self.attr_box.color == BLUE else "Right"
        color_hex = HEX_RED if self.attr_box.color == RED else HEX_BLUE
        label = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"color: {color_hex}; font-weight: bold;")
        return label
