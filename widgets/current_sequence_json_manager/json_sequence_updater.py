from typing import TYPE_CHECKING, Union
from Enums.MotionAttributes import Color
from Enums.PropTypes import PropType
from widgets.sequence_widget.sequence_properties_checker import SequencePropertiesChecker
from data.constants import BLUE, DASH, NO_ROT, RED, STATIC
from widgets.sequence_widget.SW_beat_frame.beat import BeatView

if TYPE_CHECKING:
    from widgets.json_manager import JSON_Manager


class JsonSequenceUpdater:
    def __init__(self, manager: "JSON_Manager"):
        self.manager = manager

    def update_sequence_properties(self):
        sequence = self.manager.loader_saver.load_current_sequence_json()
        if len(sequence) > 1:
            checker = SequencePropertiesChecker(sequence[1:])
            properties = checker.check_properties()

            # Update the sequence properties in the JSON
            sequence[0]["is_circular"] = properties["is_circular"]
            sequence[0]["is_permutable"] = properties["is_permutable"]
            sequence[0]["is_rotational_permutation"] = properties["is_rotational_permutation"]
            sequence[0]["is_mirrored_permutation"] = properties["is_mirrored_permutation"]
            sequence[0]["is_colorswapped_permutation"] = properties["is_colorswapped_permutation"]

            # Save the updated sequence back to the JSON
            self.manager.loader_saver.save_current_sequence(sequence)

    def update_prop_type_in_json(self, prop_type: PropType) -> None:
        sequence = self.manager.loader_saver.load_current_sequence_json()
        sequence[0]["prop_type"] = prop_type.name.lower()
        self.manager.loader_saver.save_current_sequence(sequence)

    def update_turns_in_json_at_index(
        self, index: int, color: Color, turns: Union[int, float]
    ) -> None:
        sequence = self.manager.loader_saver.load_current_sequence_json()
        sequence[index][f"{color}_attributes"]["turns"] = turns
        end_ori = self.manager.ori_calculator.calculate_end_orientation(
            sequence[index], color
        )
        sequence[index][f"{color}_attributes"]["end_ori"] = end_ori

        if sequence[index][f"{color}_attributes"]["turns"] > 0:
            pictograph = self.manager.main_widget.top_builder_widget.sequence_widget.beat_frame.beats[
                index - 2
            ].beat
            if pictograph:
                motion = pictograph.get.motion_by_color(color)
                prop_rot_dir = motion.prop_rot_dir
                sequence[index][f"{color}_attributes"]["prop_rot_dir"] = prop_rot_dir

        if sequence[index][f"{color}_attributes"]["motion_type"] in [DASH, STATIC]:
            if sequence[index][f"{color}_attributes"]["turns"] == 0:
                prop_rot_dir = NO_ROT
                sequence[index][f"{color}_attributes"]["prop_rot_dir"] = prop_rot_dir

        self.manager.loader_saver.save_current_sequence(sequence)

    def update_rot_dir_in_json_at_index(
        self, index: int, color: Color, prop_rot_dir: str
    ) -> None:
        sequence = self.manager.loader_saver.load_current_sequence_json()
        sequence[index][f"{color}_attributes"]["prop_rot_dir"] = prop_rot_dir
        self.manager.loader_saver.save_current_sequence(sequence)

    def apply_turn_pattern_to_current_sequence(self, pattern: list[tuple]) -> None:
        sequence = self.manager.loader_saver.load_current_sequence_json()
        min_length = min(len(sequence), len(pattern))
        for i in range(1, min_length + 1):
            if i == 17:
                continue
            blue_turns, red_turns = pattern[i - 1]
            blue_turns = int(blue_turns) if blue_turns.is_integer() else blue_turns
            red_turns = int(red_turns) if red_turns.is_integer() else red_turns

            if i >= len(sequence):
                break

            entry = sequence[i]
            entry["blue_attributes"]["turns"] = blue_turns
            entry["red_attributes"]["turns"] = red_turns

            if entry["blue_attributes"]["motion_type"] in [STATIC, DASH]:
                if not blue_turns == 0:
                    entry["blue_attributes"]["prop_rot_dir"] = (
                        self._calculate_continuous_prop_rot_dir(sequence, i, BLUE)
                    )
            if entry["red_attributes"]["motion_type"] in [STATIC, DASH]:
                if not red_turns == 0:
                    entry["red_attributes"]["prop_rot_dir"] = (
                        self._calculate_continuous_prop_rot_dir(sequence, i, RED)
                    )

            beat_view = self.manager.main_widget.top_builder_widget.sequence_widget.beat_frame.beats[
                i - 1
            ]
            if beat_view and beat_view.is_filled:
                beat_view.beat.get.pictograph_dict().update(entry)

        self.manager.loader_saver.save_current_sequence(sequence)
        self.manager.validation_engine.run(is_current_sequence=True)
        sequence = self.manager.loader_saver.load_current_sequence_json()
        self.manager.main_widget.top_builder_widget.sequence_widget.beat_frame.propogate_turn_adjustment(
            sequence
        )

    def _calculate_continuous_prop_rot_dir(self, sequence, current_index, color) -> str:
        ignore_motion_types = [STATIC, DASH]

        for i in range(current_index - 1, max(current_index - 16, -1), -1):
            if i == 0:
                continue
            if (
                sequence[i][f"{color}_attributes"]["motion_type"]
                not in ignore_motion_types
            ):
                return sequence[i][f"{color}_attributes"]["prop_rot_dir"]

        return NO_ROT

    def update_current_sequence_file_with_beat(self, beat_view: BeatView):
        sequence_data = self.manager.loader_saver.load_current_sequence_json()
        if len(sequence_data) == 0:  # Make sure there's at least the metadata entry
            sequence_data.append(
                {
                    "prop_type": self.manager.main_widget.prop_type.name.lower(),
                    "is_circular": False,
                }
            )
        sequence_data.append(beat_view.beat.pictograph_dict)
        self.manager.loader_saver.save_current_sequence(sequence_data)
        self.update_sequence_properties()  # Recalculate properties after each update
        self.manager.main_widget.main_window.settings_manager.save_settings()  # Save state on change

    def clear_and_repopulate_the_current_sequence(self):
        self.manager.loader_saver.clear_current_sequence_file()
        beat_frame = (
            self.manager.main_widget.top_builder_widget.sequence_widget.beat_frame
        )
        beat_views = beat_frame.beats
        start_pos = beat_frame.start_pos_view.start_pos
        if start_pos.view.is_filled:
            self.manager.start_position_handler.set_start_position_data(start_pos)
        for beat_view in beat_views:
            if beat_view.is_filled:
                self.update_current_sequence_file_with_beat(beat_view)
        self.manager.main_widget.main_window.settings_manager.save_settings()  # Save state on change
