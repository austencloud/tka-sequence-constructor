from typing import TYPE_CHECKING
from .currently_displaying_indicator_label import CurrentlyDisplayingIndicatorLabel
from .dictionary_browser_nav_sidebar import DictionaryBrowserNavSidebar
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from .dictionary_browser_section_manager import SectionManager

from .dictionary_initial_selections_widget.dictionary_initial_selections_widget import (
    DictionaryInitialSelectionsWidget,
)
from .thumbnail_box_sorter import ThumbnailBoxSorter
from .dictionary_browser_scroll_widget import DictionaryBrowserScrollWidget
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from .options_panel.dictionary_browser_options_panel import DictionaryOptionsPanel
from PyQt6.QtWidgets import QLabel

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_widget import DictionaryWidget


class DictionaryBrowser(QWidget):
    def __init__(self, dictionary_widget: "DictionaryWidget") -> None:
        super().__init__(dictionary_widget)
        self.dictionary_widget = dictionary_widget
        self.main_widget = dictionary_widget.main_widget
        self.initialized = False
        self.currently_displayed_sequences = []
        self.num_columns = 3
        self.sections: dict[str, list[tuple[str, list[str]]]] = {}

        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        self.setup_components()
        self.initial_selection_widget = DictionaryInitialSelectionsWidget(self)

    def setup_components(self):
        self.currently_displaying_label = CurrentlyDisplayingIndicatorLabel(self)
        self.nav_sidebar = DictionaryBrowserNavSidebar(self)
        self.scroll_widget = DictionaryBrowserScrollWidget(self)
        self.section_manager = SectionManager(self)
        self.thumbnail_box_sorter = ThumbnailBoxSorter(self)
        self.options_widget = DictionaryOptionsPanel(self)

        self._setup_go_back_to_initial_selection_widget_button()
        self._setup_number_of_currently_displayed_sequences_label()
        self.widgets: list[QWidget] = [
            self.nav_sidebar,
            self.scroll_widget,
            self.options_widget,
            self.go_back_button,
            self.currently_displaying_label,
            self.number_of_currently_displayed_words_label,
        ]
        for widget in self.widgets:
            widget.hide()

    def _setup_number_of_currently_displayed_sequences_label(self):
        self.number_of_currently_displayed_words_label = QLabel("")
        self.number_of_currently_displayed_words_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

    def _setup_go_back_to_initial_selection_widget_button(self):
        self.go_back_button = QPushButton("Go Back")
        self.go_back_button_layout = QHBoxLayout()
        self.go_back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.go_back_button_layout.addWidget(self.go_back_button)
        self.go_back_button_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.go_back_button.clicked.connect(self.go_back_to_initial_selection_widget)

    def go_back_to_initial_selection_widget(self):
        self.initial_selection_widget.show()
        for widget in self.widgets:
            widget.hide()
        # hide the preview_area
        self.dictionary_widget.preview_area.hide()
        # clear the dictionary preview area
        self.dictionary_widget.preview_area.clear_preview()
        # hide the number of currently displayed sequences label
        self.number_of_currently_displayed_words_label.hide()

    def showEvent(self, event):
        super().showEvent(event)
        if not self.initialized:
            sort_method = (
                self.main_widget.main_window.settings_manager.dictionary.get_sort_method()
            )
            timer = QTimer(self)
            self.add_initial_selection_widget()

    def add_initial_selection_widget(self):
        self.layout.addWidget(self.initial_selection_widget)

    def show_all_sequences(self):
        self.apply_initial_selection({"letter": "Show all"})

    def apply_initial_selection(self, initial_selections):
        # set override cursor
        # QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        # hide the buttons in the nav button widget
        self.initial_selection_widget.hide()
        self._add_components_to_layout()
        QApplication.processEvents()
        # self.thummbnail_box_sorter.currently_displayed_sequences = []  # Reset before applying new filters
        self._initialize_and_sort_thumbnails(initial_selections)
        # QApplication.restoreOverrideCursor()

    def _initialize_and_sort_thumbnails(self, sort_method):
        self.thumbnail_box_sorter.sort_and_display_thumbnail_boxes_by_initial_selection(
            sort_method
        )
        self.initialized = True

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.scroll_widget_container = QWidget()
        self.scroll_layout = QHBoxLayout(self.scroll_widget_container)

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

    def _add_components_to_layout(self):

        self.layout.addLayout(self.go_back_button_layout)
        self.layout.addWidget(self.currently_displaying_label)
        self.layout.addWidget(self.number_of_currently_displayed_words_label)
        self.layout.addWidget(self.options_widget)
        self.layout.addWidget(self.scroll_widget)
        self.scroll_layout.addWidget(self.nav_sidebar, 1)
        self.scroll_layout.addWidget(self.scroll_widget, 9)
        self.layout.addWidget(self.scroll_widget_container)
        self.dictionary_widget.layout.addWidget(self.dictionary_widget.preview_area, 3)
        for widget in self.widgets:
            widget.show()
        self.dictionary_widget.preview_area.show()
        self.resize_currently_displaying_label()
        self.resize_number_of_currently_displayed_sequences_label()

    def resize_dictionary_browser(self):
        self.scroll_widget.resize_dictionary_browser_scroll_widget()
        self.resize_go_back_button()
        self.resize_currently_displaying_label()
        self.resize_number_of_currently_displayed_sequences_label()
        self.initial_selection_widget.resize_initial_selections_widget()

    def resize_number_of_currently_displayed_sequences_label(self):
        font = self.number_of_currently_displayed_words_label.font()
        font.setPointSize(self.width() // 80)
        self.number_of_currently_displayed_words_label.setFont(font)

    def resize_go_back_button(self):
        font = QFont()
        font.setPointSize(self.width() // 120)
        self.go_back_button.setFont(font)
        self.go_back_button.setFixedWidth(self.width() // 10)

    def resize_currently_displaying_label(self):
        font = self.currently_displaying_label.font()
        font.setPointSize(self.width() // 65)
        self.currently_displaying_label.setFont(font)

    def display_filtered_sequences(self, filtered_sequences):
        """Display sequences based on the filtered criteria."""
        self.scroll_widget.clear_layout()

        num_columns = 3
        row_index = 0
        column_index = 0

        for metadata_and_thumbnail in filtered_sequences:
            metadata = metadata_and_thumbnail["metadata"]
            thumbnail = metadata_and_thumbnail["thumbnail"]
            word = metadata["sequence"][0]["word"]

            self.thumbnail_box_sorter.add_thumbnail_box(
                row_index, column_index, word, [thumbnail]
            )

            column_index += 1
            if column_index == num_columns:
                column_index = 0
                row_index += 1

    def reset_filters(self):
        """Reset filters and display all sequences."""
        self._initialize_and_sort_thumbnails(
            self.main_widget.main_window.settings_manager.dictionary.get_sort_method()
        )
