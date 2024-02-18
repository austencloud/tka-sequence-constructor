from typing import TYPE_CHECKING
from widgets.pictograph.components.pictograph_view import PictographView
from widgets.pictograph.pictograph import Pictograph
from PyQt6.QtWidgets import QGraphicsView, QFrame
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.graph_editor.graph_editor import GraphEditor


if TYPE_CHECKING:
    from widgets.graph_editor.graph_editor_pictograph import GraphEditorBlankPictograph


class GraphEditorBlankPictograph(Pictograph):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__(graph_editor.main_widget)
        self.main_widget = graph_editor.main_widget
        self.graph_editor = graph_editor
        # self.get.initiallize_getter()


class GraphEditorPictographView(PictographView):
    def __init__(
        self, GE: "GraphEditor", blank_pictograph: "GraphEditorBlankPictograph"
    ) -> None:
        super().__init__(blank_pictograph)
        self.GE = GE
        self.GE_pictograph = blank_pictograph
        self.main_widget = GE.main_widget
        self.setScene(blank_pictograph)

    def resize_GE_pictograph_view(self):
        self.setMinimumHeight(self.GE.height())
        self.setMinimumWidth(self.GE.height())
        if self.scene():
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def set_to_blank_grid(self):
        self.setScene(self.GE_pictograph)