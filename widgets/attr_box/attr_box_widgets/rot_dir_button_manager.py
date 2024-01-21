from typing import TYPE_CHECKING, Callable, List, Union
from constants import (
    BLUE,
    CLOCKWISE,
    COLOR,
    COUNTER_CLOCKWISE,
    DASH,
    ICON_DIR,
    MOTION_TYPE,
    OPP,
    PROP_ROT_DIR,
    RED,
    SAME,
    STATIC,
)
from utilities.TypeChecking.MotionAttributes import PropRotDirs
from utilities.TypeChecking.TypeChecking import VtgDirections
from widgets.factories.button_factory.button_factory import ButtonFactory
from ...factories.button_factory.buttons.rot_dir_buttons import (
    VtgDirButton,
    PropRotDirButton,
)

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton

if TYPE_CHECKING:
    from widgets.attr_box.attr_box import AttrBox
    from objects.motion.motion import Motion


class RotDirButtonManager:
    def __init__(self, attr_box: "AttrBox") -> None:
        self.attr_box = attr_box

        self.prop_rot_dir_buttons: List[
            PropRotDirButton
        ] = self._setup_prop_rot_dir_buttons()
        self.vtg_dir_buttons: List[VtgDirButton] = self._setup_vtg_dir_buttons()
        self.buttons = self.prop_rot_dir_buttons + self.vtg_dir_buttons


    def _setup_vtg_dir_buttons(self) -> List[QPushButton]:
        self.same_button: VtgDirButton = ButtonFactory.create_vtg_dir_button(
            f"{ICON_DIR}same_direction.png", lambda: self._set_vtg_dir(SAME), SAME
        )
        self.opp_button: VtgDirButton = ButtonFactory.create_vtg_dir_button(
            f"{ICON_DIR}opp_direction.png", lambda: self._set_vtg_dir(OPP), OPP
        )
        self.same_button.unpress()
        self.opp_button.unpress()
        self.same_button.hide()
        self.opp_button.hide()
        return [self.same_button, self.opp_button]

    def _setup_prop_rot_dir_buttons(self) -> List[QPushButton]:
        self.cw_button: PropRotDirButton = ButtonFactory.create_prop_rot_dir_button(
            f"{ICON_DIR}clock/clockwise.png",
            lambda: self._set_prop_rot_dir(CLOCKWISE),
            CLOCKWISE,
        )
        self.ccw_button: PropRotDirButton = ButtonFactory.create_prop_rot_dir_button(
            f"{ICON_DIR}clock/counter_clockwise.png",
            lambda: self._set_prop_rot_dir(COUNTER_CLOCKWISE),
            COUNTER_CLOCKWISE,
        )
        self.cw_button.unpress()
        self.ccw_button.unpress()
        self.cw_button.hide()
        self.ccw_button.hide()
        return [self.cw_button, self.ccw_button]

    def _vtg_dir_callback(self, direction: VtgDirections) -> Callable:
        def callback() -> None:
            self._set_vtg_dir(direction)

        return callback

    def _prop_rot_dir_callback(self, direction: VtgDirections) -> Callable:
        def callback() -> None:
            self._set_prop_rot_dir(direction)

        return callback

    def _set_vtg_dir(self, vtg_dir: VtgDirections) -> None:
        self._update_pictographs_vtg_dir(vtg_dir)
        self._update_button_states(self.vtg_dir_buttons, vtg_dir)

    def _set_prop_rot_dir(self, prop_rot_dir: PropRotDirs) -> None:
        self._update_pictographs_prop_rot_dir(prop_rot_dir)
        self._update_button_states(self.prop_rot_dir_buttons, prop_rot_dir)

    def _update_pictographs_vtg_dir(self, vtg_dir: VtgDirections) -> None:
        for (
            pictograph
        ) in (
            self.attr_box.attr_panel.filter_tab.section.scroll_area.pictographs.values()
        ):
            for motion in pictograph.motions.values():
                other_motion = pictograph.motions[RED if motion.color == BLUE else BLUE]
                if motion.check.is_dash() or motion.check.is_static():
                    if other_motion.check.is_shift():
                        if motion.motion_type == self.attr_box.motion_type:
                            if vtg_dir == SAME:
                                self._update_pictograph_vtg_dir(
                                    motion, other_motion.prop_rot_dir
                                )
                            elif vtg_dir == OPP:
                                self._update_pictograph_vtg_dir(
                                    motion,
                                    self._opposite_prop_rot_dir(
                                        other_motion.prop_rot_dir
                                    ),
                                )

    def _update_pictographs_prop_rot_dir(self, prop_rot_dir: PropRotDirs) -> None:
        for (
            pictograph
        ) in (
            self.attr_box.attr_panel.filter_tab.section.scroll_area.pictographs.values()
        ):
            for motion in pictograph.motions.values():
                if motion.motion_type in [DASH, STATIC]:
                    if self.attr_box.attribute_type == MOTION_TYPE:
                        if motion.motion_type == self.attr_box.motion_type:
                            self._update_pictograph_prop_rot_dir(motion, prop_rot_dir)
                    elif self.attr_box.attribute_type == COLOR:
                        if motion.color == self.attr_box.color:
                            self._update_pictograph_prop_rot_dir(motion, prop_rot_dir)

    def _update_pictograph_vtg_dir(
        self, motion: "Motion", vtg_dir: VtgDirections
    ) -> None:
        motion.prop_rot_dir = vtg_dir
        pictograph_dict = {
            motion.color + "_" + PROP_ROT_DIR: vtg_dir,
        }
        motion.pictograph.updater.update_pictograph(pictograph_dict)

    def _update_pictograph_prop_rot_dir(
        self, motion: "Motion", prop_rot_dir: PropRotDirs
    ) -> None:
        motion.prop_rot_dir = prop_rot_dir
        pictograph_dict = {
            motion.color + "_" + PROP_ROT_DIR: prop_rot_dir,
        }
        motion.pictograph.updater.update_pictograph(pictograph_dict)

    def _update_button_states(
        self,
        buttons: List[Union[PropRotDirButton, VtgDirButton]],
        active_direction: VtgDirections,
    ) -> None:
        for button in buttons:
            if button.prop_rot_dir == active_direction:
                button.press()
            else:
                button.unpress()

    def show_vtg_dir_buttons(self) -> None:
        self._toggle_button_sets(self.prop_rot_dir_buttons, self.vtg_dir_buttons)

    def show_prop_rot_dir_buttons(self) -> None:
        self._toggle_button_sets(self.vtg_dir_buttons, self.prop_rot_dir_buttons)

    def _toggle_button_sets(
        self, buttons_to_hide: List[QPushButton], buttons_to_show: List[QPushButton]
    ) -> None:
        for hide_button, show_button in zip(buttons_to_hide, buttons_to_show):
            self._replace_and_toggle(hide_button, show_button)

    def _replace_and_toggle(
        self, button_to_hide: QPushButton, button_to_show: QPushButton
    ) -> None:
        layout = self.attr_box.header_widget.layout
        layout.replaceWidget(button_to_hide, button_to_show)
        button_to_hide.hide()
        button_to_show.show()

    def hide_buttons(self) -> None:
        for button in self.prop_rot_dir_buttons + self.vtg_dir_buttons:
            button.hide()

    def _opposite_prop_rot_dir(self, prop_rot_dir: PropRotDirs) -> PropRotDirs:
        return {
            CLOCKWISE: COUNTER_CLOCKWISE,
            COUNTER_CLOCKWISE: CLOCKWISE,
        }.get(prop_rot_dir, prop_rot_dir)