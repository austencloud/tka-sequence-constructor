from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame
from typing import TYPE_CHECKING, Union



from ...base_attr_box_widget import AttrBoxWidget
from ...base_attr_box_widget import AttrBoxWidget
from .turn_adjustment_manager import TurnAdjustmentManager
from .turn_direct_set_manager import TurnDirectSetManager
from .turn_display_manager import TurnDisplayManager

if TYPE_CHECKING:
    from ....color_attr_box import ColorAttrBox
    from ....motion_type_attr_box import MotionTypeAttrBox
    from ....lead_state_attr_box import LeadStateAttrBox


class TurnsWidget(AttrBoxWidget):
    def __init__(self, attr_box) -> None:
        super().__init__(attr_box)
        self.attr_box: Union[
            "ColorAttrBox", "MotionTypeAttrBox", "LeadStateAttrBox"
        ] = attr_box
        self.vbox_layout: QVBoxLayout = QVBoxLayout(self)
        self.turn_direct_set_manager = TurnDirectSetManager(self)
        self.turn_adjustment_manager = TurnAdjustmentManager(self.attr_box, self)
        self.turn_display_manager = TurnDisplayManager(self, self.attr_box)

        self.initialize_components()
        self.setup_ui()
        # self.resize_turns_widget()

    def initialize_components(self) -> None:
        """Initialize components here."""
        self.turns_label = None

    def setup_ui(self) -> None:
        self.turn_adjustment_manager.setup_adjustment_buttons()
        self.turn_display_manager.setup_display_components()
        self.turn_direct_set_manager.setup_direct_set_buttons()

    def _convert_turns_from_str_to_num(self, turns) -> Union[int, float]:
        """Convert turn values from string to numeric."""
        return int(turns) if turns in ["0", "1", "2", "3"] else float(turns)

    @staticmethod
    def create_frame(layout: QHBoxLayout) -> QFrame:
        frame = QFrame()
        frame.setLayout(layout)
        frame.setContentsMargins(0, 0, 0, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        return frame

    def resize_turns_widget(self) -> None:
        self.turn_display_manager.update_turnbox_size()
        self.turn_display_manager.update_adjust_turns_button_size()