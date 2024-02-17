from widgets.pictograph.pictograph import Pictograph
from widgets.graph_editor_tab.graph_editor_pictograph_view import (
    GraphEditorPictographView,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.graph_editor_tab.graph_editor_frame import GraphEditorFrame


class GraphEditorPictograph(Pictograph):
    def __init__(
        self, main_widget: "MainWidget", graph_editor: "GraphEditorFrame"
    ) -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.graph_editor = graph_editor
        self.view: GraphEditorPictographView
