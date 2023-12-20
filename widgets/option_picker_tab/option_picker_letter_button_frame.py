from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QFont, QColor, QResizeEvent
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtSvg import QSvgRenderer
from data.letter_engine_data import letter_types
from constants.string_constants import LETTER_BTN_ICON_DIR
from typing import TYPE_CHECKING, List

from utilities.TypeChecking.Letters import Letters

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.option_picker_tab.option_picker_scroll import OptionPickerTab


class OptionPickerLetterButtonFrame(QFrame):
    def __init__(
        self, main_widget: "MainWidget", option_picker_widget: "OptionPickerTab"
    ) -> None:
        super().__init__()
        self.main_widget = main_widget
        self.option_picker_widget = option_picker_widget
        self.spacing = int(self.width() * 0.01)
        self.init_letter_buttons_layout()

    def init_letter_buttons_layout(self) -> None:
        letter_buttons_layout = QVBoxLayout()
        self.setContentsMargins(0, 0, 0, 0)
        letter_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.row_layouts: List[
            QHBoxLayout
        ] = []  # Add this line to initialize the list of row layouts

        self.letter_rows = [
            # Type 1 - Dual-Shift
            ["A", "B", "C"],
            ["D", "E", "F"],
            ["G", "H", "I"],
            ["J", "K", "L"],
            ["M", "N", "O"],
            ["P", "Q", "R"],
            ["S", "T", "U", "V"],
            # Type 2 - Shift
            ["W", "X", "Y", "Z"],
            ["Σ", "Δ", "θ", "Ω"],
            # Type 3 - Cross-Shift
            ["W-", "X-", "Y-", "Z-"],
            ["Σ-", "Δ-", "θ-", "Ω-"],
            # Type 4 - Dash
            ["Φ", "Ψ", "Λ"],
            # Type 5 - Dual-Dash
            ["Φ-", "Ψ-", "Λ-"],
            # Type 6 - Static
            ["α", "β", "Γ"],
        ]

        for row in self.letter_rows:
            row_layout = QHBoxLayout()
            row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row_layout.setSpacing(self.spacing)
            self.row_layouts.append(row_layout)

            for letter in row:
                letter_type = self.get_letter_type(letter)
                icon_path = self.get_icon_path(letter_type, letter)
                button = self.create_button(icon_path)
                row_layout.addWidget(button)

            letter_buttons_layout.addLayout(row_layout)

        self.letter_buttons_layout = letter_buttons_layout

        self.setLayout(letter_buttons_layout)

    def get_letter_type(self, letter: str) -> str:
        for letter_type in letter_types:
            if letter in letter_types[letter_type]:
                return letter_type
        return ""

    def get_icon_path(self, letter_type: str, letter: Letters) -> str:
        return f"{LETTER_BTN_ICON_DIR}/{letter_type}/{letter}.svg"

    def create_button(self, icon_path: str) -> QPushButton:
        renderer = QSvgRenderer(icon_path)
        pixmap = QPixmap(renderer.defaultSize())
        pixmap.fill(QColor(Qt.GlobalColor.transparent))
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        button = QPushButton(QIcon(pixmap), "", self.main_widget)

        button.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                border: none;
                border-radius: 0px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #e6f0ff;
            }
            QPushButton:pressed {
                background-color: #cce0ff;
            }
            """
        )
        # button.setFlat(True)
        font = QFont()
        font.setPointSize(int(20))
        button.setFont(font)
        return button

    def resize_letter_buttons(self) -> None:
        self.spacing = int(self.width() * 0.01)
        button_row_count = len(self.letter_rows)
        button_size = int((self.main_widget.height() / button_row_count) / 2)
        if button_size > self.height() / button_row_count:
            button_size = int(self.height() / (button_row_count + 1))
        icon_size = int(button_size * 0.9)

        for row_layout in self.row_layouts:
            for i in range(row_layout.count()):
                button: QPushButton = row_layout.itemAt(i).widget()
                if button:
                    button.setMaximumSize(button_size, button_size)
                    button.setIconSize(QSize(icon_size, icon_size))

        self.setMaximumHeight(int(self.main_widget.height() * 0.9))
        available_width = button_size * 4
        self.setMaximumWidth(int(available_width + self.spacing * 3))

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.resize_letter_buttons()
