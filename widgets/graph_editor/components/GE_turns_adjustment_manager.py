from typing import TYPE_CHECKING, Union
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QApplication
from Enums.Enums import Turns


if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_turns_widget import GE_TurnsWidget


from PyQt6.QtCore import pyqtSignal


class GE_TurnsAdjustmentManager(QObject):
    turns_adjusted = pyqtSignal(float)

    def __init__(self, turns_widget: "GE_TurnsWidget") -> None:
        super().__init__(turns_widget)
        self.turns_widget = turns_widget
        self.graph_editor = self.turns_widget.turns_box.graph_editor
        self.beat_frame = self.graph_editor.sequence_modifier.sequence_widget.beat_frame
        self.main_widget = self.graph_editor.main_widget
        self.json_manager = self.main_widget.json_manager
        self.current_sequence_json_handler = (
            self.json_manager.current_sequence_json_handler
        )
        self.json_validation_engine = (
            self.current_sequence_json_handler.validation_engine
        )
        self.color = self.turns_widget.turns_box.color

        self.turns_adjusted.connect(self.beat_frame.on_beat_adjusted)

    def adjust_turns(self, adjustment: Union[int, float]) -> None:
        self.pictograph = self.graph_editor.GE_pictograph_view.get_current_pictograph()
        new_turns = self._get_turns()
        new_turns = self._clamp_turns(new_turns + adjustment)
        new_turns = self.convert_turn_floats_to_ints(new_turns)
        self._update_turns_display(new_turns)
        QApplication.processEvents()
        self.turns_widget.updater._adjust_turns_for_pictograph(
            self.pictograph, adjustment
        )
        pictograph_index = self.beat_frame.get_index_of_currently_selected_beat()
        QApplication.processEvents()
        self.current_sequence_json_handler.update_turns_in_json_at_index(
            pictograph_index + 1, self.color, new_turns
        )
        QApplication.processEvents()
        self.json_validation_engine.run()
        QApplication.processEvents()
        self.turns_adjusted.emit(new_turns)

    def direct_set_turns(self, new_turns: Turns) -> None:
        self.pictograph = self.graph_editor.GE_pictograph_view.get_current_pictograph()
        self._update_motion_properties(new_turns)
        pictograph_index = self.beat_frame.get_index_of_currently_selected_beat()
        self.current_sequence_json_handler.update_turns_in_json_at_index(
            pictograph_index + 1, self.color, new_turns
        )

        self._update_turns_display(new_turns)
        self.json_validation_engine.run()
        self.main_widget.builder_toolbar.sequence_builder.option_picker.update_option_picker()
        self.turns_adjusted.emit(new_turns)

    def get_current_turns_value(self) -> Turns:
        return self._get_turns()

    def _get_turns(self) -> Turns:
        turns = self.turns_widget.display_manager.turns_display_label.text()
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

    def _update_motion_properties(self, new_turns) -> None:
        self.pictograph = self.graph_editor.GE_pictograph_view.get_current_pictograph()
        for motion in self.pictograph.motions.values():
            if motion.color == self.turns_widget.turns_box.color:
                self.turns_widget.updater.set_motion_turns(motion, new_turns)
