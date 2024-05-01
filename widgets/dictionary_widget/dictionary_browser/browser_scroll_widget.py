import os
from typing import TYPE_CHECKING
from PyQt6.QtCore import QSize, Qt
from path_helpers import get_images_and_data_path
from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QGridLayout,
    QPushButton,
    QStyle,
)

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )

    pass


class DictionaryBrowserScrollWidget(QWidget):
    def __init__(self, browser: "DictionaryBrowser"):
        super().__init__(browser)
        self.browser = browser

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_content.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.scroll_content)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.scroll_area)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background: transparent;")
        self.thumbnail_boxes: list[ThumbnailBox] = []
        self.load_base_words()

    def _remove_spacing(self):
        self.grid_layout.setSpacing(0)
        self.layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_content.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def load_base_words(self):
        dictionary_dir = get_images_and_data_path("dictionary")
        if not os.path.exists(dictionary_dir):
            os.makedirs(dictionary_dir)
        base_words = sorted(
            (
                d
                for d in os.listdir(dictionary_dir)
                if os.path.isdir(os.path.join(dictionary_dir, d))
            ),
            key=lambda x: x.lower(),  # Sorting by the base word alphabetically
        )

        self.clear_layout()
        for i, word in enumerate(base_words):
            thumbnails = self.find_thumbnails(os.path.join(dictionary_dir, word))
            thumbnail_box = ThumbnailBox(self.browser, word, thumbnails)
            row, col = divmod(i, 3)  # Assuming 3 columns layout
            self.grid_layout.addWidget(thumbnail_box, row, col)
            self.thumbnail_boxes.append(thumbnail_box)

    def clear_layout(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

    def find_thumbnails(self, word_dir: str):
        thumbnails = []
        for root, _, files in os.walk(word_dir):
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg")):
                    thumbnails.append(os.path.join(root, file))
        return thumbnails

    def show_variations(self, base_word):
        print(f"Show variations for {base_word}")

    def get_scrollbar_width(self):
        style = self.scroll_area.style()
        return style.pixelMetric(QStyle.PixelMetric.PM_ScrollBarExtent)

    def add_new_thumbnail_box(self, new_word, thumbnails):
        # Find the right position based on alphabetical order
        index = next(
            (
                i
                for i, box in enumerate(self.thumbnail_boxes)
                if box.base_word.lower() > new_word.lower()
            ),
            len(self.thumbnail_boxes),
        )

        # Create new ThumbnailBox
        thumbnail_box = ThumbnailBox(self.browser, new_word, thumbnails)
        row, col = divmod(index, 3)
        self.grid_layout.addWidget(thumbnail_box, row, col)
        self.thumbnail_boxes.insert(index, thumbnail_box)

        # Adjust positions of subsequent thumbnail boxes if necessary
        for i in range(index + 1, len(self.thumbnail_boxes)):
            row, col = divmod(i, 3)
            self.grid_layout.addWidget(self.thumbnail_boxes[i], row, col)

    def resize_dictionary_browser_scroll_area(self):
        scrollbar_width = (
            self.scroll_area.verticalScrollBar().isVisible()
            * self.scroll_area.verticalScrollBar().width()
        )
        parent_width = self.scroll_area.viewport().width() - scrollbar_width
        max_width = parent_width // 3
        for box in self.thumbnail_boxes:
            box.setMaximumWidth(max_width)
            box.setMaximumHeight(max_width)
            box.image_label.update_thumbnail()