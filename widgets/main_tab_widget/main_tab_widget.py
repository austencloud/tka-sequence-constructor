from typing import TYPE_CHECKING

from widgets.base_tab_widget import BaseTabWidget
from widgets.letterbook.letterbook import LetterBook
from widgets.dictionary.dictionary import Dictionary
from widgets.sequence_builder.sequence_builder import SequenceBuilder
from widgets.turn_pattern_widget import TurnPatternWidget

if TYPE_CHECKING:
    from ..main_widget.main_widget import MainWidget


class MainTabWidget(BaseTabWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.letterbook = LetterBook(main_widget)
        self.sequence_builder = SequenceBuilder(main_widget)
        self.dictionary = Dictionary(main_widget)
        self.turn_pattern_widget = TurnPatternWidget(self)
        self.tabs = [self.letterbook]
        self.addTab(self.sequence_builder, "Builder")
        self.addTab(self.letterbook, "LetterBook")
        self.addTab(self.dictionary, "Dictionary")
        self.addTab(self.turn_pattern_widget, "Turn Patterns")
        self.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self) -> None:

        current_tab = self.currentWidget()
        beat_frame = self.main_widget.top_builder_widget.sequence_widget.beat_frame
        if current_tab == self.sequence_builder:
            if beat_frame.start_pos_view.scene():
                if not self.sequence_builder.option_picker.isVisible():
                    self.sequence_builder.transition_to_sequence_building()
        self.resize_current_tab(current_tab)

    def resize_current_tab(self, current_tab) -> None:
        if current_tab == self.letterbook:
            self.letterbook.resize_letterbook()
        elif current_tab == self.sequence_builder:
            self.sequence_builder.resize_sequence_builder()
        elif current_tab == self.dictionary:
            self.dictionary.resize_dictionary()
