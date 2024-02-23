from typing import TYPE_CHECKING, Union
from constants import (
    ANTI,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    ICON_DIR,
    OPP,
    PRO,
    PROP_ROT_DIR,
    SAME,
)
from Enums.MotionAttributes import (
    Color,
    LeadStates,
    MotionType,
    PropRotDir,
)
from Enums.Enums import VTG_Directions

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize
from widgets.factories.button_factory.buttons.rot_dir_buttons import VtgDirButton


if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_turns_box import GE_TurnsBox

    from objects.motion.motion import Motion


class GE_VtgDirButtonManager:
    def __init__(self, turns_box: "GE_TurnsBox") -> None:
        self.turns_box = turns_box
        self.graph_editor = turns_box.graph_editor
        self.previous_turns = 0
        self.vtg_state = self.turns_box.vtg_dir_btn_state

        self.vtg_dir_buttons: list[VtgDirButton] = self._setup_vtg_dir_buttons()
        self.hide_vtg_dir_buttons()

    def show_vtg_dir_buttons(self) -> None:
        self.opp_button.show()
        self.same_button.show()

    def hide_vtg_dir_buttons(self) -> None:
        self.opp_button.hide()
        self.same_button.hide()

    def _setup_vtg_dir_buttons(self) -> list[QPushButton]:
        button_factory = self.graph_editor.main_widget.button_factory
        self.same_button: VtgDirButton = button_factory.create_vtg_dir_button(
            f"{ICON_DIR}same_direction.png", lambda: self._set_vtg_dir(SAME), SAME
        )
        self.opp_button: VtgDirButton = button_factory.create_vtg_dir_button(
            f"{ICON_DIR}opp_direction.png", lambda: self._set_vtg_dir(OPP), OPP
        )
        self.same_button.unpress()
        self.opp_button.unpress()

        return [self.same_button, self.opp_button]

    def _set_vtg_dir(self, vtg_dir: VTG_Directions) -> None:
        self._update_pictographs_vtg_dir(vtg_dir)
        self._update_button_states(self.vtg_dir_buttons, vtg_dir)

    def _update_pictographs_vtg_dir(self, vtg_dir: VTG_Directions) -> None:
        pictograph = self.graph_editor.GE_pictograph_view.get_current_pictograph()
        for motion in pictograph.motions.values():
            other_motion = pictograph.get.other_motion(motion)
            if motion.check.is_dash() or motion.check.is_static():
                if other_motion.check.is_shift():
                    pictograph.vtg_dir = vtg_dir
                    if vtg_dir == SAME:
                        self._update_pictograph_prop_rot_dir_from_vtg_dir_setting(
                            motion, other_motion.prop_rot_dir
                        )
                    elif vtg_dir == OPP:
                        self._update_pictograph_prop_rot_dir_from_vtg_dir_setting(
                            motion,
                            self._opposite_prop_rot_dir(other_motion.prop_rot_dir),
                        )

    def _update_pictograph_prop_rot_dir_from_vtg_dir_setting(
        self, motion: "Motion", prop_rot_dir: PropRotDir
    ) -> None:
        motion.prop_rot_dir = prop_rot_dir
        pictograph_dict = {motion.color.value + "_" + PROP_ROT_DIR: prop_rot_dir}
        motion.pictograph.updater.update_pictograph(pictograph_dict)

    def _update_button_states(
        self, buttons: list[VtgDirButton], active_direction: VTG_Directions
    ) -> None:
        for button in buttons:
            if button.direction == active_direction:
                button.press()
                self.vtg_state[button.direction] = True
            else:
                button.unpress()
                self.vtg_state[button.direction] = False

    def _opposite_prop_rot_dir(self, prop_rot_dir: PropRotDir) -> PropRotDir:
        return {
            CLOCKWISE: COUNTER_CLOCKWISE,
            COUNTER_CLOCKWISE: CLOCKWISE,
        }.get(prop_rot_dir, prop_rot_dir)

    def update_visibility_based_on_motion(
        self,
        new_turns,
        attribute_value: Union[Color, MotionType, LeadStates],
    ) -> None:
        if attribute_value in [PRO, ANTI]:
            return
        if new_turns > 0:
            if self.previous_turns == 0:
                self.show_vtg_dir_buttons()
                if not self.vtg_state[SAME] and not self.vtg_state[OPP]:
                    self.vtg_state[SAME] = True
                    self.same_button.press()
                    self.same_button.update_state_dict(self.vtg_state, True)
                if self.vtg_state[SAME]:
                    self.same_button.press()
                    self.same_button.update_state_dict(self.vtg_state, True)
                elif self.vtg_state[OPP]:
                    self.opp_button.press()
                    self.opp_button.update_state_dict(self.vtg_state, True)
                self.previous_turns = new_turns
        elif new_turns == 0:
            self.previous_turns = 0
            self.hide_vtg_dir_buttons()

    def unpress_vtg_buttons(self) -> None:
        self.same_button.unpress()
        self.opp_button.unpress()

    def resize_vtg_dir_buttons(self) -> None:
        header_height = self.turns_box.header_widget.header_label.height()
        for button in self.vtg_dir_buttons:
            button_height = header_height
            button_width = button_height
            button.setFixedSize(button_width, button_height)
            icon_size = int(button_height * 0.8)
            button.setIconSize(QSize(icon_size, icon_size))