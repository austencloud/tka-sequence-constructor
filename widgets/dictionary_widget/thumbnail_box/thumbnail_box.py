from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from widgets.dictionary_widget.thumbnail_box.metadata_extractor import MetaDataExtractor
from widgets.dictionary_widget.thumbnail_box.thumbnail_box_nav_btns import (
    ThumbnailBoxNavButtonsWidget,
)
from .base_word_label import BaseWordLabel
from .thumbnail_image_label import ThumbnailImageLabel
from .variation_number_label import VariationNumberLabel

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class ThumbnailBox(QWidget):
    def __init__(self, browser: "DictionaryBrowser", base_word, thumbnails) -> None:
        super().__init__(browser)
        self.margin = 10
        self.base_word = base_word
        self.thumbnails: list[str] = thumbnails
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
        self.metadata_extractor = MetaDataExtractor(self.main_widget)
        self.base_word_label = BaseWordLabel(self)
        self.image_label = ThumbnailImageLabel(self)
        self.variation_number_label = VariationNumberLabel(self)
        self.nav_buttons_widget = ThumbnailBoxNavButtonsWidget(self)

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addStretch()
        self.layout.addWidget(self.base_word_label)
        self.layout.addWidget(self.variation_number_label)
        self.layout.addWidget(
            self.image_label,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        self.layout.addWidget(self.nav_buttons_widget)
        self.layout.addStretch()
        self.layout.setContentsMargins(
            self.margin, self.margin, self.margin, self.margin
        )
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")

    def resize_thumbnail_box(self):
        scrollbar_width = (
            self.browser.scroll_widget.scroll_area.verticalScrollBar().width()
        )
        parent_width = self.browser.scroll_widget.width() - scrollbar_width

        width = parent_width // 3
        self.setFixedWidth(width)
        self.image_label.update_thumbnail(self.current_index)
        self.base_word_label.resize_base_word_label()

    def update_thumbnails(self, thumbnails=[]):
        self.thumbnails = thumbnails
        self.nav_buttons_widget.thumbnails = thumbnails
        if self == self.browser.dictionary_widget.preview_area.current_thumbnail_box:
            self.browser.dictionary_widget.preview_area.update_thumbnails(
                self.thumbnails
            )
        self.image_label.thumbnails = thumbnails
        self.image_label.set_pixmap_to_fit(QPixmap(self.thumbnails[self.current_index]))
        if len(self.thumbnails) == 1:
            self.variation_number_label.hide()
        else:
            self.variation_number_label.update_index(self.current_index + 1)

    def refresh_ui(self):
        self.update_thumbnails(self.thumbnails)
