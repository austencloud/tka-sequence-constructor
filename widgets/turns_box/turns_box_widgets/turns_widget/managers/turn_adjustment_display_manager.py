from typing import TYPE_CHECKING, List, Union
from Enums import LetterType
from constants import DASH, STATIC
from utilities.TypeChecking.TypeChecking import Turns

if TYPE_CHECKING:
    from .....pictograph.pictograph import Pictograph
    from ....turns_box_widgets.turns_widget.turns_widget import TurnsWidget


class TurnsAdjustmentDisplayManager:
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        self.turns_widget = turns_widget
        self.pictographs = self._get_pictographs()

    def adjust_turns(self, adjustment: Turns) -> None:
        turns = self._get_turns()
        turns = self._clamp_turns(turns + adjustment)
        self._update_turns_display(turns)
        self._update_visibility_based_on_motion(turns)
        for pictograph in self.pictographs:
            if self._is_relevant_letter_type(pictograph):
                self._adjust_turns_for_pictograph(pictograph, adjustment)

    def set_turns(self, new_turns: Turns) -> None:
        self._update_motion_properties(new_turns)
        turns = self._get_turns()
        self._update_turns_display(new_turns)
        self._update_visibility_based_on_motion(turns)

    def reset_turns_display(self) -> None:
        self._update_turns_display("0")
        self._update_motion_properties(0)

    def get_current_turns_value(self) -> Turns:
        return self._get_turns()

    # Private methods

    def _get_pictographs(self) -> List["Pictograph"]:
        return (
            self.turns_widget.turns_box.turns_panel.filter_tab.section.scroll_area.pictographs.values()
        )

    def _get_turns(self) -> Turns:
        turns = self.turns_widget.turns_display_manager.turns_display.text()
        turns = self.convert_turns_from_str_to_num(turns)
        turns = self.convert_turn_floats_to_ints(turns)
        return turns

    def convert_turns_from_str_to_num(self, turns) -> Union[int, float]:
        return int(turns) if turns in ["0", "1", "2", "3"] else float(turns)

    def convert_turn_floats_to_ints(self, turns: Turns) -> Turns:
        if turns in [0.0, 1.0, 2.0, 3.0]:
            return int(turns)
        else:
            return turns

    def _clamp_turns(self, turns: Turns) -> Turns:
        return self.turns_widget.updater._clamp_turns(turns)

    def _update_turns_display(self, turns: Turns) -> None:
        self.turns_widget.turns_display_manager.update_turns_display(str(turns))

    def _update_visibility_based_on_motion(self, turns: Turns) -> None:
        letter_type = (
            self.turns_widget.turns_box.turns_panel.filter_tab.section.letter_type
        )
        if self.turns_widget.turns_box.attribute_value in [STATIC, DASH]:
            button_manager = (
                self.turns_widget.turns_box.turns_panel.filter_tab.section.vtg_dir_button_manager
            )
            button_manager.update_visibility_based_on_motion(letter_type, turns)

    def _is_relevant_letter_type(self, pictograph: "Pictograph") -> bool:
        return (
            LetterType.get_letter_type(pictograph.letter)
            == self.turns_widget.turns_box.turns_panel.filter_tab.section.letter_type
        )

    def _adjust_turns_for_pictograph(self, pictograph, adjustment) -> None:
        self.turns_widget.updater._adjust_turns_for_pictograph(pictograph, adjustment)

    def _update_motion_properties(self, new_turns) -> None:
        for pictograph in self.pictographs:
            for motion in pictograph.motions.values():
                if self.turns_widget.relevance_checker.is_motion_relevant(motion):
                    self.turns_widget.updater.update_motion_properties(
                        motion, new_turns
                    )
