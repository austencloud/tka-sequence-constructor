from PyQt6.QtWidgets import QHBoxLayout, QFrame
from typing import TYPE_CHECKING, List
from constants import ANTI, DASH, MOTION_TYPE, PRO, STATIC
from utilities.TypeChecking.TypeChecking import Letters
from widgets.attr_box.attr_box import AttrBox
from widgets.factories.attr_box_factory import AttrBoxFactory
from utilities.TypeChecking.letter_lists import (
    pro_letters,
    anti_letters,
    dash_letters,
    static_letters,
)

if TYPE_CHECKING:
    from widgets.filter_tab import FilterTab


class AttrPanel(QFrame):
    def __init__(self, filter_tab: "FilterTab", attribute_type) -> None:
        super().__init__()
        self.filter_tab = filter_tab
        self.attribute_type = attribute_type
        self.attr_box_factory = AttrBoxFactory(self)
        self.boxes: List[AttrBox] = self.attr_box_factory.create_boxes()
        self.setup_layouts()

    def setup_layouts(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        for box in self.boxes:
            self.layout.addWidget(box)
            # give them black borders
            box.setFrameStyle(1)
            box.setLineWidth(1)

    def resize_attr_panel(self) -> None:
        self.setMinimumWidth(self.filter_tab.width() - self.boxes[0].attr_box_border_width)
        self.setMaximumWidth(self.filter_tab.width() - self.boxes[0].attr_box_border_width)
        for box in self.boxes:
            box.resize_attr_box()

    def show_boxes_based_on_chosen_letters(
        self, selected_letters: List[Letters]
    ) -> None:
        motion_type_mapping = {
            PRO: pro_letters,
            ANTI: anti_letters,
            DASH: dash_letters,
            STATIC: static_letters,
        }

        for box in self.boxes:
            box.hide()

        for box in self.boxes:
            if box.attribute_type == MOTION_TYPE:
                for motion_type, letters in motion_type_mapping.items():
                    if any(letter in selected_letters for letter in letters):
                        if box.motion_type == motion_type:
                            box.show()
