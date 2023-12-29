from typing import TYPE_CHECKING, Dict, Tuple
import pandas as pd
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QFrame,
    QApplication,
)
from PyQt6.QtCore import Qt, pyqtSignal
from constants import BLUE, RED
from widgets.image_generator_tab.ig_filter_frame import IGFilterFrame
from widgets.image_generator_tab.ig_letter_button_frame import IGLetterButtonFrame
from widgets.image_generator_tab.ig_pictograph import IGPictograph
from widgets.image_generator_tab.ig_scroll import IGScroll


if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
from typing import List


class IGTab(QWidget):
    imageGenerated = pyqtSignal(str)  # Signal to indicate when an image is generated

    ### INITIALIZATION ###

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.main_pictograph = (
            self.main_widget.graph_editor_tab.graph_editor.main_pictograph
        )
        self.pictograph_df = self.load_and_sort_data("PictographDataFrame.csv")
        self.selected_pictographs = []
        self.setupUI()

    ### DATA LOADING ###

    def load_and_sort_data(self, file_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            df.set_index(["start_pos", "end_pos"], inplace=True)
            df.sort_index(inplace=True)
            return df
        except Exception as e:
            # Handle specific exceptions as needed
            print(f"Error loading data: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error

    ### UI SETUP ###

    def setupUI(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.setLayout(self.layout)
        button_panel = QFrame()
        button_panel_layout = QVBoxLayout()

        self.letter_button_frame = IGLetterButtonFrame(self.main_widget)
        self.layout.addWidget(self.letter_button_frame)

        self.ig_scroll_area = IGScroll(self.main_widget, self)
        self.filter_frame = IGFilterFrame(self)
        self.letter_button_frame.setStyleSheet(
            """
            QFrame {
                border: 1px solid black;
            }
            """
        )
        action_button_frame = self._setup_action_button_frame()
        button_panel.setLayout(button_panel_layout)
        button_panel.setStyleSheet(
            """
            QFrame {
                border: 1px solid black;
            }
            """
        )
        button_panel.setContentsMargins(0, 0, 0, 0)
        button_panel_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        button_panel_layout.setContentsMargins(0, 0, 0, 0)
        button_panel_layout.setSpacing(0)
        button_panel_layout.addWidget(self.letter_button_frame, 8)
        button_panel_layout.addWidget(action_button_frame, 1)
        self.layout.addWidget(self.ig_scroll_area)
        self.layout.addWidget(button_panel)
        letters = self.get_letters()
        letters.sort(
            key=lambda x: x
            if x not in ["Σ", "Δ", "θ", "Ω", "Φ", "Ψ", "Λ", "α", "β", "Γ"]
            else chr(ord(x) + 1000)
        )

        for key, button in self.letter_button_frame.buttons.items():
            button.clicked.connect(
                lambda checked, letter=key: self.on_letter_button_clicked(letter)
            )

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
        generate_all_images_button = QPushButton("Generate All Images 🧨", self)
        generate_all_images_button.setStyleSheet("font-size: 16px;")

        generate_selected_images_button = QPushButton("Generate Selected Images", self)
        generate_selected_images_button.setStyleSheet("font-size: 16px;")

        generate_all_images_button.clicked.connect(self.generate_all_images)
        generate_selected_images_button.clicked.connect(self.generate_selected_images)

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

    def get_letters(self) -> List[str]:
        return self.pictograph_df.iloc[:, 0].unique().tolist()

    ### IMAGE GENERATION ###

    def on_letter_button_clicked(self, letter) -> None:
        print(f"Button for letter {letter} clicked")
        button = self.letter_button_frame.buttons[letter]

        if letter in self.selected_pictographs:
            self.selected_pictographs.remove(letter)
            button.setFlat(False)  # This makes the button appear not pressed
            button.setStyleSheet(self.get_button_style(pressed=False))
        else:
            self.selected_pictographs.append(letter)
            button.setFlat(True)  # This makes the button appear pressed
            button.setStyleSheet(self.get_button_style(pressed=True))

        self.ig_scroll_area.update_displayed_pictographs()

    def on_letter_checkbox_state_changed(self, state, letter) -> None:
        print(f"Checkbox for letter {letter} state changed: {state}")
        if state and letter not in self.selected_pictographs:
            self.selected_pictographs.append(letter)
        elif not state and letter in self.selected_pictographs:
            self.selected_pictographs.remove(letter)
        self.ig_scroll_area.update_displayed_pictographs()  # Add this line to update the display

    def generate_selected_images(self) -> None:
        main_widget = self.parentWidget()  # Access the main widget
        main_widget.setEnabled(False)  # Disable the widget
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)  # Show loading cursor
        self.setMouseTracking(False)  # Ignore mouse clicks
        for letter in self.selected_pictographs:
            self.generate_images_for_letter(letter)
        main_widget.setEnabled(True)  # Enable the widget after generation
        QApplication.restoreOverrideCursor()
        self.setMouseTracking(True)  # Enable mouse clicks

    def generate_all_images(self) -> None:
        main_widget = self.parentWidget()  # Access the main widget
        main_widget.setEnabled(False)  # Disable the widget
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)  # Show loading cursor
        self.setMouseTracking(False)  # Ignore mouse clicks
        for letter in self.get_letters():
            self.generate_images_for_letter(letter)
        main_widget.setEnabled(True)  # Enable the widget after generation
        QApplication.restoreOverrideCursor()

        self.setMouseTracking(True)  # Enable mouse clicks

    def generate_images_for_letter(self, letter) -> None:
        pictographs_for_letter: pd.DataFrame = self.pictograph_df[
            self.pictograph_df["letter"] == letter
        ]

        for index, pictograph_data in pictographs_for_letter.iterrows():
            self.render_pictograph_to_image(pictograph_data)

    def toggle_pictograph_selection(self, state, index) -> None:
        if state == Qt.CheckState.Checked:
            self.selected_pictographs.append(index)
        else:
            self.selected_pictographs.remove(index)

    def render_pictograph_to_image(self, pd_row_data) -> None:
        ig_pictograph = self._create_ig_pictograph(pd_row_data)
        ig_pictograph.update_pictograph()
        ig_pictograph.render_and_cache_image()

    ### OPTION CREATION ###

    def _create_ig_pictograph(self, pd_row_data: pd.Series):
        letter = pd_row_data["letter"]
        ig_pictograph = IGPictograph(self.main_widget, self.ig_scroll_area)
        ig_pictograph.setSceneRect(0, 0, 950, 950)

        ig_pictograph._finalize_motion_setup(pd_row_data, self.filter_frame.filters)

        blue_motion_dict = ig_pictograph._create_motion_dict_from_pd_row_data(
            pd_row_data, "blue", self.filter_frame.filters
        )
        red_motion_dict = ig_pictograph._create_motion_dict_from_pd_row_data(
            pd_row_data, "red", self.filter_frame.filters
        )

        ig_pictograph.props[RED].ghost = ig_pictograph.ghost_props[RED]
        ig_pictograph.props[BLUE].ghost = ig_pictograph.ghost_props[BLUE]
        ig_pictograph.motions[RED].prop = ig_pictograph.props[RED]
        ig_pictograph.motions[BLUE].prop = ig_pictograph.props[BLUE]

        ig_pictograph.motions[RED].setup_attributes(red_motion_dict)
        ig_pictograph.motions[BLUE].setup_attributes(blue_motion_dict)

        ig_pictograph.current_letter = letter
        ig_pictograph.start_pos = pd_row_data.name[0]
        ig_pictograph.end_pos = pd_row_data.name[1]

        ig_pictograph.motions[RED].arrow = ig_pictograph.arrows[RED]
        ig_pictograph.motions[BLUE].arrow = ig_pictograph.arrows[BLUE]
        ig_pictograph.motions[RED].prop = ig_pictograph.props[RED]
        ig_pictograph.motions[BLUE].prop = ig_pictograph.props[BLUE]
        ig_pictograph.motions[RED].arrow.location = ig_pictograph.motions[
            RED
        ].get_arrow_location(
            ig_pictograph.motions[RED].start_loc,
            ig_pictograph.motions[RED].end_loc,
        )
        ig_pictograph.motions[BLUE].arrow.location = ig_pictograph.motions[
            BLUE
        ].get_arrow_location(
            ig_pictograph.motions[BLUE].start_loc,
            ig_pictograph.motions[BLUE].end_loc,
        )

        ig_pictograph.arrows[RED].motion_type = pd_row_data["red_motion_type"]
        ig_pictograph.arrows[BLUE].motion_type = pd_row_data["blue_motion_type"]
        ig_pictograph.motions[RED].motion_type = pd_row_data["red_motion_type"]
        ig_pictograph.motions[BLUE].motion_type = pd_row_data["blue_motion_type"]

        ig_pictograph.arrows[RED].motion = ig_pictograph.motions[RED]
        ig_pictograph.arrows[BLUE].motion = ig_pictograph.motions[BLUE]

        ig_pictograph.motions[RED].end_or = ig_pictograph.motions[RED].get_end_or()
        ig_pictograph.motions[BLUE].end_or = ig_pictograph.motions[BLUE].get_end_or()

        ig_pictograph.motions[RED].update_prop_orientation()
        ig_pictograph.motions[BLUE].update_prop_orientation()

        for arrow in ig_pictograph.arrows.values():
            arrow.set_is_svg_mirrored_from_attributes()
            arrow.update_mirror()
            arrow.update_appearance()

        for prop in ig_pictograph.props.values():
            prop.update_rotation()
            prop.update_appearance()

        motion = ig_pictograph.motions[arrow.color]
        arrow.motion, prop.motion = motion, motion
        arrow.ghost = ig_pictograph.ghost_arrows[arrow.color]
        arrow.ghost.motion = motion
        ig_pictograph.update_pictograph()
        return ig_pictograph
