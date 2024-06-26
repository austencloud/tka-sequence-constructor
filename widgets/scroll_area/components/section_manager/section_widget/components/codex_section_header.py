from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QFrame
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap
from widgets.scroll_area.components.section_manager.section_widget.components.type_label import (
    SectionTypeLabel,
)

if TYPE_CHECKING:
    from widgets.scroll_area.components.section_manager.section_widget.letterbook_section_widget import (
        LetterBookSectionWidget,
    )


class LetterBookSectionHeader(QWidget):
    clicked = pyqtSignal()
    EXPAND_ARROW_PATH = "images/icons/dropdown/expand.png"
    COLLAPSE_ARROW_PATH = "images/icons/dropdown/collapse.png"

    def __init__(self, section: "LetterBookSectionWidget") -> None:
        super().__init__()
        self.section = section
        self.type_label = SectionTypeLabel(section)
        self._setup_arrow_label()
        self._setup_frames()
        self._setup_layout()

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addWidget(self.main_frame)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

    def _setup_arrow_label(self):
        self.arrow_label = QLabel()
        self.arrow_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.arrow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.expand_arrow_pixmap = self.load_and_resize_pixmap(self.EXPAND_ARROW_PATH)
        self.collapse_arrow_pixmap = self.load_and_resize_pixmap(
            self.COLLAPSE_ARROW_PATH
        )
        self.toggle_dropdown_arrow(False)

    def _setup_frames(self) -> None:
        self._setup_left_frame()
        self._setup_middle_frame()
        self._setup_right_frame()
        self._setup_main_frame()
        self._set_frame_sizes()

    def _setup_main_frame(self):
        self.main_frame = QFrame()
        self.main_frame.layout = QHBoxLayout(self.main_frame)
        self.main_frame.layout.addStretch(10)
        self.main_frame.layout.addWidget(self.left_frame)
        self.main_frame.layout.addStretch(1)
        self.main_frame.layout.addWidget(self.middle_frame)
        self.main_frame.layout.addStretch(1)
        self.main_frame.layout.addWidget(self.right_frame)
        self.main_frame.layout.addStretch(10)
        self.main_frame.setContentsMargins(0, 0, 0, 0)
        self.main_frame.layout.setContentsMargins(0, 0, 0, 0)

    def _setup_left_frame(self) -> None:
        self.left_frame = QWidget()
        left_layout = QHBoxLayout(self.left_frame)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.section.vtg_dir_button_manager.opp_button)

    def _setup_middle_frame(self) -> None:
        self.middle_frame = QWidget()
        middle_layout = QHBoxLayout(self.middle_frame)
        middle_layout.setContentsMargins(0, 0, 0, 0)
        middle_layout.addWidget(self.type_label)
        middle_layout.addStretch(2)
        middle_layout.addWidget(self.arrow_label)

    def _setup_right_frame(self) -> None:
        self.right_frame = QWidget()
        right_layout = QHBoxLayout(self.right_frame)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(self.section.vtg_dir_button_manager.same_button)

    def _set_frame_sizes(self) -> None:
        button_size = self.section.scroll_area.width() // 30
        self.left_frame.setFixedWidth(button_size)
        self.left_frame.setFixedHeight(button_size)
        self.right_frame.setFixedWidth(button_size)
        self.right_frame.setFixedHeight(button_size)
        self.setMaximumHeight(button_size)

    def load_and_resize_pixmap(self, path: str) -> QPixmap:
        pixmap = QPixmap(path)
        base_class_name = type(self.section.scroll_area).__name__
        if base_class_name == "LetterBookScrollArea":
            height = self.section.scroll_area.width() // 45
        elif base_class_name == "OptionPickerScrollArea":
            height = self.section.scroll_area.width() // 60
        return pixmap.scaledToHeight(height, Qt.TransformationMode.SmoothTransformation)

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        self.clicked.emit()

    def toggle_dropdown_arrow(self, is_expanded) -> None:
        arrow_pixmap = (
            self.expand_arrow_pixmap if is_expanded else self.collapse_arrow_pixmap
        )
        self.arrow_label.setPixmap(arrow_pixmap)

    def resize_section_header(self):
        for button in [
            self.section.vtg_dir_button_manager.opp_button,
            self.section.vtg_dir_button_manager.same_button,
        ]:
            button.setMaximumSize(int(self.height()), int(self.height()))
            button.setIconSize(button.size() * 0.9)
