from PyQt6.QtCore import QPointF
import math
from settings.numerical_constants import BETA_OFFSET, STAFF_LENGTH, STAFF_WIDTH
from settings.string_constants import (
    VERTICAL,
    COLOR,
    MOTION_TYPE,
    STATIC,
    START_LOCATION,
    END_LOCATION,
    PRO,
    ANTI,
    NORTH,
    SOUTH,
    EAST,
    WEST,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    RED,
    BLUE,
)
from typing import TYPE_CHECKING, Dict, List
from objects.staff import Staff
from utilities.TypeChecking.TypeChecking import (
    ArrowAttributesDicts,
    LetterDictionary,
    OptimalLocationEntries,
    OptimalLocationsDicts,
    Direction,
    Location,
)

if TYPE_CHECKING:
    from widgets.graphboard.graphboard import GraphBoard


class StaffPositioner:
    current_state: List[ArrowAttributesDicts]
    matching_letters: List[LetterDictionary]
    arrow_dict: List[ArrowAttributesDicts]
    letters: LetterDictionary

    def __init__(self, graphboard: "GraphBoard") -> None:
        self.graphboard = graphboard
        self.view = graphboard.view
        self.letters = graphboard.letters

    def update(self) -> None:
        for staff in self.graphboard.staffs:
            self.set_default_staff_locations(staff)
        if self.staffs_in_beta():
            self.reposition_beta_staffs()

    def set_default_staff_locations(self, staff: "Staff") -> None:
        staff.set_staff_transform_origin_to_center()
        if (
            staff.location in self.graphboard.grid.handpoints
        ):  # add check for key existence
            if staff.axis == VERTICAL:
                staff.setPos(
                    self.graphboard.grid.handpoints[staff.location]
                    + QPointF(-STAFF_LENGTH / 2, -STAFF_LENGTH + STAFF_WIDTH / 2)
                )
            else:
                staff.setPos(
                    self.graphboard.grid.handpoints[staff.location]
                    + QPointF(-STAFF_LENGTH / 2, -STAFF_WIDTH / 2)
                )

    def reposition_beta_staffs(self) -> None:
        board_state = self.graphboard.get_state()

        def move_staff(staff: Staff, direction) -> None:
            new_position = self.calculate_new_position(staff.pos(), direction)
            staff.setPos(new_position)

        arrows_grouped_by_start_loc: Dict[Location, List[ArrowAttributesDicts]] = {}
        for arrow in board_state:
            arrows_grouped_by_start_loc.setdefault(arrow[START_LOCATION], []).append(arrow)

        pro_or_anti_arrows = [
            arrow for arrow in board_state if arrow[MOTION_TYPE] in [PRO, ANTI]
        ]
        static_arrows = [arrow for arrow in board_state if arrow[MOTION_TYPE] == STATIC]

        # STATIC BETA
        if len(static_arrows) > 1:
            self.reposition_static_beta(move_staff, static_arrows)

        # BETA → BETA - G, H, I
        for start_location, arrows in arrows_grouped_by_start_loc.items():
            if len(arrows) == 2:
                arrow1, arrow2 = arrows
                if (
                    arrow1[START_LOCATION] == arrow2[START_LOCATION]
                    and arrow1[END_LOCATION] == arrow2[END_LOCATION]
                ):
                    if arrow1[MOTION_TYPE] in [PRO, ANTI]:
                        if arrow2[MOTION_TYPE] in [PRO, ANTI]:
                            self.reposition_beta_to_beta(arrows)

        # GAMMA → BETA - Y, Z
        if len(pro_or_anti_arrows) == 1 and len(static_arrows) == 1:
            self.reposition_gamma_to_beta(move_staff, pro_or_anti_arrows, static_arrows)

        # ALPHA → BETA - D, E, F
        converging_arrows = [
            arrow for arrow in board_state if arrow[MOTION_TYPE] not in [STATIC]
        ]
        if len(converging_arrows) == 2:
            if converging_arrows[0].get(START_LOCATION) != converging_arrows[1].get(
                START_LOCATION
            ):
                self.reposition_alpha_to_beta(move_staff, converging_arrows)

    ### STATIC BETA ### β

    def reposition_static_beta(self, move_staff: callable, static_arrows: List[ArrowAttributesDicts]) -> None:
        for arrow in static_arrows:
            staff = next(
                (
                    staff
                    for staff in self.graphboard.staffs
                    if staff.arrow.color == arrow[COLOR]
                ),
                None,
            )
            if not staff:
                continue

            end_location = arrow[END_LOCATION]

            beta_reposition_map = {
                (NORTH, RED): RIGHT,
                (NORTH, BLUE): LEFT,
                (SOUTH, RED): RIGHT,
                (SOUTH, BLUE): LEFT,
                (EAST, RED): (UP, DOWN) if end_location == EAST else None,
                (WEST, BLUE): (UP, DOWN) if end_location == WEST else None,
            }

            direction: Direction= beta_reposition_map.get((staff.location, arrow[COLOR]), None)

            if direction:
                if isinstance(direction, str):
                    move_staff(staff, direction)
                elif isinstance(direction, tuple):
                    move_staff(staff, direction[0])
                    other_staff = next(
                        (
                            s
                            for s in self.graphboard.staffs
                            if s.location == staff.location and s != staff
                        ),
                        None,
                    )
                    if other_staff:
                        move_staff(other_staff, direction[1])

    ### ALPHA TO BETA ### D, E, F

    def reposition_alpha_to_beta(self, move_staff, converging_arrows) -> None:
        end_locations = [arrow[END_LOCATION] for arrow in converging_arrows]
        start_locations = [arrow[START_LOCATION] for arrow in converging_arrows]
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
                            for staff in self.graphboard.staffs
                            if staff.arrow.color == arrow[COLOR]
                        ),
                        direction,
                    )

    ### BETA TO BETA ### G, H, I

    def reposition_beta_to_beta(self, arrows) -> None:
        arrow1, arrow2 = arrows
        same_motion_type = arrow1[MOTION_TYPE] == arrow2[MOTION_TYPE] in [PRO, ANTI]

        if same_motion_type:
            self.reposition_G_and_H(arrow1, arrow2)

        else:
            self.reposition_I(arrow1, arrow2)

    def reposition_G_and_H(self, arrow1, arrow2) -> None:
        optimal_location1 = self.get_optimal_arrow_location(arrow1)
        optimal_location2 = self.get_optimal_arrow_location(arrow2)

        if not optimal_location1 or not optimal_location2:
            return

        distance1 = self.get_distance_from_center(optimal_location1)
        distance2 = self.get_distance_from_center(optimal_location2)

        further_arrow = arrow1 if distance1 > distance2 else arrow2
        other_arrow = arrow1 if further_arrow == arrow2 else arrow2

        further_direction = self.determine_translation_direction(further_arrow)

        further_staff = next(
            staff
            for staff in self.graphboard.staffs
            if staff.arrow.color == further_arrow[COLOR]
        )
        new_position_further = self.calculate_new_position(
            further_staff.pos(), further_direction
        )
        further_staff.setPos(new_position_further)

        other_direction = self.get_opposite_direction(further_direction)
        other_staff = next(
            staff
            for staff in self.graphboard.staffs
            if staff.arrow.color == other_arrow[COLOR]
        )
        new_position_other = self.calculate_new_position(
            other_staff.pos(), other_direction
        )
        other_staff.setPos(new_position_other)

    def reposition_I(self, arrow1, arrow2) -> None:
        pro_arrow = arrow1 if arrow1[MOTION_TYPE] == PRO else arrow2
        anti_arrow = arrow2 if arrow1[MOTION_TYPE] == PRO else arrow1

        pro_staff = next(
            (
                staff
                for staff in self.graphboard.staffs
                if staff.arrow.color == pro_arrow[COLOR]
            ),
            None,
        )
        anti_staff = next(
            (
                staff
                for staff in self.graphboard.staffs
                if staff.arrow.color == anti_arrow[COLOR]
            ),
            None,
        )

        if pro_staff and anti_staff:
            pro_staff_translation_direction = self.determine_translation_direction(
                pro_arrow
            )
            anti_staff_translation_direction = self.get_opposite_direction(
                pro_staff_translation_direction
            )

            new_position_pro = self.calculate_new_position(
                pro_staff.pos(), pro_staff_translation_direction
            )
            pro_staff.setPos(new_position_pro)

            new_position_anti = self.calculate_new_position(
                anti_staff.pos(), anti_staff_translation_direction
            )
            anti_staff.setPos(new_position_anti)

    ### GAMMA TO BETA ### Y, Z

    def reposition_gamma_to_beta(
        self, move_staff, pro_or_anti_arrows, static_arrows
    ) -> None:
        pro_or_anti_arrow, static_arrow = pro_or_anti_arrows[0], static_arrows[0]
        direction = self.determine_translation_direction(pro_or_anti_arrow)
        if direction:
            move_staff(
                next(
                    staff
                    for staff in self.graphboard.staffs
                    if staff.arrow.color == pro_or_anti_arrow[COLOR]
                ),
                direction,
            )
            move_staff(
                next(
                    staff
                    for staff in self.graphboard.staffs
                    if staff.arrow.color == static_arrow[COLOR]
                ),
                self.get_opposite_direction(direction),
            )

    ### HELPERS ###

    def staffs_in_beta(self) -> bool | None:
        visible_staves: List[Staff] = []
        for staff in self.graphboard.staffs:
            if staff.isVisible():
                visible_staves.append(staff)
        if len(visible_staves) == 2:
            if visible_staves[0].location == visible_staves[1].location:
                return True
            else:
                return False

    def find_optimal_arrow_location_entry(
        self,
        current_state,
        matching_letters,
        arrow_dict,
    ) -> OptimalLocationEntries | None:
        for variants in matching_letters:
            if self.graphboard.arrow_positioner.compare_states(current_state, variants):
                optimal_entry: OptimalLocationsDicts = next(
                    (
                        d
                        for d in variants
                        if "optimal_red_location" in d and "optimal_blue_location" in d
                    ),
                    None,
                )

                if optimal_entry:
                    color_key = f"optimal_{arrow_dict[COLOR]}_location"
                    return optimal_entry.get(color_key)
        return None

    def determine_translation_direction(self, arrow_state) -> Direction:
        """Determine the translation direction based on the arrow's board_state."""
        if arrow_state[MOTION_TYPE] in [PRO, ANTI]:
            if arrow_state[END_LOCATION] in [NORTH, SOUTH]:
                return RIGHT if arrow_state[START_LOCATION] == EAST else LEFT
            elif arrow_state[END_LOCATION] in [EAST, WEST]:
                return DOWN if arrow_state[START_LOCATION] == SOUTH else UP

    def calculate_new_position(
        self,
        current_position: QPointF,
        direction: Direction,
    ) -> QPointF:
        offset = (
            QPointF(BETA_OFFSET, 0)
            if direction in [LEFT, RIGHT]
            else QPointF(0, BETA_OFFSET)
        )
        if direction in [RIGHT, DOWN]:
            return current_position + offset
        else:
            return current_position - offset

    ### GETTERS

    def get_distance_from_center(self, arrow_pos: Dict[str, float]) -> float:
        grid_center = self.graphboard.grid.center
        arrow_x, arrow_y = arrow_pos.get("x", 0.0), arrow_pos.get("y", 0.0)
        center_x, center_y = grid_center.x(), grid_center.y()

        distance_from_center = math.sqrt(
            (arrow_x - center_x) ** 2 + (arrow_y - center_y) ** 2
        )
        return distance_from_center

    def get_optimal_arrow_location(
        self, arrow_attributes: ArrowAttributesDicts
    ) -> Dict[str, float] | None:
        current_state = self.graphboard.get_state()
        current_letter = self.graphboard.current_letter

        if current_letter is not None:
            matching_letters = self.letters[current_letter]
            optimal_location = self.find_optimal_arrow_location_entry(
                current_state, matching_letters, arrow_attributes
            )
            if optimal_location:
                return optimal_location
        return None

    def get_opposite_direction(self, movement: Direction) -> Direction:
        if movement == LEFT:
            return RIGHT
        elif movement == RIGHT:
            return LEFT
        elif movement == UP:
            return DOWN
        elif movement == DOWN:
            return UP