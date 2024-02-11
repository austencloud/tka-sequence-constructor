from typing import TYPE_CHECKING, Union
from Enums import LetterType
from utilities.TypeChecking.TypeChecking import Letters


from constants import (
    BLUE_END_LOC,
    BLUE_MOTION_TYPE,
    BLUE_PROP_ROT_DIR,
    BLUE_START_LOC,
    END_POS,
    LETTER,
    RED_END_LOC,
    RED_MOTION_TYPE,
    RED_PROP_ROT_DIR,
    RED_START_LOC,
    START_POS,
)

from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.sequence_builder.components.option_picker.option_picker_scroll_area import (
        OptionPickerScrollArea,
    )
    from widgets.scroll_area.codex_scroll_area import CodexScrollArea


class ScrollAreaPictographFactory:
    def __init__(
        self,
        scroll_area: Union["CodexScrollArea", "OptionPickerScrollArea"],
        pictograph_cache: dict[str, Pictograph],
    ) -> None:
        self.scroll_area = scroll_area
        self.pictograph_cache = pictograph_cache

    def get_or_create_pictograph(
        self, pictograph_key: str, pictograph_dict=None
    ) -> Pictograph:
        letter = pictograph_key.split("_")[0]

        if pictograph_key in self.pictograph_cache.get(letter, {}):
            return self.pictograph_cache[letter][pictograph_key]

        if pictograph_dict is not None:
            pictograph = self.create_pictograph()
            pictograph.updater.update_pictograph(pictograph_dict)

            if letter not in self.pictograph_cache:
                self.pictograph_cache[letter] = {}
            self.pictograph_cache[letter][pictograph_key] = pictograph
            self.scroll_area.main_widget.all_pictographs[pictograph_key] = pictograph
            letter_type = LetterType.get_letter_type(letter)
            for letter_type in LetterType:
                if letter in letter_type.letters:
                    letter_type = letter_type
                    break
            section = self.scroll_area.sections_manager.get_section(letter_type)
            section.pictographs[pictograph_key] = pictograph

            return pictograph

        raise ValueError("Pictograph dict is required for creating a new pictograph.")

    def process_selected_letters(self) -> None:
        selected_letters = set(self.scroll_area.codex.selected_letters)
        for letter in selected_letters:
            if str(letter) not in self.scroll_area.codex.pictograph_cache:
                pictograph_dicts = self.scroll_area.letters.get(letter, [])
                for pictograph_dict in pictograph_dicts:
                    pictograph_key = self.generate_pictograph_key_from_dict(
                        pictograph_dict
                    )
                    self.get_or_create_pictograph(pictograph_key, pictograph_dict)
            for (
                pictograph_key,
                pictograph,
            ) in self.scroll_area.codex.pictograph_cache[letter].items():
                self.scroll_area.pictograph_cache[pictograph_key] = pictograph

    def get_deselected_letters(self) -> set[Letters]:
        selected_letters = set(self.scroll_area.codex.selected_letters)
        existing_letters = {
            key.split("_")[0] for key in self.scroll_area.pictograph_cache.keys()
        }
        return existing_letters - selected_letters

    def remove_deselected_letter_pictographs(self, deselected_letter) -> None:
        keys_to_remove = [
            key
            for key in self.scroll_area.pictograph_cache
            if key.startswith(deselected_letter + "_")
        ]
        for key in keys_to_remove:
            pictograph = self.scroll_area.pictograph_cache.pop(key)
            pictograph.view.setParent(None)

    def get_pictograph(self, pictograph_key) -> Pictograph:
        return self.scroll_area.pictograph_cache[pictograph_key]

    def create_pictograph(self) -> Pictograph:
        pictograph = Pictograph(
            self.scroll_area.main_widget,
            self.scroll_area,
        )
        return pictograph

    def generate_pictograph_key_from_dict(self, pictograph_dict) -> str:
        return (
            f"{pictograph_dict[LETTER]}_"
            f"{pictograph_dict[START_POS]}→{pictograph_dict[END_POS]}_"
            f"{pictograph_dict[BLUE_MOTION_TYPE]}_"
            f"{pictograph_dict[BLUE_PROP_ROT_DIR]}_"
            f"{pictograph_dict[BLUE_START_LOC]}→{pictograph_dict[BLUE_END_LOC]}_"
            f"{pictograph_dict[RED_MOTION_TYPE]}_"
            f"{pictograph_dict[RED_PROP_ROT_DIR]}_"
            f"{pictograph_dict[RED_START_LOC]}→{pictograph_dict[RED_END_LOC]}"
        )
