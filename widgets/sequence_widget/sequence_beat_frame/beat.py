from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QMouseEvent
from widgets.pictograph.pictograph import Pictograph


if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.sequence_widget.sequence_beat_frame.sequence_builder_beat_frame import (
        SequenceBuilderBeatFrame,
    )


class Beat(Pictograph):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.view: "BeatView" = None


class BeatView(QGraphicsView):
    original_style: str

    def __init__(self, beat_frame: "SequenceBuilderBeatFrame") -> None:
        super().__init__(beat_frame)
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.beat_frame = beat_frame
        self.selection_manager = self.beat_frame.selection_manager
        self.beat: "Beat" = None
        self.is_start_pos = False
        self.is_filled = False
        self.is_selected = False
        self.setContentsMargins(0, 0, 0, 0)


    def set_pictograph(self, new_beat: "Beat") -> None:
        self.beat = new_beat
        new_beat.view = self
        new_beat.view.is_filled = True
        self.setScene(self.beat)
        view_width = self.height()
        self.view_scale = view_width / self.beat.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def create_button(self, icon_path, action) -> QPushButton:
        button = QPushButton(QIcon(icon_path), "", self)
        button.clicked.connect(action)
        return button

    def clear(self):
        self.setScene(None)
        self.beat_frame.start_pos_view.setScene(None)
        sequence_builder = self.beat.main_widget.main_builder_widget.sequence_builder
        sequence_builder.current_pictograph = self.beat_frame.start_pos
        sequence_builder.reset_to_start_pos_picker()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.mousePressEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and self.is_filled:
            self.selection_manager.select_beat(self)

    def paintEvent(self, event) -> None:
        super().paintEvent(event)

    def deselect(self) -> None:
        self.is_selected = False
        self.update()
