from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from functools import partial

from .lesson_mode_toggle_widget import LessonModeToggleWidget

if TYPE_CHECKING:
    from .learn_widget import LearnWidget


class LessonSelector(QWidget):
    """Widget for selecting lessons and quiz mode in the learning module."""

    def __init__(self, learn_widget: "LearnWidget") -> None:
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.main_widget = learn_widget.main_widget

        # Store buttons and description labels for resizing
        self.buttons: dict[str, QPushButton] = {}
        self.description_labels: dict[str, QLabel] = {}

        # Layout setup
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        # Title label
        self.title_label = QLabel("Select a Lesson:")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create ModeToggleWidget and center it
        self.mode_toggle_widget = LessonModeToggleWidget(self)

        # Add elements to layout
        self.layout.addStretch(2)
        self.layout.addWidget(self.title_label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.mode_toggle_widget)  # Add toggle widget here
        self.layout.addStretch(1)

        # Add buttons and description labels for each lesson
        self.add_lesson_button(
            "Lesson 1",
            "Match the correct letter to the given pictograph",
            partial(self.learn_widget.start_lesson, 1),
        )
        self.add_lesson_button(
            "Lesson 2",
            "Identify the correct pictograph for the displayed letter",
            partial(self.learn_widget.start_lesson, 2),
        )
        self.add_lesson_button(
            "Lesson 3",
            "Choose the pictograph that logically follows",
            partial(self.learn_widget.start_lesson, 3),
        )

        self.layout.addStretch(2)

    def add_lesson_button(
        self, button_text: str, description_text: str, callback
    ) -> None:
        """Create and add a button and its description as a vertical group."""
        # Create a vertical layout for the button and its description
        lesson_layout = QVBoxLayout()
        lesson_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create the button
        button = QPushButton(button_text)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(callback)
        self.buttons[button_text] = button

        # Create the description label
        description_label = QLabel(description_text)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_labels[button_text] = description_label

        # Add the button and description to the vertical layout
        lesson_layout.addWidget(button)
        lesson_layout.addWidget(description_label)

        # Add the lesson layout to the main layout
        self.layout.addLayout(lesson_layout)
        self.layout.addStretch(1)

    # --------------------------------------
    # Resizing Methods
    # --------------------------------------
    def resize_lesson_selector(self) -> None:
        """Resize title, buttons, and descriptions based on window size."""
        self._resize_title_label()
        self._resize_lesson_layouts()
        self._resize_toggle_button()

    def _resize_title_label(self):
        title_font_size = self.main_widget.width() // 50
        font = self.title_label.font()
        font.setFamily("Georgia")
        font.setPointSize(title_font_size)
        self.title_label.setFont(font)

    def _resize_lesson_layouts(self):
        self._resize_buttons()
        self._resize_descriptions()
        self._resize_mode_labels()

    def _resize_mode_labels(self):
        for label in [
            self.mode_toggle_widget.fixed_question_label,
            self.mode_toggle_widget.countdown_label,
        ]:
            label_font_size = self.main_widget.width() // 85
            font = label.font()
            font.setPointSize(label_font_size)
            label.setFont(font)

    def _resize_buttons(self):
        for button in self.buttons.values():
            button_font_size = self.main_widget.width() // 50
            button.setFixedSize(
                self.main_widget.width() // 4, self.main_widget.height() // 10
            )
            button.setStyleSheet(f"font-size: {button_font_size}px;")

    def _resize_descriptions(self):
        for description in self.description_labels.values():
            description_font_size = self.main_widget.width() // 140
            font = description.font()
            font.setPointSize(description_font_size)
            description.setFont(font)

    def _resize_toggle_button(self):
        button_font_size = self.main_widget.width() // 60