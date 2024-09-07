from typing import TYPE_CHECKING

from main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.beat import (
    BeatView,
)
from main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.start_pos_beat import (
    StartPositionBeatView,
)


if TYPE_CHECKING:
    from .sequence_widget_beat_frame import SequenceWidgetBeatFrame


class BeatDeletionManager:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame") -> None:
        self.beat_frame = beat_frame
        self.manual_builder = None
        self.selection_overlay = self.beat_frame.selection_overlay
        self.json_manager = self.beat_frame.json_manager  # Access json manager
        self.settings_manager = self.beat_frame.settings_manager

    def delete_selected_beat(self) -> None:
        self.beats = self.beat_frame.beats
        if not self.manual_builder:
            self.manual_builder = (
                self.beat_frame.main_widget.top_builder_widget.sequence_builder.manual_builder
            )
        self.GE_pictograph_view = (
            self.beat_frame.main_widget.top_builder_widget.sequence_widget.graph_editor.pictograph_container.GE_pictograph_view
        )
        selected_beat = self.beat_frame.selection_overlay.get_selected_beat()

        if selected_beat.__class__ == StartPositionBeatView:
            self._delete_start_pos()
        elif selected_beat == self.beats[0]:
            self._delete_first_beat(selected_beat)
        else:
            self._delete_non_first_beat(selected_beat)

        self.json_manager.updater.clear_and_repopulate_the_current_sequence()
        if self.settings_manager.global_settings.get_grow_sequence():
            self.beat_frame.adjust_layout_to_sequence_length()
        self.beat_frame.sequence_widget.update_current_word()

        # QApplication.processEvents()
        self.manual_builder.option_picker.update_option_picker()

    def _delete_non_first_beat(self, selected_beat):
        self.delete_beat(selected_beat)
        for i in range(self.beats.index(selected_beat), len(self.beats)):
            self.delete_beat(self.beats[i])
        last_beat = self.beat_frame.get_last_filled_beat()
        self.selection_overlay.select_beat(last_beat)
        self.manual_builder.last_beat = last_beat.beat

    def _delete_first_beat(self, selected_beat):
        self.start_pos_view = self.beat_frame.start_pos_view
        self.selection_overlay.select_beat(self.start_pos_view)
        self.manual_builder.last_beat = self.start_pos_view.beat
        self.delete_beat(selected_beat)

        for i in range(
            self.beats.index(selected_beat) + 1,
            len(self.beats),
        ):
            self.delete_beat(self.beats[i])

        self.sequence_widget = (
            self.beat_frame.main_widget.top_builder_widget.sequence_widget
        )
        self.sequence_widget.difficulty_label.set_difficulty_level("")

    def _delete_start_pos(self):
        self.start_pos_view = self.beat_frame.start_pos_view
        self.start_pos_view.setScene(self.start_pos_view.blank_beat)
        self.start_pos_view.is_filled = False
        self.GE_pictograph_view.set_to_blank_grid()
        for beat in self.beats:
            self.delete_beat(beat)
        self.selection_overlay.deselect_beat()
        self.json_manager.loader_saver.clear_current_sequence_file()
        self.manual_builder.last_beat = None
        self.manual_builder.reset_to_start_pos_picker()
        self.manual_builder.option_picker.update_option_picker()
        graph_editor = (
            self.beat_frame.main_widget.top_builder_widget.sequence_widget.graph_editor
        )
        graph_editor.adjustment_panel.update_adjustment_panel()

    def delete_beat(self, beat_view: BeatView) -> None:
        beat_view.setScene(beat_view.blank_beat)
        beat_view.is_filled = False
