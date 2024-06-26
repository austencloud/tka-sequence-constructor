from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtGui import QLinearGradient, QColor, QPainter
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QWidget


class BackgroundManager(QObject):
    update_required = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.gradient_shift = 0
        self.color_shift = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_background)
        self.timer.start(50)

    def animate_background(self):
        pass

