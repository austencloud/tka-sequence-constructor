from PyQt6.QtWidgets import QFrame, QHBoxLayout, QApplication
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from Enums.Enums import LetterType, Letter
from data.constants import BLUE_START_ORI, BLUE_TURNS, RED_START_ORI, RED_TURNS
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.top_builder_widget.sequence_builder.advanced_start_pos_picker.advanced_start_pos_picker import (
    AdvancedStartPosPicker,
)
from main_window.main_widget.top_builder_widget.sequence_builder.components.start_pos_picker.start_pos_picker import (
    StartPosPicker,
)

from main_window.main_widget.top_builder_widget.sequence_builder.add_to_sequence_manager import (
    AddToSequenceManager,
)
from main_window.main_widget.top_builder_widget.sequence_builder.option_picker.option_picker import (
    OptionPicker,
)
from main_window.main_widget.top_builder_widget.sequence_builder.option_picker.option_picker_click_handler import (
    OptionPickerClickHandler,
)

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_builder.sequence_builder import (
        SequenceBuilder,
    )
    from main_window.main_widget.main_widget import MainWidget


class ManualBuilder(QFrame):
    def __init__(self, sequence_builder_tab_widget: "SequenceBuilder") -> None:
        super().__init__(sequence_builder_tab_widget)
        self.sequence_builder = sequence_builder_tab_widget
        self.main_widget: "MainWidget" = sequence_builder_tab_widget.main_widget
        self.last_beat: BasePictograph = None
        self.json_manager = self.main_widget.json_manager
        self.start_position_picked = False
        self.pictograph_cache: dict[Letter, dict[str, BasePictograph]] = {
            letter: {} for letter in Letter
        }

        self.option_click_handler = OptionPickerClickHandler(self)
        self.start_pos_picker = StartPosPicker(self)
        self.option_picker = OptionPicker(self)
        self.add_to_sequence_manager = AddToSequenceManager(self)
        self.advanced_start_pos_picker = AdvancedStartPosPicker(self)

        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.start_pos_picker)
        self.layout().addWidget(self.advanced_start_pos_picker)
        self.advanced_start_pos_picker.hide()  # Initially hidden
        self.initialized = False

    def transition_to_sequence_building(self) -> None:
        self.start_position_picked = True
        self._hide_start_pos_picker()
        self._hide_advanced_start_pos_picker()
        self._show_option_picker()

    def transition_to_advanced_start_pos_picker(self) -> None:
        self._hide_start_pos_picker()
        self.show_advanced_start_pos_picker()

    def _hide_advanced_start_pos_picker(self) -> None:
        self.advanced_start_pos_picker.hide()
        self.layout().removeWidget(self.advanced_start_pos_picker)

    def _hide_start_pos_picker(self) -> None:
        self.start_pos_picker.hide()
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.layout().removeWidget(self.start_pos_picker)

    def show_advanced_start_pos_picker(self) -> None:
        self.start_pos_picker.hide()
        self.layout().addWidget(self.advanced_start_pos_picker)
        self.advanced_start_pos_picker.show()
        self.advanced_start_pos_picker.init_ui()
        self.advanced_start_pos_picker.advanced_start_pos_manager.set_all_orientations_to_in()
        self.advanced_start_pos_picker.resize_advanced_start_pos_picker()

    def _show_option_picker(self) -> None:
        self.layout().addWidget(self.option_picker)
        self.option_picker.show()
        self.option_picker.scroll_area.section_manager.show_all_sections()
        self.option_picker.update_option_picker()
        # self.option_picker.resize_option_picker()

    def render_and_store_pictograph(
        self, pictograph_dict: dict, sequence
    ) -> BasePictograph:
        pictograph_dict = self._add_turns_and_start_ori(pictograph_dict, sequence)
        letter_str = pictograph_dict["letter"]
        letter = Letter.get_letter(letter_str)
        letter_type = LetterType.get_letter_type(letter)
        pictograph_key = (
            self.main_widget.pictograph_key_generator.generate_pictograph_key(
                pictograph_dict
            )
        )

        scroll_area = self.option_picker.scroll_area
        if pictograph_key in scroll_area.pictograph_cache:
            return scroll_area.pictograph_cache[pictograph_key]

        new_pictograph = scroll_area.pictograph_factory.get_or_create_pictograph(
            pictograph_key, pictograph_dict
        )
        scroll_area.pictograph_cache[pictograph_key] = new_pictograph
        self.main_widget.pictograph_cache[new_pictograph.letter][
            pictograph_key
        ] = new_pictograph
        if pictograph_key not in self.pictograph_cache[letter]:
            self.pictograph_cache[letter][pictograph_key] = new_pictograph
        section = scroll_area.section_manager.get_section(letter_type)
        section.pictographs[pictograph_key] = new_pictograph
        scroll_area.pictograph_cache[pictograph_key] = new_pictograph
        return new_pictograph

    def _add_turns_and_start_ori(self, pictograph_dict, sequence):
        self.current_end_red_ori = self.json_manager.loader_saver.get_red_end_ori(
            sequence
        )
        self.current_end_blue_ori = self.json_manager.loader_saver.get_blue_end_ori(
            sequence
        )

        pictograph_dict["red_attributes"][RED_START_ORI] = self.current_end_red_ori
        pictograph_dict["blue_attributes"][BLUE_START_ORI] = self.current_end_blue_ori
        pictograph_dict[RED_TURNS] = 0
        pictograph_dict[BLUE_TURNS] = 0
        return pictograph_dict

    def reset_to_start_pos_picker(self) -> None:
        self.start_position_picked = False
        self.option_picker.hide()
        self.advanced_start_pos_picker.hide()
        self.layout().removeWidget(self.option_picker)
        self.layout().addWidget(self.start_pos_picker)
        self.start_pos_picker.show()
        self.start_pos_picker.resize_start_pos_picker()

    def  resize_manual_builder(self) -> None:
        self.start_pos_picker.resize_start_pos_picker()
        self.advanced_start_pos_picker.resize_advanced_start_pos_picker()
        self.option_picker.resize_option_picker()

    def get_last_added_pictograph(self, sequence):
        """Returns the last pictograph in the sequence. Assumes the sequence is not empty."""
        return sequence[-1]