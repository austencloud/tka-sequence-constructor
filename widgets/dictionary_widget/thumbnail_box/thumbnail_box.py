from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShowEvent, QResizeEvent
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from widgets.dictionary_widget.thumbnail_box.metadata_extractor import MetaDataExtractor
from .base_word_label import BaseWordLabel
from .navigation_buttons_widget import ThumbnailBoxNavButtonsWidget
from .thumbnail_image_label import ThumbnailImageLabel
from .variation_number_label import VariationNumberLabel

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class ThumbnailBox(QWidget):
    def __init__(self, browser: "DictionaryBrowser", base_word, thumbnails) -> None:
        super().__init__(browser)

        self.base_word = base_word
        self.thumbnails = thumbnails
        self.browser = browser
        self.main_widget = browser.dictionary_widget.main_widget
        self.initial_size_set = False
        self.current_index = 0
        self.browser = browser
        self.setContentsMargins(0, 0, 0, 0)
        self._setup_components()
        self._setup_layout()
        self.layout.setSpacing(0)

    def _setup_components(self):
        # Component setup remains unchanged
        self.metadata_extractor = MetaDataExtractor(self)
        self.base_word_label = BaseWordLabel(self)
        self.image_label = ThumbnailImageLabel(self)
        self.variation_number_label = VariationNumberLabel(self)
        self.navigation_buttons = ThumbnailBoxNavButtonsWidget(self)

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.base_word_label, 1)
        self.layout.addWidget(self.variation_number_label, 1)
        self.layout.addWidget(
            self.image_label,
            16,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        self.layout.addWidget(self.navigation_buttons, 1)
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")

    def resize_thumbnail_box(self):
        # Calculate available width considering scrollbar presence
        scrollbar_width = (
            self.browser.scroll_widget.scroll_area.verticalScrollBar().isVisible()
            * self.browser.scroll_widget.scroll_area.verticalScrollBar().width()
        )
        parent_width = self.browser.width() - scrollbar_width

        # Calculate the width for each thumbnail box
        max_width = parent_width // 3
        self.setMaximumWidth(max_width)
        self.setMinimumHeight(max_width)
        self.setMaximumHeight(max_width)  # Keep aspect ratio square or as needed
        self.image_label.update_thumbnail()