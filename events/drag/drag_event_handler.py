from events.drag.drag_preview import DragPreview

class DragEventHandler:
    def __init__(self, drag_manager):
        self.drag_manager = drag_manager
        self.helpers = self.drag_manager.helpers
        self.graphboard = self.drag_manager.graphboard
        self.arrowbox = self.drag_manager.arrowbox
        self.scene_updater = self.drag_manager.scene_updater
        self.info_handler = self.drag_manager.info_handler
        self.staff_handler = self.drag_manager.staff_handler
        self.arrow_manager = self.drag_manager.arrow_manager
        self.arrow_attributes = self.arrow_manager.attributes
        self.staff_attributes = self.staff_handler.attributes
        self.staff_factory = self.staff_handler.factory
        self.main_window = self.drag_manager.main_window
        
    ### DRAG INITIALIZATION ###

    def start_drag(self, scene, target_arrow, event_pos):
        self.setup_drag_preview(scene, target_arrow, event_pos)

    def setup_drag_preview(self, arrowbox, target_arrow, event_pos):
        self.drag_preview = DragPreview(self.drag_manager, target_arrow)
        self.arrow_dragged = True
        self.dragging = True
        self.previous_quadrant = None
        self.invisible_arrow = None
        self.target_arrow = target_arrow
        self.drag_preview.setParent(arrowbox.main_widget)
        self.drag_preview.show()
        self.drag_preview.move_to_cursor(arrowbox, event_pos, target_arrow)

    ### DRAG INTO GRAPHBOARD ###

    def handle_drag_into_graphboard(self, view, event):
        if self.drag_preview:
            self.update_drag_preview_for_graphboard(view, event)

    def update_drag_preview_for_graphboard(self, view, event):
        if not self.drag_preview.has_entered_graphboard_once:
            self.just_entered_graphboard = True
            self.drag_preview.has_entered_graphboard_once = True

        local_pos_in_graphboard = self.helpers.get_local_pos_in_graphboard(view, event)
        new_quadrant = self.graphboard.get_graphboard_quadrants(
            self.graphboard.view.mapToScene(local_pos_in_graphboard.toPoint())
        )

        # Check if the quadrant has changed
        if self.previous_quadrant != new_quadrant:
            from objects.arrow.arrow import Arrow

            for item in self.drag_manager.graphboard.items():
                if isinstance(item, Arrow) and item.color == self.drag_preview.color:
                    self.graphboard.removeItem(item)

            self.drag_preview.update_rotation_for_quadrant(new_quadrant)
            new_arrow_dict = self.target_arrow.attributes.create_dict_from_arrow(
                self.drag_preview
            )
            self.invisible_arrow = self.helpers.create_and_add_arrow(new_arrow_dict)
            self.invisible_arrow.setVisible(False)

            self.new_staff_dict = self.staff_attributes.create_staff_dict_from_arrow(
                self.drag_preview
            )

            for staff in self.graphboard.staffs:
                if staff.color == self.drag_preview.color:
                    staff.attributes.update_attributes_from_dict(
                        staff, self.new_staff_dict
                    )
                    staff.arrow = self.invisible_arrow
                    self.invisible_arrow.staff = staff
                    staff.location = staff.arrow.end_location
                    staff.update_appearance()
                    staff.setVisible(True)

            self.staff_handler.update_graphboard_staffs(self.graphboard)

            self.invisible_arrow.arrow_manager.attributes.update_attributes(
                self.invisible_arrow, new_arrow_dict
            )
            self.content_changed = True
            self.info_handler.update()

            self.previous_quadrant = new_quadrant  # Update the previous quadrant

    ### MOUSE MOVE ###

    def handle_mouse_move(self, arrowbox, event, event_pos):
        if hasattr(self, "drag_preview") and self.drag_preview:
            self.update_drag_preview_on_mouse_move(arrowbox, event_pos)
        else:
            event.ignore()

    def update_drag_preview_on_mouse_move(self, arrowbox, event_pos):
        self.update_arrow_drag_preview(arrowbox, event_pos)
        if self.drag_preview.has_entered_graphboard_once and self.content_changed:
            new_arrow_dict = self.arrow_manager.attributes.create_dict_from_arrow(
                self.drag_preview
            )
            self.invisible_arrow.arrow_manager.attributes.update_attributes(
                self.invisible_arrow, new_arrow_dict
            )
            board_state = self.graphboard.get_state()
            self.staff_handler.positioner.reposition_staffs(
                self.graphboard, board_state
            )
            self.info_handler.update()
            self.content_changed = False

    def update_arrow_drag_preview(self, arrowbox, event_pos):
        """Update the arrow's drag preview."""
        over_graphboard = self.helpers.is_over_graphboard(arrowbox, event_pos)

        if over_graphboard:
            self.handle_drag_into_graphboard(arrowbox, event_pos)

        self.drag_preview.move_to_cursor(arrowbox, event_pos, self.target_arrow)

    ### MOUSE RELEASE ###

    def handle_mouse_release(self, event, event_pos):
        if hasattr(self, "drag_preview") and self.drag_preview:
            self.handle_drop_event(event, event_pos)
            self.drag_manager.reset_drag_state()

    def handle_drop_event(self, event, event_pos):
        if self.dragging and event_pos:
            if event_pos.toPoint() not in self.arrowbox.view.rect() and self.drag_preview.has_entered_graphboard_once:
                self.place_arrow_on_graphboard(event)
                self.scene_updater.cleanup_and_update_scene()
                self.scene_updater.update_info_handler()
            else:
                self.drag_preview.deleteLater()
                self.drag_preview = None

    def place_arrow_on_graphboard(self, event):
        placed_arrow = self.invisible_arrow
        placed_arrow.setVisible(True)

        if self.drag_preview.has_entered_graphboard_once:
            self.drag_manager.set_focus_and_accept_event(event)

            self.graphboard.clear_selection()
            placed_arrow.setSelected(True)

    ### MOUSE PRESS EVENTS ###

    def handle_mouse_press(self, event):
        self.graphboard.setFocus()
        items = self.graphboard.items(event.pos())
        self.drag_manager.select_or_deselect_items(event, items)
        if not items or not items[0].isSelected():
            self.graphboard.clear_selection()
