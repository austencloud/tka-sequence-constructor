from copy import deepcopy
from typing import TYPE_CHECKING, Dict, List
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QFrame,
    QApplication,
)
from PyQt6.QtCore import Qt, pyqtSignal
from Enums import LetterType
from constants import CODEX_PICTOGRAPH
from utilities.TypeChecking.TypeChecking import Letters
from widgets.pictograph.pictograph import Pictograph
from widgets.scroll_area.scroll_area import ScrollArea
from .codex_letter_button_frame import LetterButtonFrame


if TYPE_CHECKING:
    from widgets.main_tab_widget.main_tab_widget import MainTabWidget


class Codex(QWidget):
    imageGenerated = pyqtSignal(str)
    selected_letters: List[Letters] = []

    ### INITIALIZATION ###

    def __init__(self, main_tab_widget: "MainTabWidget") -> None:
        super().__init__(main_tab_widget)
        self.main_tab_widget = main_tab_widget
        self.letters_dict = self.main_tab_widget.main_widget.letters

        self._setup_ui()

    ### UI SETUP ###

    def _setup_ui(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.setLayout(self.layout)
        self.setup_buttons()
        self.scroll_area = ScrollArea(self)
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.left_layout.addWidget(self.scroll_area)
        self.right_layout.addWidget(self.button_panel)
        self.layout.addLayout(self.left_layout)
        self.layout.addLayout(self.right_layout)
        self.connect_buttons(self.letter_button_frame)

    def setup_buttons(self) -> None:
        self.letter_button_frame: LetterButtonFrame = self.setup_button_frames()[0]
        self.action_button_frame: QFrame = self.setup_button_frames()[1]
        self.button_panel = self._setup_button_panel(
            self.letter_button_frame, self.action_button_frame
        )

    def connect_buttons(self, letter_button_frame: LetterButtonFrame) -> None:
        for letter, button in letter_button_frame.buttons.items():
            button.clicked.connect(
                lambda checked, letter=letter: self.letter_button_frame.on_letter_button_clicked(
                    letter
                )
            )

    def setup_button_frames(self) -> LetterButtonFrame:
        letter_button_frame = LetterButtonFrame(self)
        letter_button_frame.setStyleSheet("QFrame { border: 1px solid black; }")
        action_button_frame = self._setup_action_button_frame()
        return letter_button_frame, action_button_frame

    def _setup_button_panel(self, letter_button_frame, action_button_frame) -> QFrame:
        button_panel = QFrame()
        button_panel_layout = QVBoxLayout()
        button_panel.setLayout(button_panel_layout)
        button_panel.setStyleSheet("QFrame { border: 1px solid black; }")
        button_panel.setContentsMargins(0, 0, 0, 0)
        button_panel_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        button_panel_layout.setContentsMargins(0, 0, 0, 0)
        button_panel_layout.setSpacing(0)
        button_panel_layout.addWidget(letter_button_frame, 8)
        button_panel_layout.addWidget(action_button_frame, 1)
        self.button_panel_layout = button_panel_layout
        return button_panel

    def _setup_action_button_frame(self) -> QFrame:
        action_button_frame = QFrame()
        action_buttons = self._setup_action_buttons()
        action_button_frame_layout = QVBoxLayout(action_button_frame)
        action_button_frame_layout.setContentsMargins(0, 0, 0, 0)
        action_button_frame_layout.setSpacing(0)
        for button in action_buttons.values():
            action_button_frame_layout.addWidget(button)

        return action_button_frame

    def _setup_action_buttons(self) -> Dict[str, QPushButton]:
        buttons = {}
        select_all_button = QPushButton("Select All", self)
        select_all_button.setStyleSheet("font-size: 16px;")
        generate_all_images_button = QPushButton("Generate All Images 🧨", self)
        generate_all_images_button.setStyleSheet("font-size: 16px;")
        generate_selected_images_button = QPushButton("Generate Selected Images", self)
        generate_selected_images_button.setStyleSheet("font-size: 16px;")
        select_all_button.clicked.connect(self.select_all_letters)
        generate_all_images_button.clicked.connect(self.generate_all_images)
        generate_selected_images_button.clicked.connect(self.generate_selected_images)
        buttons["select_all_button"] = select_all_button
        buttons["generate_all_button"] = generate_all_images_button
        buttons["generate_selected_button"] = generate_selected_images_button
        return buttons

    ### LETTERS ###

    def get_button_style(self, pressed: bool) -> str:
        if pressed:
            # Here you can define your custom style for the pressed state
            return """
                QPushButton {
                    background-color: #ccd9ff;
                    border: 2px solid #0000ff;
                    padding: 5px;
                }
            """
        else:
            # Here you define the default style
            return """
                QPushButton {
                    background-color: white;
                    border: 1px solid black;
                    padding: 0px;
                }
                QPushButton:hover {
                    background-color: #e6f0ff;
                }
                QPushButton:pressed {
                    background-color: #cce0ff;
                }
            """

    ### IMAGE GENERATION ###

    def process_pictographs_for_letter(self, letter) -> None:
        pictograph_dicts = self.main_tab_widget.main_widget.letters.get(letter, [])
        for pictograph_dict in pictograph_dicts:
            pictograph_key = (
                self.scroll_area.pictograph_factory.generate_pictograph_key_from_dict(
                    pictograph_dict
                )
            )
            self.scroll_area.pictograph_factory.get_or_create_pictograph(
                pictograph_key, pictograph_dict
            )

    def generate_selected_images(self) -> None:
        main_widget = self.parentWidget()
        main_widget.setEnabled(False)
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.setMouseTracking(False)
        for letter in self.selected_letters:
            pictograph_dict_list = self.main_tab_widget.main_widget.letters[letter]
            for pictograph_dict in pictograph_dict_list:
                codex_pictograph: Pictograph = (
                    self.scroll_area.pictograph_factory.create_pictograph(
                        CODEX_PICTOGRAPH
                    )
                )
                codex_pictograph.image_renderer.render_and_cache_image()
        main_widget.setEnabled(True)
        QApplication.restoreOverrideCursor()
        self.setMouseTracking(True)

    def generate_all_images(self) -> None:
        main_widget = self.parentWidget()
        main_widget.setEnabled(False)
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.setMouseTracking(False)
        for _, pictograph_dict_list in self.main_tab_widget.main_widget.letters.items():
            for pictograph_dict in pictograph_dict_list:
                codex_pictograph: Pictograph = self.scroll_area._create_pictograph(
                    CODEX_PICTOGRAPH
                )
                codex_pictograph.render_and_cache_image()

        main_widget.setEnabled(True)
        QApplication.restoreOverrideCursor()
        self.setMouseTracking(True)

    def toggle_pictograph_selection(self, state, index) -> None:
        if state == Qt.CheckState.Checked:
            self.selected_letters.append(index)
        else:
            self.selected_letters.remove(index)

    def select_all_letters(self) -> None:
        for button_letter, button in self.letter_button_frame.buttons.items():
            button.setFlat(True)
            button.setStyleSheet(self.get_button_style(pressed=True))

        for button_letter, button in self.letter_button_frame.buttons.items():
            button.clicked.disconnect()
            button.click()

            self.selected_letters.append(button_letter)
            button.clicked.connect(
                lambda checked, letter=button_letter: self.on_letter_button_clicked(
                    letter
                )
            )

        self.scroll_area.update_pictographs()

    def update_letters_dict(self) -> None:
        for letter, pictograph_list in self.letters_dict.items():
            for pictograph_dict in pictograph_list:
                if "turns" in self.scroll_area.filter_tab_manager.filters:
                    pictograph_dict[
                        "blue_turns"
                    ] = self.scroll_area.filter_tab_manager.filters["turns"]

    def resize_codex(self) -> None:
        self.scroll_area.resize_scroll_area()
        self.scroll_area.update_pictographs()