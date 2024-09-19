from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QLabel,
    QGridLayout,
    QWidget,
)
from PyQt6.QtCore import Qt
from functools import partial
from .filter_section_base import FilterSectionBase

if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_browser.initial_filter_selection_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )


class SequenceLengthSection(FilterSectionBase):
    AVAILABLE_LENGTHS = [4, 6, 8, 10, 12, 16, 20, 24, 28, 32]

    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget, "Select by Sequence Length:")
        self.buttons: dict[int, QPushButton] = {}
        self.sequence_tally_labels: dict[int, QLabel] = {}
        self.spacer_labels: list[QLabel] = []
        self.grid_layout = QGridLayout()
        self.add_buttons()

    def add_buttons(self):
        self.back_button.show()
        self.header_label.show()
        layout: QVBoxLayout = self.layout()

        sequence_counts = self._get_sequence_length_counts()

        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        max_columns = 3  # Adjust this to control how many buttons are in one row
        row = col = 0

        # Clear existing labels and buttons dictionaries
        self.buttons.clear()
        self.sequence_tally_labels.clear()
        self.spacer_labels.clear()

        for length in self.AVAILABLE_LENGTHS:
            count = sequence_counts.get(length, 0)
            if count > 0:
                button = self.create_length_button(length)
                label = self.create_sequence_tally_label(length, count)

                # Add button and label to the grid
                self.grid_layout.addWidget(button, row * 3, col)
                self.grid_layout.addWidget(label, row * 3 + 1, col)

                col += 1
                if col >= max_columns:
                    col = 0
                    # Add a spacer between rows
                    spacer_label = QLabel()
                    self.spacer_labels.append(spacer_label)
                    self.grid_layout.addWidget(
                        spacer_label, row * 3 + 2, 0, 1, max_columns
                    )
                    row += 1

        # Handle the case where the last row isn't full
        if col != 0:
            # Add a spacer after the last row
            spacer_label = QLabel()
            self.spacer_labels.append(spacer_label)
            self.grid_layout.addWidget(spacer_label, row * 3 + 2, 0, 1, max_columns)

        layout.addStretch(1)
        layout.addLayout(self.grid_layout)
        layout.addStretch(1)
        self.resize_sequence_length_section()

    def create_length_button(self, length: int) -> QPushButton:
        """Create and configure a QPushButton for a given sequence length."""
        button = QPushButton(str(length))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.buttons[length] = button
        button.clicked.connect(
            partial(
                self.initial_selection_widget.on_length_button_clicked,
                length,
            )
        )
        return button

    def create_sequence_tally_label(self, length: int, count: int) -> QLabel:
        """Create a QLabel displaying the sequence count for a given length."""
        sequence_text = "sequence" if count == 1 else "sequences"
        label = QLabel(f"{count} {sequence_text}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sequence_tally_labels[length] = label
        return label

    def _get_sequence_length_counts(self) -> dict[int, int]:
        """Tally up how many sequences are available for each length."""
        length_counts = {}
        base_words = self.thumbnail_box_sorter.get_sorted_base_words("sequence_length")

        for _, _, seq_length in base_words:
            length_counts[seq_length] = length_counts.get(seq_length, 0) + 1

        return length_counts

    def display_only_thumbnails_with_sequence_length(self, length: int):
        """Display sequences of a specific length."""
        self.initial_selection_widget.browser.dictionary_widget.dictionary_settings.set_current_filter(
            {"sequence_length": length}
        )
        self.browser.prepare_ui_for_filtering(f"sequences of length {length}")

        base_words = self.thumbnail_box_sorter.get_sorted_base_words("sequence_length")
        matching_sequences = [
            (word, thumbnails, seq_length)
            for word, thumbnails, seq_length in base_words
            if seq_length == length
        ]

        total_sequences = len(matching_sequences) or 1  # Prevent division by zero
        self.browser.currently_displayed_sequences = matching_sequences

        self.browser.update_and_display_ui(total_sequences, length)

    def resize_sequence_length_section(self):
        self.resize_buttons()
        self.resize_widget_font(self.header_label, 100)
        self.resize_sequence_count_labels()
        self.set_grid_spacing()
        self.resize_spacers()

    def resize_widget_font(self, widget: QWidget, factor: int):
        font = widget.font()
        font.setPointSize(max(10, self.main_widget.width() // factor))
        widget.setFont(font)

    def resize_sequence_count_labels(self):
        for label in self.sequence_tally_labels.values():
            self.resize_widget_font(label, 120)

    def resize_buttons(self):
        width = self.main_widget.width() // 12
        height = self.main_widget.height() // 12
        font_size = max(10, self.main_widget.width() // 75)
        for button in self.buttons.values():
            font = button.font()
            font.setPointSize(font_size)
            button.setFont(font)
            button.setFixedSize(width, height)

    def set_grid_spacing(self):
        """Set the spacing in the grid layout to adjust the layout."""
        hor_spacing = self.main_widget.width() // 30
        vert_spacing = self.main_widget.height() // 200  # Minimal vertical spacing
        self.grid_layout.setHorizontalSpacing(hor_spacing)
        self.grid_layout.setVerticalSpacing(vert_spacing)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

    def resize_spacers(self):
        """Adjust the height of spacer labels during resizing."""
        spacer_height = self.main_widget.height() // 20
        for spacer_label in self.spacer_labels:
            spacer_label.setFixedHeight(spacer_height)