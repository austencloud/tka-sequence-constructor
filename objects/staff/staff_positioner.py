from PyQt6.QtCore import QPointF
import math
from resources.constants import (
    GRAPHBOARD_WIDTH,
    GRAPHBOARD_SCALE,
    PICTOGRAPH_SCALE,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    BETA_OFFSET,
)
from objects.staff.staff import Staff


class StaffPositioner:
    def __init__(self, staff_handler):
        self.staff_handler = staff_handler
        self.letters = staff_handler.main_widget.letters

        
    ### REPOSITIONERS ###

    def check_replace_beta_staffs(self, scene):
        view = scene.views()[0]
        board_state = view.get_state()

        visible_staves = []
        
        for staff in view.staffs:
            if staff.isVisible():
                visible_staves.append(staff)

        if len(visible_staves) == 2:
            if visible_staves[0].location == visible_staves[1].location:
                self.reposition_staffs(scene, board_state)

    def reposition_staffs(self, scene, board_state):
        view = scene.views()[0]
        scale = GRAPHBOARD_SCALE if view else PICTOGRAPH_SCALE

        def move_staff(staff, direction):
            new_position = self.calculate_new_position(staff.pos(), direction, scale)
            staff.setPos(new_position)

        arrows_grouped_by_start = {}
        for arrow in board_state["arrows"]:
            arrows_grouped_by_start.setdefault(arrow["start_location"], []).append(
                arrow
            )

        pro_or_anti_arrows = [
            arrow
            for arrow in board_state["arrows"]
            if arrow["motion_type"] in ["pro", "anti"]
        ]
        static_arrows = [
            arrow for arrow in board_state["arrows"] if arrow["motion_type"] == "static"
        ]

        # STATIC BETA
        if len(static_arrows) > 1:
            self.reposition_static_beta(static_arrows, scale)

        # BETA → BETA - G, H, I
        for start_location, arrows in arrows_grouped_by_start.items():
            if len(arrows) > 1 and all(
                arrow["start_location"] == arrow["end_location"] for arrow in arrows
            ):
                self.reposition_beta_to_beta(scene, arrows, scale)


        # GAMMA → BETA - Y, Z
        if len(pro_or_anti_arrows) == 1 and len(static_arrows) == 1:
            self.reposition_gamma_to_beta(move_staff, pro_or_anti_arrows, static_arrows)

        # ALPHA → BETA - D, E, F
        converging_arrows = [
            arrow
            for arrow in board_state["arrows"]
            if arrow["motion_type"] not in ["static"]
        ]
        if len(converging_arrows) == 2:
            if converging_arrows[0].get("start_location") != converging_arrows[1].get(
                "start_location"
            ):
                self.reposition_alpha_to_beta(move_staff, converging_arrows)

        scene.update()

    def reposition_static_beta(self, static_arrows, scale):
        for arrow in static_arrows:
            staff = next((staff for staff in self.staffs_on_board.values() if staff.arrow.color == arrow['color']), None)
            if not staff:
                continue

            end_location = arrow.get("end_location", "")

            beta_reposition_map = {
                ("N", "red"): "right",
                ("N", "blue"): "left",
                ("S", "red"): "right",
                ("S", "blue"): "left",
                ("E", "red"): ("up", "down") if end_location == "e" else None,
                ("W", "blue"): ("up", "down") if end_location == "w" else None,
            }

            action = beta_reposition_map.get((staff.location, arrow["color"]), None)

            if action:
                if isinstance(action, str):
                    self.move_staff(staff, action, scale)
                elif isinstance(action, tuple):
                    self.move_staff(staff, action[0], scale)
                    other_staff = next(
                        (
                            s
                            for s in self.staff_handler.staffs_on_board
                            if s.location == staff.location and s != staff
                        ),
                        None,
                    )
                    if other_staff:
                        self.move_staff(other_staff, action[1], scale)

    def reposition_alpha_to_beta(self, move_staff, converging_arrows):  # D, E, F
        end_locations = [arrow["end_location"] for arrow in converging_arrows]
        start_locations = [arrow["start_location"] for arrow in converging_arrows]
        if (
            end_locations[0] == end_locations[1]
            and start_locations[0] != start_locations[1]
        ):
            for arrow in converging_arrows:
                direction = self.determine_translation_direction(arrow)
                if direction:
                    move_staff(
                        next(
                            staff
                            for staff in self.staff_handler.main_widget.graphboard_view.staffs
                            if staff.arrow.color == arrow["color"]
                        ),
                        direction,
                    )

    def reposition_beta_to_beta(self, scene, arrows, scale):  # G, H, I
        view = scene.views()[0]
        if len(arrows) != 2:
            return

        arrow1, arrow2 = arrows
        same_motion_type = (
            arrow1["motion_type"] == arrow2["motion_type"] in ["pro", "anti"]
        )

        if same_motion_type:
            self.reposition_G_and_H(scale, view, arrow1, arrow2)

        else:
            self.reposition_I(scale, arrow1, arrow2)

        scene.update()

    def reposition_G_and_H(self, scale, view, arrow1, arrow2):
        optimal_position1 = self.get_optimal_arrow_location(arrow1, view)
        optimal_position2 = self.get_optimal_arrow_location(arrow2, view)

        distance1 = self.get_distance_from_center(optimal_position1)
        distance2 = self.get_distance_from_center(optimal_position2)

        further_arrow = arrow1 if distance1 > distance2 else arrow2
        other_arrow = arrow1 if further_arrow == arrow2 else arrow2

        further_direction = self.determine_translation_direction(further_arrow)

        further_staff = next(
            staff
            for staff in self.staff_handler.main_widget.graphboard_view.staffs
            if staff.arrow.color == further_arrow["color"]
        )
        new_position_further = self.calculate_new_position(
            further_staff.pos(), further_direction, scale
        )
        further_staff.setPos(new_position_further)

        other_direction = self.get_opposite_direction(further_direction)
        other_staff = next(
            staff
            for staff in self.staff_handler.main_widget.graphboard_view.staffs
            if staff.arrow.color == other_arrow["color"]
        )
        new_position_other = self.calculate_new_position(
            other_staff.pos(), other_direction, scale
        )
        other_staff.setPos(new_position_other)

    def reposition_I(self, scale, arrow1, arrow2):
        pro_arrow = arrow1 if arrow1["motion_type"] == "pro" else arrow2
        anti_arrow = arrow2 if arrow1["motion_type"] == "pro" else arrow1

        pro_staff = next(
            (
                staff
                for staff in self.staff_handler.main_widget.graphboard_view.staffs
                if staff.arrow.color == pro_arrow["color"]
            ),
            None,
        )
        anti_staff = next(
            (
                staff
                for staff in self.staff_handler.main_widget.graphboard_view.staffs
                if staff.arrow.color == anti_arrow["color"]
            ),
            None,
        )

        if pro_staff and anti_staff:
            # Determine the direction to move the staffs based on the pro arrow's start and end locations
            pro_staff_translation_direction = self.determine_translation_direction(
                pro_arrow
            )
            anti_staff_translation_direction = self.get_opposite_direction(
                pro_staff_translation_direction
            )

            # Move the staff corresponding to the pro arrow closer
            new_position_pro = self.calculate_new_position(
                pro_staff.pos(), pro_staff_translation_direction, scale
            )
            pro_staff.setPos(new_position_pro)

            # Move the other staff further
            new_position_anti = self.calculate_new_position(
                anti_staff.pos(), anti_staff_translation_direction, scale
            )
            anti_staff.setPos(new_position_anti)

    def reposition_gamma_to_beta(
        self, move_staff, pro_or_anti_arrows, static_arrows
    ):  # Y, Z
        pro_or_anti_arrow, static_arrow = pro_or_anti_arrows[0], static_arrows[0]
        direction = self.determine_translation_direction(pro_or_anti_arrow)
        if direction:
            move_staff(
                next(
                    staff
                    for staff in self.staff_handler.main_widget.graphboard_view.staffs
                    if staff.arrow.color == pro_or_anti_arrow["color"]
                ),
                direction,
            )
            move_staff(
                next(
                    staff
                    for staff in self.staff_handler.main_widget.graphboard_view.staffs
                    if staff.arrow.color == static_arrow["color"]
                ),
                self.get_opposite_direction(direction),
            )

    ### HELPERS ###

    def get_distance_from_center(self, position):
        center_point = QPointF(
            GRAPHBOARD_WIDTH / 2, GRAPHBOARD_WIDTH / 2
        )  # Assuming this is the center point of your coordinate system

        x_position = position.get("x", 0.0)
        y_position = position.get("y", 0.0)
        center_x = center_point.x()
        center_y = center_point.y()

        # Calculate the distance
        distance = math.sqrt(
            (x_position - center_x) ** 2 + (y_position - center_y) ** 2
        )
        return distance

    def get_optimal_arrow_location(self, arrow, view):
        current_state = view.get_state()
        current_letter = view.info_handler.determine_current_letter_and_type()[0]

        if current_letter is not None:
            matching_letters = self.letters[current_letter]
            optimal_location = self.find_optimal_arrow_location(
                current_state, view, matching_letters, arrow
            )

            if optimal_location:
                return optimal_location

        return None  # Return None if there are no optimal positions

    def find_optimal_arrow_location(
        self, current_state, view, matching_letters, arrow_dict
    ):
        for variations in matching_letters:
            if view.main_widget.arrow_manager.state_comparator.compare_states(
                current_state, variations
            ):
                optimal_entry = next(
                    (
                        d
                        for d in variations
                        if "optimal_red_location" in d and "optimal_blue_location" in d
                    ),
                    None,
                )

                if optimal_entry:
                    color_key = f"optimal_{arrow_dict['color']}_location"
                    return optimal_entry.get(color_key)

        return None

    def set_staff_position_based_on_arrow(self, arrow, scale):
        staff = next(
            (
                staff
                for staff in self.staff_handler.staffs_on_board
                if staff.arrow.color == arrow["color"]
                and staff.location == arrow["end_location"]
            ),
            None,
        )
        direction = self.determine_translation_direction(arrow)
        new_position = self.calculate_new_position(staff.pos(), direction, scale)
        staff.setPos(new_position)

    def determine_translation_direction(self, arrow_state):
        """Determine the translation direction based on the arrow's board_state."""
        if arrow_state["motion_type"] in ["pro", "anti"]:
            if arrow_state["end_location"] in ["n", "s"]:
                return RIGHT if arrow_state["start_location"] == "e" else LEFT
            elif arrow_state["end_location"] in ["e", "w"]:
                return DOWN if arrow_state["start_location"] == "s" else UP
        return None

    def calculate_new_position(self, current_position, direction, scale):
        """Calculate the new position based on the direction."""
        offset = (
            QPointF(BETA_OFFSET * scale, 0)
            if direction in [LEFT, RIGHT]
            else QPointF(0, BETA_OFFSET * scale)
        )
        if direction in [RIGHT, DOWN]:
            return current_position + offset
        else:
            return current_position - offset

    def get_opposite_direction(self, movement):
        if movement == "left":
            return "right"
        elif movement == "right":
            return "left"
        elif movement == "up":
            return "down"
        elif movement == "down":
            return "up"

    ### UPDATERS ###

    def update_staff_position_based_on_quadrant(self, staff, quadrant):
        new_position = self.calculate_new_position_based_on_quadrant(staff, quadrant)
        staff.setPos(new_position)