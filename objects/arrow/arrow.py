from typing import Union
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QTransform
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent

from constants import *
from objects.arrow.arrow_attr_manager import ArrowAttrManager
from objects.arrow.arrow_mirror_manager import ArrowMirrorManager
from objects.arrow.arrow_mouse_event_handler import ArrowMouseEventHandler
from .arrow_location_manager import ArrowLocationCalculator
from .arrow_rot_angle_manager import ArrowRotAngleCalculator
from ..prop.prop import Prop

from ..graphical_object.graphical_object import GraphicalObject
from utilities.TypeChecking.TypeChecking import (
    Colors,
    Locations,
    MotionTypes,
    Turns,
    TYPE_CHECKING,
    Dict,
)


if TYPE_CHECKING:
    from ..motion.motion import Motion
    from .ghost_arrow import GhostArrow
    from ..prop.prop import Prop
    from widgets.graph_editor_tab.graph_editor_object_panel.arrowbox.arrowbox import (
        ArrowBox,
    )
    from widgets.pictograph.pictograph import Pictograph


class Arrow(GraphicalObject):
    svg_cache = {}

    def __init__(self, scene, arrow_dict, motion: "Motion") -> None:
        super().__init__(scene)
        self.scene: Pictograph | ArrowBox = scene
        self.motion: Motion = motion
        self.rot_angle_calculator = ArrowRotAngleCalculator(self)
        self.location_calculator = ArrowLocationCalculator(self)
        self.mirror_manager = ArrowMirrorManager(self)
        self.attr_manager = ArrowAttrManager(self)
        
        self.motion_type: MotionTypes = None
        self.ghost: GhostArrow = None
        self.is_svg_mirrored: bool = False
        self.color = arrow_dict[COLOR]
        self.prop: Prop = None
        self.is_ghost: bool = False
        self.loc: Locations = None

        # Create an instance of ArrowMouseEventHandler
        self.mouse_event_handler = ArrowMouseEventHandler(self)

    def setup_arrow(self, arrow_dict) -> None:
        self.motion_type = arrow_dict[MOTION_TYPE]
        self.turns = arrow_dict[TURNS]

        self.svg_file = self.svg_manager.get_arrow_svg_file(
            arrow_dict[MOTION_TYPE],
            arrow_dict[TURNS],
        )
        self.svg_manager.setup_svg_renderer(self.svg_file)
        self.setAcceptHoverEvents(True)
        self.attr_manager.update_attributes(arrow_dict)
        self.drag_offset = QPointF(0, 0)

    ### UPDATERS ###

    def set_drag_pos(self, new_pos: QPointF) -> None:
        self.setPos(new_pos)

    def set_arrow_transform_origin_to_center(self) -> None:
        self.setTransformOriginPoint(self.boundingRect().center())

    ### GETTERS ###

    def update_arrow(self, arrow_dict=None) -> None:
        if arrow_dict:
            self.attr_manager.update_attributes(arrow_dict)
            if not self.is_ghost and self.ghost:
                self.ghost.attr_manager.update_attributes(arrow_dict)

        if not self.is_ghost:
            self.ghost.transform = self.transform
        self.svg_manager.update_arrow_svg()
        self.mirror_manager.update_mirror()
        self.svg_manager.update_color()
        self.location_calculator.update_location()
        self.rot_angle_calculator.update_rotation()

    def adjust_position(self, adjustment) -> None:
        self.setPos(self.pos() + QPointF(*adjustment))

    ### DELETION ###

    def delete_arrow(self, keep_prop: bool = False) -> None:
        if self in self.scene.arrows.values():
            self.scene.removeItem(self)
            self.scene.removeItem(self.ghost)
            
            self.ghost.attr_manager.clear_attributes()
            self.prop.attr_manager.clear_attributes()
        if keep_prop:
            self.motion.attr_manager._change_motion_attributes_to_static()
        else:
            self.scene.removeItem(self.prop)

        self.scene.state_updater.update_pictograph()

    ### MOUSE EVENTS ###

    # Pass the events to the ArrowMouseEventHandler instance
    def mousePressEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_press(event)

    def mouseMoveEvent(self, event) -> None:
        self.mouse_event_handler.hand_mouse_move(event)

    def mouseReleaseEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_release(event)


