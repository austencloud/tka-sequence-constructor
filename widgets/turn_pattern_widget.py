import json
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QListWidgetItem,
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QInputDialog

from path_helpers import resource_path
from widgets.turn_pattern_converter import TurnPatternConverter

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_modifier import SequenceModifier


class TurnPatternWidget(QWidget):
    def __init__(self, sequence_modifier: "SequenceModifier"):
        super().__init__()
        self.sequence_modifier = sequence_modifier
        self.main_widget = sequence_modifier.main_widget
        self.current_sequence_json_handler = (
            self.sequence_modifier.main_widget.json_manager.current_sequence_json_handler
        )
        self._setup_ui()
        self.load_turn_patterns()
        self.apply_button.clicked.connect(self.apply_turn_pattern)
        self.save_button.clicked.connect(self.save_turn_pattern)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        self.turn_pattern_list = QListWidget()
        self.apply_button = QPushButton("Apply Turn Pattern")
        self.save_button = QPushButton("Save Current Turn Pattern")
        layout.addWidget(self.turn_pattern_list)
        layout.addWidget(self.apply_button)
        layout.addWidget(self.save_button)
        self.turn_pattern_list.itemDoubleClicked.connect(self.apply_turn_pattern)

    def load_turn_patterns(self) -> None:
        turn_patterns_path = resource_path("turn_patterns.json")
        try:
            with open(turn_patterns_path, "r") as file:
                patterns = json.load(file)
                self.turn_pattern_list.clear()
                for pattern_dict in patterns:
                    for name, pattern in pattern_dict.items():
                        item = QListWidgetItem(f"{name}: {pattern}")
                        item.setData(Qt.ItemDataRole.UserRole, pattern)
                        self.turn_pattern_list.addItem(item)
        except FileNotFoundError:
            print("Turn patterns file not found. Starting with an empty list.")

    def save_turn_pattern(self) -> None:
        current_pattern = self.get_current_turn_pattern()
        pattern_name, ok = QInputDialog.getText(
            self, "Save Pattern", "Enter pattern name:"
        )
        if ok:
            # if the user did not enter a name, then assign one
            if not pattern_name:
                pattern_name = "Pattern " + str(self.turn_pattern_list.count() + 1)

            new_pattern = {pattern_name: current_pattern}

            patterns = []
            try:
                with open("turn_patterns.json", "r") as file:
                    patterns = json.load(file)
            except FileNotFoundError:
                pass

            patterns.append(new_pattern)

            with open("turn_patterns.json", "w") as file:
                json.dump(patterns, file, indent=4)

            self.load_turn_patterns()



    def get_current_turn_pattern(self) -> str:
        sequence = self.current_sequence_json_handler.load_current_sequence_json()
        pattern = TurnPatternConverter.sequence_to_pattern(sequence)
        return pattern

    def apply_turn_pattern(self) -> None:
        selected_items = self.turn_pattern_list.selectedItems()
        if not selected_items:
            return
        pattern_str = selected_items[0].data(Qt.ItemDataRole.UserRole)
        self.current_sequence_json_handler.apply_turn_pattern_to_current_sequence(
            TurnPatternConverter.pattern_to_sequence(pattern_str)
        )