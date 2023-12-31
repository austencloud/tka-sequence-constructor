from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop
from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent


class PictographEventHandler:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

    def handle_mouse_press(self, event: "QGraphicsSceneMouseEvent") -> None:
        scene_pos = event.scenePos()
        items_at_pos = self.pictograph.items(scene_pos)

        # Prioritize arrows over props if both are clicked simultaneously
        arrow = next((item for item in items_at_pos if isinstance(item, Arrow)), None)
        if arrow:
            self.pictograph.select_arrow(arrow)  # Select the arrow
            self.pictograph.dragged_arrow = arrow
            self.pictograph.dragged_arrow.mousePressEvent(event)
        else:
            prop = next((item for item in items_at_pos if isinstance(item, Prop)), None)
            if prop:
                self.pictograph.dragged_prop = prop
                self.pictograph.dragged_prop.mousePressEvent(event)
            else:
                self.pictograph.clear_selections()
                
    def handle_mouse_move(self, event) -> None:
        if self.pictograph.dragged_prop:
            self.pictograph.dragged_prop.mouseMoveEvent(event)
        elif self.pictograph.dragged_arrow:
            self.pictograph.dragged_arrow.mouseMoveEvent(event)

    def handle_mouse_release(self, event) -> None:
        if self.pictograph.dragged_prop:
            self.pictograph.dragged_prop.mouseReleaseEvent(event)
            self.pictograph.dragged_prop = None
        elif self.pictograph.dragged_arrow:
            self.pictograph.dragged_arrow.mouseReleaseEvent(event)
            self.pictograph.dragged_arrow = None

    def handle_context_menu(self, event: "QGraphicsSceneMouseEvent") -> None:
        scene_pos = self.pictograph.view.mapToScene(event.pos().toPoint())
        items_at_pos = self.pictograph.items(scene_pos)

        clicked_item = None
        for item in items_at_pos:
            if isinstance(item, Arrow) or isinstance(item, Prop):
                clicked_item = item
                break

        if not clicked_item and items_at_pos:
            clicked_item = items_at_pos[0]

        event_pos = event.screenPos()
        self.pictograph.pictograph_menu_handler.create_master_menu(
            event_pos, clicked_item
        )
