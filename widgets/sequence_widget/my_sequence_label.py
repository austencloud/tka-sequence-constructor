from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class MySequenceLabel(QLabel):
    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.setMouseTracking(True)
        self.setAcceptDrops(True)
        self.setLineWidth(2)
        self.setScaledContents(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("My Sequence:")
        padding = self.height() // 4
        self.setContentsMargins(0, 0, 0, padding)

    def resize_my_sequence_label(self) -> None:
        size = self.sequence_widget.width() // 30
        font = QFont("Monotype Corsiva", size, QFont.Weight.Bold)
        self.setFont(font)
