from typing import TYPE_CHECKING
from Enums.Enums import LetterType, Turns
from Enums.MotionAttributes import PropRotDir
from data.constants import (
    BLUE,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    FLOAT,
    NO_ROT,
    RED,
    STATIC,
    SAME,
    OPP,
)
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from .turns_widget import TurnsWidget
    from base_widgets.base_pictograph.base_pictograph import BasePictograph

    from objects.motion.motion import Motion


class TurnsUpdater:
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        self.turns_box = turns_widget.turns_box
        self.turns_widget = turns_widget
        self.json_manager = (
            self.turns_widget.turns_box.adjustment_panel.graph_editor.main_widget.json_manager
        )
        self.beat_frame = (
            self.turns_widget.turns_box.adjustment_panel.graph_editor.sequence_widget.beat_frame
        )

    def set_motion_turns(self, motion: "Motion", new_turns: Turns) -> None:
        if new_turns == "fl":
            motion.prefloat_motion_type = motion.motion_type
            motion.motion_type = FLOAT
            pictograph_index = self.beat_frame.get_index_of_currently_selected_beat()
            self.json_manager.updater.update_motion_type_in_json_at_index(
                pictograph_index + 2, motion.color, FLOAT
            )
        else:
            motion.motion_type = motion.prefloat_motion_type
            pictograph_index = self.beat_frame.get_index_of_currently_selected_beat()
            self.json_manager.updater.update_motion_type_in_json_at_index(
                pictograph_index + 2, motion.color, motion.motion_type
            )
        self._update_turns(motion, new_turns)
        other_motion_color = RED if motion.color == BLUE else BLUE
        other_motion = motion.pictograph.get.other_motion(motion)
        arrow_dict = {
            f"{motion.color}_attributes": {"turns": new_turns},
            f"{other_motion_color}_attributes": {"turns": other_motion.turns},
        }
        motion.pictograph.updater.update_pictograph(arrow_dict)
        self._repaint_views(motion)

    def _repaint_views(self, motion: "Motion"):
        """Repaint the pictograph and GE pictograph views to reflect the change."""
        motion.pictograph.view.repaint()
        GE_pictograph = (
            self.turns_box.adjustment_panel.graph_editor.pictograph_container.GE_pictograph_view.get_current_pictograph()
        )
        GE_pictograph.view.repaint()
        QApplication.processEvents()

    def _adjust_turns_for_pictograph(
        self, pictograph: "BasePictograph", adjustment: Turns
    ) -> None:
        """Adjust turns for each relevant motion in the pictograph."""
        for motion in pictograph.motions.values():
            if motion.color == self.turns_box.color:
                new_turns = self._calculate_new_turns(motion.turns, adjustment)
                self.set_motion_turns(motion, new_turns)

    def _calculate_new_turns(self, current_turns: Turns, adjustment: Turns) -> Turns:
        """Calculate new turns value based on adjustment."""
        new_turns = max(0, min(3, current_turns + adjustment))
        return int(new_turns) if new_turns.is_integer() else new_turns

    def _update_turns(self, motion: "Motion", new_turns: Turns) -> None:
        """Update motion's turns and rotation properties based on new turn value."""
        if motion.motion_type in [DASH, STATIC]:
            self._handle_static_dash_motion(motion, new_turns)
        motion.turns_manager.set_motion_turns(new_turns)

    def _handle_static_dash_motion(self, motion: "Motion", new_turns: Turns) -> None:
        """Handle specific logic for static or dash motion types."""
        vtg_dir_button_manager = self.turns_widget.turns_box.vtg_dir_button_manager

        if new_turns == 0:
            motion.prop_rot_dir = NO_ROT
            vtg_dir_button_manager.unpress_vtg_buttons()
            if hasattr(self.turns_box, "prop_rot_dir_button_manager"):
                self.turns_widget.turns_box.prop_rot_dir_button_manager.unpress_prop_rot_dir_buttons()
            # if the prop rot dir butons are visible, hide them
            if self.turns_box.prop_rot_dir_button_manager.cw_button.isVisible():
                self.turns_box.prop_rot_dir_button_manager.hide_prop_rot_dir_buttons()
            if self.turns_box.vtg_dir_button_manager.same_button.isVisible():
                self.turns_box.vtg_dir_button_manager.hide_vtg_dir_buttons()

        elif motion.turns == 0 and new_turns > 0:
            self._set_prop_rot_dir(motion)

    def _set_prop_rot_dir(self, motion: "Motion") -> None:
        """set the rotation direction of the motion based on the vtg directional relationship."""
        other_motion = motion.pictograph.get.other_motion(motion)
        GE_pictograph = (
            self.turns_box.adjustment_panel.graph_editor.pictograph_container.GE_pictograph_view.get_current_pictograph()
        )
        if GE_pictograph.letter_type in [
            LetterType.Type2,
            LetterType.Type3,
        ]:
            prop_rot_dir = self._determine_prop_rot_dir_for_type2_type3(other_motion)
            motion.prop_rot_dir = prop_rot_dir
            if not self.turns_box.vtg_dir_button_manager.same_button.isVisible():
                self.turns_box.vtg_dir_button_manager.show_vtg_dir_buttons()
        elif GE_pictograph.letter_type in [
            LetterType.Type4,
            LetterType.Type5,
            LetterType.Type6,
        ]:
            if not self.turns_box.prop_rot_dir_button_manager.cw_button.isVisible():
                self.turns_box.prop_rot_dir_button_manager.show_prop_rot_dir_buttons()
            self._set_prop_rot_dir_for_type4_5_6(motion)

    def _set_prop_rot_dir_for_type4_5_6(self, motion: "Motion"):
        if self.turns_box.prop_rot_dir_btn_state[CLOCKWISE]:
            motion.prop_rot_dir = CLOCKWISE
        elif self.turns_box.prop_rot_dir_btn_state[COUNTER_CLOCKWISE]:
            motion.prop_rot_dir = COUNTER_CLOCKWISE
        elif (
            not self.turns_box.prop_rot_dir_btn_state[CLOCKWISE]
            and not self.turns_box.prop_rot_dir_btn_state[COUNTER_CLOCKWISE]
        ):
            motion.prop_rot_dir = self._get_default_prop_rot_dir_for_type4_5_6()
        if motion.prop_rot_dir == CLOCKWISE:
            self.turns_box.prop_rot_dir_button_manager.cw_button.press()
            self.turns_box.prop_rot_dir_btn_state[CLOCKWISE] = True
            self.turns_box.prop_rot_dir_btn_state[COUNTER_CLOCKWISE] = False
        elif motion.prop_rot_dir == COUNTER_CLOCKWISE:
            self.turns_box.prop_rot_dir_button_manager.ccw_button.press()
            self.turns_box.prop_rot_dir_btn_state[CLOCKWISE] = False
            self.turns_box.prop_rot_dir_btn_state[COUNTER_CLOCKWISE] = True

    def _determine_prop_rot_dir_for_type2_type3(
        self, other_motion: "Motion"
    ) -> PropRotDir:
        """Determine the property rotation direction."""
        vtg_state = self.turns_box.vtg_dir_btn_state
        self.turns_box.vtg_dir_button_manager.show_vtg_dir_buttons()
        if not vtg_state[SAME] and not vtg_state[OPP]:
            self._set_vtg_dir_state_default()

        if vtg_state[SAME]:
            # if the button isn't pressed, press it
            same_button = self.turns_box.vtg_dir_button_manager.same_button
            if not same_button.is_pressed():
                same_button.press()
            return other_motion.prop_rot_dir
        elif vtg_state[OPP]:
            opposite_button = self.turns_box.vtg_dir_button_manager.opp_button
            if not opposite_button.is_pressed():
                opposite_button.press()
            if other_motion.prop_rot_dir == CLOCKWISE:
                return COUNTER_CLOCKWISE
            elif other_motion.prop_rot_dir == COUNTER_CLOCKWISE:
                return CLOCKWISE

    def _get_default_prop_rot_dir_for_type4_5_6(self) -> PropRotDir:
        self._set_prop_rot_dir_state_default()
        self.turns_box.prop_rot_dir_button_manager.show_prop_rot_dir_buttons()
        self.turns_box.prop_rot_dir_button_manager.cw_button.press()
        return CLOCKWISE

    def _set_vtg_dir_state_default(self) -> None:
        """set the vtg direction state to default."""
        self.turns_box.vtg_dir_btn_state[SAME] = True
        self.turns_box.vtg_dir_btn_state[OPP] = False

    def _set_prop_rot_dir_state_default(self) -> None:
        """set the vtg direction state to default."""
        self.turns_box.prop_rot_dir_btn_state[CLOCKWISE] = True
        self.turns_box.prop_rot_dir_btn_state[COUNTER_CLOCKWISE] = False

    def _clamp_turns(self, turns: Turns) -> Turns:
        """Clamp the turns value to be within allowable range."""
        return max(0, min(3, turns))
