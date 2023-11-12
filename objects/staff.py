from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import Qt, QPointF
from settings.numerical_constants import (
    STAFF_WIDTH,
    STAFF_LENGTH,
)
from settings.string_constants import (
    STAFF_ATTRIBUTES,
    COLOR,
    LOCATION,
    LAYER,
    NORTH,
    SOUTH,
    WEST,
    EAST,
    HORIZONTAL,
    VERTICAL,
    STAFF_SVG_FILE_PATH,
    STAFF_DIR,
    RED,
    BLUE,
    COLOR_MAP,
    CLOCKWISE,
    RED_HEX,
    BLUE_HEX,
)
import logging
import re

logging.basicConfig(
    filename="logs/staff.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


class Staff(QGraphicsSvgItem):
    def __init__(self, graphboard, attributes):
        super().__init__()
        self._setup(graphboard, attributes)

    ### SETUP ###

    def _setup(self, graphboard, attributes):
        self.svg_file = STAFF_SVG_FILE_PATH
        self._setup_svg_renderer(self.svg_file)
        self._setup_attributes(graphboard, attributes)
        self._setup_graphics_flags()

    def _setup_attributes(self, graphboard, attributes):
        self.graphboard = graphboard
        
        self.drag_offset = QPointF(0, 0)
        self.previous_location = None
        
        self.arrow = None
        self.ghost_staff = None

        self.color = None
        self.location = None
        self.layer = None

        if attributes:
            self.set_attributes_from_dict(attributes)
            self.update_appearance()
            
        self.center = self.get_staff_center()

    def _setup_graphics_flags(self):
        self.setFlags(
            QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsSvgItem.GraphicsItemFlag.ItemSendsGeometryChanges
            | QGraphicsSvgItem.GraphicsItemFlag.ItemIsFocusable
        )
        self.setTransformOriginPoint(self.center)

    def _setup_svg_renderer(self, svg_file):
        self.renderer = QSvgRenderer(svg_file)
        self.setSharedRenderer(self.renderer)

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event):
        self.setSelected(True)
        self.ghost_staff = self.graphboard.ghost_staffs[self.color]
        self.ghost_staff.update(self)
        self.graphboard.addItem(self.ghost_staff)
        self.ghost_staff.arrow = self.arrow
        self.graphboard.staffs.append(self.ghost_staff)
        self.graphboard.staffs.remove(self)
        self.graphboard.staff_positioner.update()
        self.graphboard.staffs.append(self)
        for item in self.graphboard.items():
            if item != self:
                item.setSelected(False)

        self.drag_start_pos = self.pos()
        self.drag_offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            scene_event_pos = self.mapToScene(event.pos())
            view_event_pos = self.graphboard.view.mapFromScene(scene_event_pos)
            in_view = self.graphboard.view.rect().contains(view_event_pos)
            new_pos = event.scenePos() - self.get_staff_center()
            self.setPos(new_pos)

            new_location = self.get_closest_handpoint(event.scenePos())[1]
            print(new_location)
            
            if new_location != self.previous_location:
                if in_view:   
                    self.update_for_new_location(event, new_location)

    def update_for_new_location(self, event, new_location):
        self.location = new_location
        self.attributes[LOCATION] = new_location

        self.update_rotation()
        self.ghost_staff.update(self)


        self.ghost_staff.set_attributes_from_dict(self.attributes)
        self.ghost_staff.update_appearance()
        self.arrow.set_attributes_from_staff(self)
        self.arrow.update_appearance()

        self.update_appearance()

        self.ghost_staff.update(self)
        self.graphboard.staffs.remove(self)
        self.graphboard.update()
        self.graphboard.staffs.append(self)


    def mouseReleaseEvent(self, event):
        self.graphboard.removeItem(self.ghost_staff)
        self.graphboard.staffs.remove(self.ghost_staff)
        self.ghost_staff.arrow = None
        self.ghost_staff = None
        self.graphboard.arrow_positioner.update() 
        self.finalize_staff_drop(self, event)

    def finalize_staff_drop(self, staff, event):
        # Calculate closest handpoint and new location
        closest_handpoint, new_location = staff.get_closest_handpoint(event.scenePos())

        staff.attributes[LOCATION] = new_location
        staff.location = new_location

        # Update staff attributes and appearance
        staff.update_appearance()

        # Position the staff at the closest handpoint
        staff.setPos(closest_handpoint)

        # Update associated arrow if any
        if staff.arrow:
            staff.arrow.set_attributes_from_staff(staff)
            staff.arrow.update_appearance()

        # Hide ghost staff
        self.graphboard.ghost_staffs[staff.color].hide()

        staff.previous_location = new_location

        
    ### UPDATERS ###

    def update(self, attributes):
        self.set_attributes_from_dict(attributes)
        self.update_appearance()

    def update_rotation(self):
        angle = self.get_rotation_angle()
        self.setRotation(angle)

    def update_position(self, event):
        offset = self.get_staff_center()
        new_pos = QPointF(
            event.scenePos().x() + offset.x(), event.scenePos().y() + offset.y()
        )
        self.setPos(new_pos)

    def update_staff_orientation(self, mouse_pos):
        closest_handpoint, closest_location = self.get_closest_handpoint(mouse_pos)
        self.update_axis(closest_location)
        self.update_appearance()
        self.apply_rotation()

    def update_axis(self, location):
        if self.layer == 1:
            self.axis = VERTICAL if location in [NORTH, SOUTH] else HORIZONTAL
        elif self.layer == 2:
            self.axis = HORIZONTAL if location in [NORTH, SOUTH] else VERTICAL

    def update_color(self):
        new_svg_data = self.set_svg_color(self.color)
        self.renderer.load(new_svg_data)
        self.setSharedRenderer(self.renderer)

    def update_appearance(self):
        self.update_color()
        if self.location:
            self.update_axis(self.location)
        else:
            logging.warning("Staff has no location")
            
        self.update_axis(self.location)
        self.set_rotation_from_axis()

    def update_svg(self, svg_file):
        self.svg_file = svg_file
        self._setup_svg_renderer(svg_file)
        self.set_svg_color(self.color)

    def update_dict_attr_from_object(self):
        for attr in STAFF_ATTRIBUTES:
            self.attributes[attr] = getattr(self, attr)

    def update_staff_orientation(self, mouse_pos):
        closest_handpoint, closest_location = self.get_closest_handpoint(mouse_pos)
        previous_axis = self.axis
        self.update_axis(closest_location)
        self.update_appearance()

        # If the orientation changed, adjust the position to maintain alignment
        if self.axis != previous_axis:
            staff_center = self.get_center()
            self.setPos(mouse_pos - staff_center)

        self.apply_rotation()

    def set_attributes_from_dict(self, attributes):
        self.color = attributes.get(COLOR, None)
        self.location = attributes.get(LOCATION, None)
        self.layer = attributes.get(LAYER, None)

        self.attributes = {
            COLOR: attributes.get(COLOR, None),
            LOCATION: attributes.get(LOCATION, None),
            LAYER: attributes.get(LAYER, None),
        }

    def set_transform_origin_to_center(self):
        self.center = self.get_staff_center()
        self.setTransformOriginPoint(self.center)

    def set_attributes_from_arrow(self, arrow):
        new_dict = {
            COLOR: arrow.color,
            LOCATION: arrow.end_location,
            LAYER: 1,
        }
        self.attributes.update(new_dict)
        self.color = arrow.color
        self.location = arrow.end_location
        self.axis = VERTICAL if self.location in [NORTH, SOUTH] else HORIZONTAL
        self.layer = 1
        self.update_appearance()

    def set_rotation_from_axis(self):
        if self.axis == VERTICAL:
            self.current_position = self.pos()
            self.setTransformOriginPoint(self.get_staff_center())
            self.setRotation(90)
        else:
            self.setRotation(0)

    ### GETTERS ###

    def get_rotation_angle(self):
        location_to_angle = self.get_location_to_angle()
        return location_to_angle

    def get_location_to_angle(self):
        if self.location == NORTH or self.location == SOUTH:
            return {
                    NORTH: 90,
                    SOUTH: 270,
                }.get(self.location, {})
        elif self.location == EAST or self.location == WEST:
            return {
                    WEST: 0,
                    EAST: 180,
                }.get(self.location, {})
        else:
            return {}
        
    def get_staff_center(self):
        if self.axis == VERTICAL:
            return QPointF((STAFF_WIDTH / 2), (STAFF_LENGTH / 2))
        elif self.axis == HORIZONTAL:
            return QPointF((STAFF_LENGTH / 2), (STAFF_WIDTH / 2))

    def get_closest_handpoint(self, mouse_pos):
        closest_distance = float("inf")
        closest_handpoint = None
        closest_location = None
        for location, point in self.graphboard.grid.handpoints.items():
            distance = (point - mouse_pos).manhattanLength()
            if distance < closest_distance:
                closest_distance = distance
                closest_handpoint = point
                closest_location = location
        return closest_handpoint, closest_location

    def get_attributes(self):
        return {attr: getattr(self, attr) for attr in STAFF_ATTRIBUTES}

    def get_svg_file(self):
        svg_file = f"{STAFF_DIR}staff.svg"
        return svg_file


    ### HELPERS ###

    def apply_rotation(self):
        if self.axis == VERTICAL:
            self.setRotation(90)
        else:
            self.setRotation(0)

    def create_staff_dict_from_arrow(self, arrow):
        staff_dict = {COLOR: arrow.color, LOCATION: arrow.end_location, LAYER: 1}
        return staff_dict

    def swap_axis(self):
        if self.axis == VERTICAL:
            self.axis = HORIZONTAL
        else:
            self.axis = VERTICAL
        self.set_rotation_from_axis()

    def set_svg_color(self, new_color):
        color_map = {RED: RED_HEX, BLUE: BLUE_HEX}
        new_hex_color = color_map.get(new_color)

        with open(self.svg_file, CLOCKWISE) as f:
            svg_data = f.read()

        style_tag_pattern = re.compile(
            r"\.st0{fill\s*:\s*(#[a-fA-F0-9]{6})\s*;}", re.DOTALL
        )
        match = style_tag_pattern.search(svg_data)

        if match:
            old_color = match.group(1)
            svg_data = svg_data.replace(old_color, new_hex_color)
        return svg_data.encode("utf-8")

class RedStaff(Staff):
    def __init__(self, scene, dict):
        super().__init__(scene, dict)
        self.setSharedRenderer(self.renderer)



class BlueStaff(Staff):
    def __init__(self, scene, dict):
        super().__init__(scene, dict)
        self.setSharedRenderer(self.renderer)

