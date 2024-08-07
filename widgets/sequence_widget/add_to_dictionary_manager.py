import os
import re  # Ensure to import re at the top of your file

from typing import TYPE_CHECKING
from widgets.path_helpers.path_helpers import get_images_and_data_path
from widgets.sequence_widget.structural_variation_checker import (
    StructuralVariationChecker,
)
from widgets.sequence_widget.thumbnail_generator import ThumbnailGenerator
from widgets.sequence_widget.turn_pattern_variation_checker import (
    TurnPatternVariationChecker,
)
from widgets.turn_pattern_converter import TurnPatternConverter

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class AddToDictionaryManager:
    def __init__(self, sequence_widget: "SequenceWidget"):
        self.sequence_widget = sequence_widget
        self.json_manager = self.sequence_widget.main_widget.json_manager
        self.dictionary_dir = get_images_and_data_path("dictionary")
        self.structural_checker = StructuralVariationChecker(self)

    def add_to_dictionary(self):
        self.thumbnail_generator = ThumbnailGenerator(self)
        current_sequence = self.json_manager.loader_saver.load_current_sequence_json()
        if self.is_sequence_invalid(current_sequence):
            self.display_message(
                "You must build a sequence to add it to your dictionary."
            )
            return
        self.process_sequence(current_sequence)

    def process_sequence(self, current_sequence):
        base_word = self.sequence_widget.beat_frame.get_current_word()
        base_path = os.path.join(self.dictionary_dir, base_word)

        if self.structural_checker.check_for_structural_variation(
            current_sequence, base_word
        ):
            turn_variation_checker = TurnPatternVariationChecker(self, base_path)
            if turn_variation_checker.check_for_turn_pattern_variation(
                current_sequence
            ):
                self.display_message(
                    f"This exact turn pattern variation for {base_word} already exists."
                )
            else:
                variation_number = self.get_variation_number(base_word)
                self.save_variation(current_sequence, base_word, variation_number)
                self.display_message(
                    f"New turn pattern variation added to '{base_word}'."
                )

        else:
            variation_number = self.get_next_variation_number(base_word)
            self.save_variation(current_sequence, base_word, variation_number)
            self.display_message(
                f"New structural and turn pattern variation added to '{base_word}'."
            )

        self.refresh_ui()
        thumbnail_box = self.sequence_widget.main_widget.dictionary_widget.browser.scroll_widget.thumbnail_boxes_dict.get(
            base_word
        )
        if thumbnail_box:
            thumbnail_box.resize_thumbnail_box()

    def get_variation_number(self, base_word):
        base_path = os.path.join(self.dictionary_dir, base_word)
        max_number = 0
        for dir_name in os.listdir(base_path):
            if dir_name.startswith(f"{base_word}_ver"):
                try:
                    number_part = dir_name.split("_ver")[-1]
                    number = int(
                        "".join(filter(str.isdigit, number_part.split("_")[0]))
                    )
                    max_number = max(max_number, number)
                except ValueError:
                    continue
        return max_number

    def get_next_variation_number(self, base_word):
        base_path = os.path.join(self.dictionary_dir, base_word)
        existing_numbers = []
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if "ver" in file:
                    try:
                        number_part = re.search(r"_ver(\d+)", file)
                        if number_part:
                            number = int(number_part.group(1))
                            existing_numbers.append(number)
                    except ValueError:
                        continue
        return max(existing_numbers, default=0) + 1

    def get_start_orientations(self, sequence) -> str:
        start_pos_dict = sequence[1]
        if sequence and "sequence_start_position" in start_pos_dict:
            blue_ori = start_pos_dict["blue_attributes"].get("start_ori", "none")
            red_ori = start_pos_dict["red_attributes"].get("start_ori", "none")
            return f"({blue_ori},{red_ori})"
        return "none,none"

    def save_variation(self, sequence, base_word, variation_number):
        turn_pattern_description = TurnPatternConverter.sequence_to_pattern(sequence)
        start_orientations = self.get_start_orientations(sequence)
        directory = self.get_variation_directory(
            base_word, variation_number, start_orientations
        )
        self.thumbnail_generator.generate_and_save_thumbnail(
            sequence, turn_pattern_description, variation_number, directory
        )
        self.display_message(
            f"Saved new variation for '{base_word}' under version {variation_number}."
        )

        thumbnails = self.collect_thumbnails(base_word)
        thumbnail_box = self.find_thumbnail_box(base_word)
        if thumbnail_box:
            thumbnail_box.update_thumbnails(thumbnails)
        self.display_message(f"Saved new variation for '{base_word}'.")

    def collect_thumbnails(self, base_word):
        base_path = os.path.join(self.dictionary_dir, base_word)
        thumbnails = []
        for root, dirs, files in os.walk(base_path):
            for filename in files:
                if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                    thumbnails.append(os.path.join(root, filename))
        return thumbnails

    def find_thumbnail_box(self, base_word):
        return self.sequence_widget.main_widget.dictionary_widget.browser.scroll_widget.thumbnail_boxes_dict.get(
            base_word
        )

    def get_variation_directory(
        self, base_word, variation_number, start_orientations: str
    ) -> str:
        base_dir = os.path.join(
            self.dictionary_dir, f"{base_word}", f"{base_word}_ver{variation_number}"
        )
        orientation_dir = start_orientations.replace(" ", "").replace(",", "_")
        master_dir = os.path.join(base_dir, orientation_dir)
        os.makedirs(master_dir, exist_ok=True)
        return master_dir

    def display_message(self, message):
        self.sequence_widget.indicator_label.show_message(message)

    def refresh_ui(self):
        self.sequence_widget.main_widget.dictionary_widget.browser.sorter.sort_and_display_thumbnails(
            self.sequence_widget.main_widget.main_window.settings_manager.dictionary.get_sort_method()
        )

    def get_base_word(self, sequence):
        base_sequence = []
        for entry in sequence:
            base_entry = entry.copy()
            base_sequence.append(base_entry)

        revalidated_sequence = self.revalidate_sequence(base_sequence)
        base_word = "".join(item.get("letter", "") for item in revalidated_sequence)
        base_word = base_word[1:]
        return base_word

    def revalidate_sequence(self, sequence):
        if not hasattr(self, "validation_engine"):
            self.validation_engine = self.json_manager.validation_engine
        self.validation_engine.sequence = sequence
        self.validation_engine.run()
        return self.validation_engine.sequence

    def is_sequence_invalid(self, sequence):
        return len(sequence) <= 1
