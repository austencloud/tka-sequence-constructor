from objects.arrow.arrow import Arrow
from objects.staff.staff import Staff
from PyQt6.QtCore import Qt

class KeyEventHandler:
    def keyPressEvent(self, event, graphboard_view):
        main_widget = graphboard_view.main_widget
        arrow_manager = main_widget.arrow_manager
        sequence_view = main_widget.sequence_view
        arrow_manipulator = arrow_manager.manipulator
        arrow_selector = arrow_manager.selector
        self.graphboard_scene = graphboard_view.scene()
        selected_items = self.graphboard_scene.selectedItems()
        staff_handler = graphboard_view.staff_handler
        staff_visibility_manager = staff_handler.visibility_manager
        
        if len(selected_items) >= 1:
            try:
                selected_item = selected_items[0]
            except IndexError:
                selected_item = None

            selected_arrow_color = None
            if selected_item and isinstance(selected_item, Arrow):
                selected_arrow_color = selected_item.color

            if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_Delete:
                for item in selected_items:
                    if isinstance(item, Arrow):
                        arrow_selector.delete_arrow(item)
                    elif isinstance(item, Staff):
                        arrow_selector.delete_staff(item)

            elif event.key() == Qt.Key.Key_Delete:
                for item in selected_items:
                    if isinstance(item, Arrow):
                        arrow_selector.delete_arrow(item)
                        staff_visibility_manager.hide_staff(item.staff)
                    elif isinstance(item, Staff):
                        item.view.staff_handler.visibility_manager.hide_staff(item)

            elif selected_item and isinstance(selected_item, Arrow):
                if event.key() == Qt.Key.Key_W:
                    arrow_manipulator.move_arrow_quadrant_wasd('up', selected_item)
                elif event.key() == Qt.Key.Key_A:
                    arrow_manipulator.move_arrow_quadrant_wasd('left', selected_item)
                elif event.key() == Qt.Key.Key_S:
                    arrow_manipulator.move_arrow_quadrant_wasd('down', selected_item)
                elif event.key() == Qt.Key.Key_D:
                    arrow_manipulator.move_arrow_quadrant_wasd('right', selected_item)
                elif event.key() == Qt.Key.Key_E:
                    arrow_manipulator.mirror_arrow(selected_items, selected_arrow_color)
                elif event.key() == Qt.Key.Key_Q:
                    arrow_manipulator.swap_motion_type(selected_items, selected_arrow_color)
                elif event.key() == Qt.Key.Key_F:
                    sequence_view.add_to_sequence(graphboard_view)
