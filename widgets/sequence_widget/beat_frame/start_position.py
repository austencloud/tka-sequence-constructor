from constants.numerical_constants import RATIO
from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
)
from objects.pictograph.pictograph import Pictograph
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsView

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.sequence_widget.beat_frame.beat_frame import BeatFrame
    from widgets.sequence_widget.beat_frame.start_position import StartPosition


class StartPosition(Pictograph):
    def __init__(self, main_widget: "MainWidget", beat_frame: "BeatFrame") -> None:
        super().__init__(main_widget, "start_position")
        self.main_widget = main_widget
        self.beat_frame = beat_frame


class StartPositionView(QGraphicsView):
    def __init__(self, beat_frame: "BeatFrame") -> None:
        super().__init__(beat_frame)

        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.start_position: "StartPosition" = None
        self.beat_frame = beat_frame

    def set_start_position(self, start_position: "StartPosition") -> None:
        self.start_position = start_position
        self.setScene(self.start_position)
        view_width = int(self.height() * RATIO)
        self.view_scale = view_width / self.start_position.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def resizeEvent(self, event) -> None:
        view_width = int(self.height() * RATIO)
        self.setMaximumWidth(view_width)
        if self.start_position:
            self.view_scale = view_width / self.start_position.width()
            self.resetTransform()
            self.scale(self.view_scale, self.view_scale)