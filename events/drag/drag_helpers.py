from events.drag.drag_preview import DragPreview
from PyQt6.QtWidgets import QGraphicsItem, QApplication

class DragHelpers:
    def __init__(self, drag_manager):
        self.drag_manager = drag_manager
        self.graphboard_view = self.drag_manager.graphboard_view
        self.graphboard_scene = self.drag_manager.graphboard_scene
        self.staff_handler = self.drag_manager.staff_handler
        self.staff_factory = self.drag_manager.staff_factory
        self.arrow_factory = self.drag_manager.arrow_factory
        
    def is_click_on_arrow(self, view, event):
        from objects.arrow.arrow import Arrow

        items = view.items(event.pos())
        return any(isinstance(item, Arrow) for item in items)

    def is_over_graphboard(self, view, event):
        pos_in_main_window = view.mapTo(view.window(), event.pos())
        local_pos_in_graphboard = self.drag_manager.graphboard_view.mapFrom(
            view.window(), pos_in_main_window
        )
        return self.drag_manager.graphboard_view.rect().contains(local_pos_in_graphboard)

    def get_local_pos_in_graphboard(self, view, event):
        return self.drag_manager.graphboard_view.mapFrom(
            view.window(), view.mapTo(view.window(), event.pos())
        )

    def create_and_add_arrow(self, arrow_dict):
        new_arrow = self.arrow_factory.create_arrow(self.graphboard_view, arrow_dict)
        new_arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.graphboard_scene.addItem(new_arrow)
        return new_arrow

    def link_arrow_and_staff(self, arrow, staff):
        arrow.staff = staff
        staff.arrow = arrow
        
