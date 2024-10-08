from PyQt6.QtCore import QObject, pyqtSignal
from data.constants import END_POS, START_POS
from typing import TYPE_CHECKING

from base_widgets.base_pictograph.base_pictograph import BasePictograph


if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_builder.option_picker.option_picker import (
        OptionPicker,
    )


class OptionGetter(QObject):
    option_selected = pyqtSignal(BasePictograph)

    def __init__(self, option_picker: "OptionPicker"):
        super().__init__()
        self.manual_builder = option_picker.manual_builder
        self.main_widget = option_picker.main_widget
        self.start_options: dict[str, BasePictograph] = {}

    def get_next_options(self, sequence) -> list[dict]:
        next_options = []

        last_pictograph_dict = (
            sequence[-1]
            if sequence[-1].get("is_placeholder", "") != True
            else sequence[-2]
        )
        start_pos = last_pictograph_dict[END_POS]

        if start_pos:
            for dict_list in self.main_widget.pictograph_dicts.values():
                for dict in dict_list:
                    if dict[START_POS] == start_pos:
                        next_options.append(dict)

        return next_options
