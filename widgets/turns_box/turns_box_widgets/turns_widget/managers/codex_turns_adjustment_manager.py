from typing import TYPE_CHECKING, Union
from Enums.Enums import LetterType, Turns


if TYPE_CHECKING:
    from .....pictograph.pictograph import Pictograph
    from .....letterbook.letterbook_turns_widget import LetterBookTurnsWidget


class LetterBookTurnsAdjustmentManager:
    def __init__(self, turns_widget: "LetterBookTurnsWidget") -> None:
        self.turns_widget = turns_widget
        self.pictographs = self._get_pictographs()
        self.letter_type = (
            self.turns_widget.turns_box.turns_panel.turns_tab.section.letter_type
        )

        self.vtg_button_manager = (
            self.turns_widget.turns_box.turns_panel.turns_tab.section.vtg_dir_button_manager
        )
        self.prop_rot_dir_manager = (
            self.turns_widget.turns_box.prop_rot_dir_button_manager
        )

    def adjust_turns(self, adjustment: Turns) -> None:
        turns = self._get_turns()
        turns = self._clamp_turns(turns + adjustment)
        turns = self.convert_turn_floats_to_ints(turns)
        self._update_turns_display(turns)
        self._update_visibility_based_on_motion(turns)
        for pictograph in self.pictographs:
            if self._is_relevant_letter_type(pictograph):
                self._adjust_turns_for_pictograph(pictograph, adjustment)

    def direct_set_turns(self, new_turns: Turns) -> None:
        turns = self._get_turns()
        turns = self.convert_turn_floats_to_ints(turns)
        self._update_turns_display(new_turns)
        self._update_visibility_based_on_motion(new_turns)
        for pictograph in self.pictographs:
            for motion in pictograph.motions.values():
                if self.turns_widget.relevance_checker.is_motion_relevant(motion):
                    self.turns_widget.updater.set_motion_turns(motion, new_turns)

    def get_current_turns_value(self) -> Turns:
        return self._get_turns()

    def _get_pictographs(self) -> list["Pictograph"]:
        return (
            self.turns_widget.turns_box.turns_panel.turns_tab.section.scroll_area.pictograph_cache.values()
        )

    def _get_turns(self) -> Turns:
        turns = self.turns_widget.display_manager.turns_display.text()
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
        self.turns_widget.display_manager.update_turns_display(str(turns))

    def _update_visibility_based_on_motion(self, turns: Turns) -> None:
        button_manager = (
            self.vtg_button_manager
            if self.letter_type in [LetterType.Type2, LetterType.Type3]
            else (self.prop_rot_dir_manager)
        )
        button_manager.update_visibility_based_on_motion(
            turns, self.turns_widget.turns_box.attribute_value
        )

    def _is_relevant_letter_type(self, pictograph: "Pictograph") -> bool:
        return (
            LetterType.get_letter_type(pictograph.letter)
            == self.turns_widget.turns_box.turns_panel.turns_tab.section.letter_type
        )

    def _adjust_turns_for_pictograph(self, pictograph, adjustment) -> None:
        self.turns_widget.updater._adjust_turns_for_pictograph(pictograph, adjustment)
