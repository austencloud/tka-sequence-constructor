from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
    QHBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from typing import TYPE_CHECKING, List
from objects.motion.motion import Motion
from constants import CLOCKWISE_ICON, COUNTER_CLOCKWISE_ICON, ICON_DIR
from ..attr_box.attr_box_widgets.turns_widgets.base_turns_widget.base_turns_widget import (
    TurnsWidget,
)


if TYPE_CHECKING:
    from ..graph_editor_tab.graph_editor_attr_box import GraphEditorAttrBox


class GraphEditorTurnsWidget(TurnsWidget):
    def __init__(self, attr_box: "GraphEditorAttrBox") -> None:
        super().__init__(attr_box)
        self.clockwise_pixmap = self._create_clock_pixmap(CLOCKWISE_ICON)
        self.counter_clockwise_pixmap = self._create_clock_pixmap(
            COUNTER_CLOCKWISE_ICON
        )
        self._setup_ui()

    def _setup_ui(self) -> None:
        # super().setup_ui()
        self._create_clock_labels()
        self.turnbox_vbox_frame: QFrame = self._create_turnbox_vbox_frame()
        self.buttons_hbox_layout = QHBoxLayout()
        self.setup_additional_layouts()
        self._setup_layout_frames()

    def setup_additional_layouts(self) -> None:
        self.turn_display_and_adjust_btns_hbox_layout = QHBoxLayout()

    ### LAYOUTS ###

    def _setup_layout_frames(self) -> None:
        """Adds the header and buttons to their respective frames."""
        self._add_widgets_to_layout(
            [self.clock_left, self.turnbox_vbox_frame, self.clock_right],
            self.turn_display_and_adjust_btns_hbox_layout,
        )

        self.turn_display_and_adjust_btns_hbox_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_hbox_layout.setContentsMargins(0, 0, 0, 0)

        self.header_frame = self._create_frame(
            self.turn_display_and_adjust_btns_hbox_layout
        )
        self.button_frame = self._create_frame(self.buttons_hbox_layout)

        self.header_frame.setContentsMargins(0, 0, 0, 0)
        self.button_frame.setContentsMargins(0, 0, 0, 0)

    def setup_additional_layouts(self):
        self.turn_display_and_adjust_btns_hbox_layout = QHBoxLayout()

    def _create_frame(self, layout: QHBoxLayout | QVBoxLayout) -> QFrame:
        """Creates a frame with the given layout."""
        frame = QFrame()
        frame.setLayout(layout)
        frame.setContentsMargins(0, 0, 0, 0)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        return frame

    ### WIDGETS ###

    def _add_widgets_to_layout(
        self, widgets: List[QWidget], layout: QHBoxLayout | QVBoxLayout
    ) -> None:
        """Adds the given widgets to the specified layout."""
        for widget in widgets:
            layout.addWidget(widget)

    def _create_clock_labels(self) -> None:
        """Creates and configures the clock labels for rotation direction."""
        self.clock_left, self.clock_right = QLabel(), QLabel()
        for clock in [self.clock_left, self.clock_right]:
            clock.setLayout(QVBoxLayout())
            clock.setAlignment(Qt.AlignmentFlag.AlignCenter)
            clock.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
            clock.setScaledContents(True)
            clock.clear()

    def _create_turnbox_vbox_frame(self) -> None:
        """Creates the turns box and buttons for turn adjustments."""
        turnbox_frame = QFrame(self)
        turnbox_frame.setLayout(QVBoxLayout())

        self.turns_label = QLabel("Turns")
        self.turns_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        turnbox_frame.layout().addWidget(self.turns_label)
        turnbox_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        turnbox_frame.layout().setContentsMargins(0, 0, 0, 0)
        turnbox_frame.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        turnbox_frame.layout().setSpacing(0)
        return turnbox_frame

    def _create_clock_pixmap(self, icon_path: str) -> QPixmap:
        """Load and scale a clock pixmap based on the initial size."""
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            print(f"Failed to load the icon from {icon_path}.")
            return QPixmap()
        return pixmap

    ### CALLBACKS ###

    def _add_turn_callback(self) -> None:
        motion = self.attr_box.pictograph.motions[self.attr_box.color]
        if motion:
            motion.add_turn()
            self.attr_box.update_attr_box(motion)

    def _subtract_turn_callback(self) -> None:
        motion = self.attr_box.pictograph.motions[self.attr_box.color]
        if motion:
            motion.subtract_turn()
            self.attr_box.update_attr_box(motion)

    def _add_half_turn_callback(self) -> None:
        motion = self.attr_box.pictograph.motions[self.attr_box.color]
        if motion:
            motion.add_half_turn()
            self.attr_box.update_attr_box(motion)

    def _subtract_half_turn_callback(self) -> None:
        motion = self.attr_box.pictograph.motions[self.attr_box.color]
        if motion:
            motion.subtract_half_turn()
            self.attr_box.update_attr_box(motion)

    ### UPDATE METHODS ###

    def _update_clocks(self, rot_dir: str) -> None:
        # Clear both clock labels
        self.clock_left.clear()
        self.clock_right.clear()

        # Depending on the rotation direction, display the correct clock
        if rot_dir == "ccw":
            self.clock_left.setPixmap(self.counter_clockwise_pixmap)
        elif rot_dir == "cw":
            self.clock_right.setPixmap(self.clockwise_pixmap)
        elif rot_dir == None:
            self.clock_left.clear()
            self.clock_right.clear()

    def _update_turnbox(self, turns) -> None:
        turns_str = str(turns)
        for i in range(self.turn_display_manager.turns_display.count()):
            if self.turn_display_manager.turns_display.itemText(i) == turns_str:
                self.turn_display_manager.turns_display.setCurrentIndex(i)
                return
            elif turns == None:
                self.turn_display_manager.turns_display.setCurrentIndex(-1)

    def _update_turns(self, index: int) -> None:
        turns = str(index)
        if turns == "0" or turns == "1" or turns == "2" or turns == "3":
            motion: Motion = self.attr_box.pictograph.motions[self.attr_box.color]
            if motion and motion.arrow:
                if int(turns) != motion.turns:
                    motion.set_motion_turns(int(turns))
                    self.attr_box.update_attr_box(motion)
                    self.attr_box.pictograph.update()
        elif turns == "0.5" or turns == "1.5" or turns == "2.5":
            motion: Motion = self.attr_box.pictograph.motions[self.attr_box.color]
            if motion:
                if float(turns) != motion.turns:
                    motion.set_motion_turns(float(turns))
                    self.attr_box.update_attr_box(motion)
                    self.attr_box.pictograph.update()
        else:
            self.turn_display_manager.turns_display.setCurrentIndex(-1)

    ### EVENT HANDLERS ###

    def _update_widget_sizes(self) -> None:
        """Updates the sizes of the widgets based on the widget's size."""
        available_height = self.height()
        header_height = int(available_height * 2 / 3)
        turns_widget_height = int(available_height * 1 / 3)
        self.header_frame.setMaximumHeight(header_height)

    def _update_clock_size(self) -> None:
        """Updates the sizes of the clock labels based on the widget's size."""
        clock_size = int(self.height() / 2)
        for clock in [self.clock_left, self.clock_right]:
            clock.setMinimumSize(clock_size, clock_size)
            clock.setMaximumSize(clock_size, clock_size)

    def _update_button_size(self) -> None:
        for adjust_turns_button in self.turn_adjustment_manager.adjust_turns_buttons:
            button_size = int(self.attr_box.width() / 7)
            if (
                adjust_turns_button.text() == "-0.5"
                or adjust_turns_button.text() == "+0.5"
            ):
                button_size = int(button_size * 0.85)
            else:
                button_size = int(self.attr_box.width() / 6)
            adjust_turns_button.update_adjust_turns_button_size(button_size)
