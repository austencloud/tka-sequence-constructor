from typing import TYPE_CHECKING

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtCore import QPointF
from widgets.sequence_widget.sequence_widget_beat_frame.beat import Beat, BeatView

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.sequence_widget.sequence_widget_beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )
    from widgets.sequence_widget.sequence_widget_beat_frame.start_pos_beat import (
        StartPositionBeat,
    )


class StartPositionBeat(Beat):
    def __init__(
        self, main_widget: "MainWidget", beat_frame: "SequenceWidgetBeatFrame"
    ) -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.beat_frame = beat_frame

    def add_start_text(self) -> None:
        start_text_item = QGraphicsTextItem("Start")
        start_text_item.setFont(QFont("Georgia", 60, QFont.Weight.DemiBold))
        start_text_item.setPos(
            QPointF(
                (self.width() // 2) - start_text_item.boundingRect().width() // 2,
                self.height() // 28,
            )
        )
        if self.view and self.view.scene():
            self.view.scene().addItem(start_text_item)


class StartPositionBeatView(BeatView):
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame") -> None:
        self.beat_frame = beat_frame
        super().__init__(beat_frame)
        self.is_filled = False
        self.is_start_pos = True

    def set_start_pos(self, start_pos: "StartPositionBeat") -> None:
        self.start_pos = self.beat = start_pos
        self.is_filled = True
        self.start_pos.view = self
        self.setScene(self.start_pos)
        view_width = self.height()
        self.view_scale = view_width / self.start_pos.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
        self.start_pos.add_start_text()