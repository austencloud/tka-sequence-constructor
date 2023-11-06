from objects.arrow.arrow import Arrow
from PyQt6.QtCore import QByteArray

from PyQt6.QtGui import QTransform
from settings.string_constants import *


class ArrowManipulator:
    def __init__(self, arrow_manager):
        self.arrow_manager = arrow_manager

    def set_turns(self, arrows, color, turns):
        arrows = [arrow for arrow in arrows if arrow.color == color]
        for arrow in arrows:
            arrow.turns = turns
            self.update_arrow_turns(arrow)
            self.finalize_manipulation(arrow)

    def increment_turns(self, arrows, color):
        arrows = [arrow for arrow in arrows if arrow.color == color]
        for arrow in arrows:
            arrow.turns += 1
            if arrow.turns > 2:
                arrow.turns = 0
            self.update_arrow_turns(arrow)
            self.finalize_manipulation(arrow)

    def decrement_turns(self, arrows, color):
        arrows = [arrow for arrow in arrows if arrow.color == color]
        for arrow in arrows:
            arrow.turns -= 1
            if arrow.turns < 0:
                arrow.turns = 2
            self.update_arrow_turns(arrow)
            self.finalize_manipulation(arrow)

    def update_arrow_turns(self, arrow):
        """Update the appearance of the arrow based on its turns."""
        arrow.svg_file = (
            f"resources/images/arrows/shift/{arrow.motion_type}_{arrow.turns}.svg"
        )
        arrow.initialize_svg_renderer(arrow.svg_file)
        arrow.update_appearance()

    def update_arrow_and_staff(self, arrow, arrow_dict, staff_dict):
        staff = arrow.staff
        arrow.attributes.update_attributes(arrow, arrow_dict)
        staff.attributes.update_attributes_from_dict(staff, staff_dict)

    def finalize_manipulation(self, arrow):
        self.arrow_manager.positioner.update_arrow_position(
            self.arrow_manager.graphboard
        )
        arrow.update_appearance()
        self.arrow_manager.infobox.update()
        arrow.scene.staff_handler.update_graphboard_staffs(arrow.scene)
        arrow.scene.info_handler.update()

    def move_arrow_quadrant_wasd(self, direction, selected_arrow):
        wasd_quadrant_mapping = {
            UP: {"se": "ne", "sw": "nw"},
            LEFT: {"ne": "nw", "se": "sw"},
            DOWN: {"ne": "se", "nw": "sw"},
            RIGHT: {"nw": "ne", "sw": "se"},
        }
        selected_arrow = selected_arrow
        current_quadrant = selected_arrow.quadrant
        new_quadrant = wasd_quadrant_mapping.get(direction, {}).get(
            current_quadrant, current_quadrant
        )
        selected_arrow.quadrant = new_quadrant
        (
            new_start_location,
            new_end_location,
        ) = selected_arrow.attributes.get_start_end_locations(
            selected_arrow.motion_type, selected_arrow.rotation_direction, new_quadrant
        )

        updated_arrow_dict = {
            COLOR: selected_arrow.color,
            MOTION_TYPE: selected_arrow.motion_type,
            QUADRANT: new_quadrant,
            ROTATION_DIRECTION: selected_arrow.rotation_direction,
            START_LOCATION: new_start_location,
            END_LOCATION: new_end_location,
            TURNS: selected_arrow.turns,
        }

        updated_staff_dict = {
            COLOR: selected_arrow.color,
            LOCATION: new_end_location,
            LAYER: 1,
        }

        self.update_arrow_and_staff(
            selected_arrow, updated_arrow_dict, updated_staff_dict
        )
        self.finalize_manipulation(selected_arrow)

    def rotate_arrow(self, rotation_direction, arrows):
        if arrows:
            for arrow in arrows:
                quadrants = ["ne", "se", "sw", "nw"]
                current_quadrant_index = quadrants.index(arrow.quadrant)
                new_quadrant_index = (
                    (current_quadrant_index + 1) % 4
                    if rotation_direction == RIGHT
                    else (current_quadrant_index - 1) % 4
                )
                new_quadrant = quadrants[new_quadrant_index]
                (
                    new_start_location,
                    new_end_location,
                ) = arrow.attributes.get_start_end_locations(
                    arrow.motion_type, arrow.rotation_direction, new_quadrant
                )

                updated_arrow_dict = {
                    COLOR: arrow.color,
                    MOTION_TYPE: arrow.motion_type,
                    QUADRANT: new_quadrant,
                    ROTATION_DIRECTION: arrow.rotation_direction,
                    START_LOCATION: new_start_location,
                    END_LOCATION: new_end_location,
                    TURNS: arrow.turns,
                }

                updated_staff_dict = {
                    COLOR: arrow.color,
                    LOCATION: new_end_location,
                    LAYER: 1,
                }

            self.update_arrow_and_staff(arrow, updated_arrow_dict, updated_staff_dict)
            self.finalize_manipulation(arrow)

    def mirror_arrow(self, arrows, color):
        arrows = [arrow for arrow in arrows if arrow.color == color]
        for arrow in arrows:
            if arrow.is_mirrored:
                arrow.is_mirrored = False
                original_svg_data = arrow.get_svg_data(arrow.svg_file)
                arrow.renderer.load(QByteArray(original_svg_data))  # No need to encode

                # Reset the transformation matrix to the identity matrix to unmirror the arrow
                arrow.resetTransform()

            else:
                arrow.is_mirrored = True

                # Get the center of the arrow
                center_x = arrow.boundingRect().width() / 2
                center_y = arrow.boundingRect().height() / 2

                # Create a QTransform object and configure it for mirroring around the center
                transform = QTransform()
                transform.translate(center_x, center_y)
                transform.scale(-1, 1)
                transform.translate(-center_x, -center_y)

                # Apply the transform to the arrow
                arrow.setTransform(transform)

            if arrow.rotation_direction == COUNTER_CLOCKWISE:
                new_rotation_direction = CLOCKWISE
            elif arrow.rotation_direction == CLOCKWISE:
                new_rotation_direction = COUNTER_CLOCKWISE

            old_start_location = arrow.start_location
            old_end_location = arrow.end_location
            new_start_location = old_end_location
            new_end_location = old_start_location

            arrow.update_appearance()

            new_arrow_dict = {
                COLOR: arrow.color,
                MOTION_TYPE: arrow.motion_type,
                QUADRANT: arrow.quadrant,
                ROTATION_DIRECTION: new_rotation_direction,
                START_LOCATION: new_start_location,
                END_LOCATION: new_end_location,
                TURNS: arrow.turns,
            }

            arrow.staff.location = new_end_location
            arrow.attributes.update_attributes(arrow, new_arrow_dict)
            self.finalize_manipulation(arrow)
            self.arrow_manager.positioner.update_arrow_position(arrow.scene)
            arrow.update()
            arrow.scene.staff_handler.update_graphboard_staffs(arrow.scene)

    def swap_motion_type(self, arrows, color):
        arrows = [arrow for arrow in arrows if arrow.color == color]
        if not isinstance(arrows, list):
            arrows = [arrows]

        arrows = [arrow for arrow in arrows if isinstance(arrow, Arrow)]

        for arrow in arrows:
            if arrow.motion_type == ANTI:
                new_motion_type = PRO
            elif arrow.motion_type == PRO:
                new_motion_type = ANTI
            else:
                continue

            if arrow.rotation_direction == COUNTER_CLOCKWISE:
                new_rotation_direction = CLOCKWISE
            elif arrow.rotation_direction == CLOCKWISE:
                new_rotation_direction = COUNTER_CLOCKWISE

            new_arrow_dict = {
                COLOR: arrow.color,
                MOTION_TYPE: new_motion_type,
                QUADRANT: arrow.quadrant,
                ROTATION_DIRECTION: new_rotation_direction,
                START_LOCATION: arrow.start_location,
                END_LOCATION: arrow.end_location,
                TURNS: arrow.turns,
            }

            new_staff_dict = {
                COLOR: arrow.color,
                LOCATION: arrow.end_location,
                LAYER: 1,
            }

            arrow.svg_file = (
                f"resources/images/arrows/shift/{new_motion_type}_{arrow.turns}.svg"
            )
            arrow.initialize_svg_renderer(arrow.svg_file)
            arrow.attributes.update_attributes(arrow, new_arrow_dict)
            arrow.update_appearance()
            arrow.scene.info_handler.update()

            self.arrow_manager.infobox.update()

            self.update_arrow_and_staff(arrow, new_arrow_dict, new_staff_dict)
            self.finalize_manipulation(arrow)

    def swap_colors(self):
        graphboard = self.arrow_manager.graphboard
        current_letter = graphboard.info_handler.determine_current_letter_and_type()[0]
        if current_letter != "G" and current_letter != "H":
            arrows = [
                item for item in self.graphboard.items() if isinstance(item, Arrow)
            ]
            if len(arrows) >= 1:
                for arrow in arrows:
                    if arrow.color == RED:
                        new_color = BLUE
                    elif arrow.color == BLUE:
                        new_color = RED
                    else:
                        continue

                    arrow.color = new_color
                    arrow.staff.color = new_color

                    arrow.update_appearance()
                    arrow.staff.update_appearance()
                    self.finalize_manipulation(arrow)
