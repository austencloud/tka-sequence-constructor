from typing import TYPE_CHECKING, Dict, List
from PyQt6.QtGui import QPixmap
from constants import COLOR, OPP, SAME
from objects.motion.motion import Motion
from utilities.TypeChecking.TypeChecking import Colors
from .base_attr_box import BaseAttrBox
from .attr_box_widgets.base_attr_box_widget import AttrBoxWidget
from .attr_box_widgets.header_widgets.color_header_widget import ColorHeaderWidget
from .attr_box_widgets.turns_widgets.color_turns_widget import ColorTurnsWidget

if TYPE_CHECKING:
    from widgets.attr_panel.color_attr_panel import ColorAttrPanel
    from objects.pictograph.pictograph import Pictograph

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QHBoxLayout


class ColorAttrBox(BaseAttrBox):
    def __init__(
        self,
        attr_panel: "ColorAttrPanel",
        color: Colors,
    ) -> None:
        super().__init__(attr_panel, None)  # Note the None for the single pictograph
        self.attr_panel = attr_panel
        self.color = color
        self.font_size = self.width() // 10
        self.widgets: List[AttrBoxWidget] = []
        self.combobox_border = 2
        self.pixmap_cache: Dict[str, QPixmap] = {}  # Initialize the pixmap cache
        self.hbox_layout = QHBoxLayout(self)
        self.hbox_layout.addLayout(self.vbox_layout)
        self._setup_widgets()
        self.attribute_type = COLOR
        self.vtg_dir_btn_state = {SAME: True, OPP: False}

    def _setup_widgets(self) -> None:  # add common widgets
        self.header_widget = ColorHeaderWidget(self, self.color)
        self.turns_widget = ColorTurnsWidget(self)
        self.vbox_layout.addWidget(self.header_widget, 1)
        self.vbox_layout.addWidget(self.turns_widget, 2)
        self.setLayout(self.hbox_layout)

    def update_attr_box(self, motion: Motion) -> None:
        for pictograph in self.attr_panel.scroll_area.scroll_area.pictographs.values():
            for motion in pictograph.motions.values():
                self.turns_widget.turn_display_manager.update_turns_display(
                    motion.turns
                )

    def get_pictographs(self) -> List["Pictograph"]:
        return list(self.attr_panel.scroll_area.scroll_area.pictographs.values())

