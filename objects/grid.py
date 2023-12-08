from typing import TYPE_CHECKING, List, Dict, Union
from xml.etree import ElementTree as ET
from PyQt6.QtCore import QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtGui import QTransform


from settings.string_constants import (
    GRID_DIR,
    NORTH,
    EAST,
    SOUTH,
    WEST,
    NORTHEAST,
    SOUTHEAST,
    SOUTHWEST,
    NORTHWEST,
)

if TYPE_CHECKING:
    from widgets.graph_editor.object_panel.arrowbox.arrowbox import ArrowBox
    from widgets.graph_editor.object_panel.propbox.propbox import PropBox
    from widgets.graph_editor.pictograph.pictograph import Pictograph


class GridItem(QGraphicsSvgItem):
    def __init__(self, path) -> None:
        super().__init__(path)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setZValue(-1)

    def mousePressEvent(self, event) -> None:
        event.ignore()
        
    def mouseMoveEvent(self, event) -> None:
        event.ignore()
        
    def mouseReleaseEvent(self, event) -> None:
        event.ignore()
        

class Grid:
    def __init__(self, grid_scene: Union["ArrowBox", "PropBox", "Pictograph"]) -> None:
        self.svg_paths = {
            "center_point": f"{GRID_DIR}grid_center_point.svg",
            "hand_points": f"{GRID_DIR}grid_hand_points.svg",
            "layer2_points": f"{GRID_DIR}grid_layer2_points.svg",
            "outer_points": f"{GRID_DIR}grid_outer_points.svg",
        }

        self.items: Dict[str, GridItem] = {}
        for key, path in self.svg_paths.items():
            item = GridItem(path)
            grid_scene.addItem(item)
            self.items[key] = item
        self.grid_scene = grid_scene

    def setPos(self, position: QPointF) -> None:
        for item in self.items.values():
            item.setPos(position)

    def scale_grid(self, scale_factor: float) -> None:
        # Determine the center point of the grid layout before scaling
        grid_center = QPointF(self.grid_scene.width() / 2, self. grid_scene.height() / 2)
        
        for item in self.items.values():
            item.setTransform(QTransform())

            item_center = item.boundingRect().center()
            transform = QTransform()
            transform.translate(item_center.x(), item_center.y())
            transform.scale(scale_factor, scale_factor)
            transform.translate(-item_center.x(), -item_center.y())
            item.setTransform(transform)

            relative_pos = (item.pos() - grid_center) * scale_factor
            new_pos = grid_center + relative_pos - item_center * scale_factor
            item.setPos(new_pos)


    def toggle_element_visibility(self, element_id: str, visible: bool):
        if element_id in self.items:
            self.items[element_id].setVisible(visible)
        else:
            raise ValueError(f"Element with id '{element_id}' not found.")

    def get_circle_coordinates(self, circle_id: str) -> Union[QPointF, None]:
        # Determine which SVG file contains the circle based on its ID
        svg_file_path = self._determine_svg_file_path(circle_id)
        if not svg_file_path:
            return None

        # Read and parse the SVG file
        with open(svg_file_path, "r") as svg_file:
            svg_content = svg_file.read()

        root = ET.fromstring(svg_content)
        namespace = "{http://www.w3.org/2000/svg}"
        circle_element = root.find(f".//{namespace}circle[@id='{circle_id}']")
        if circle_element is not None:
            cx = float(circle_element.attrib["cx"])
            cy = float(circle_element.attrib["cy"])
            return QPointF(cx, cy)
        else:
            return None

    def _determine_svg_file_path(self, circle_id: str) -> str:
        # Logic to determine which SVG file to read based on the circle_id
        if "hand" in circle_id:
            return self.svg_paths["hand_points"]
        elif "layer2" in circle_id:
            return self.svg_paths["layer2_points"]
        elif "outer" in circle_id:
            return self.svg_paths["outer_points"]
        elif "center" in circle_id:
            return self.svg_paths["center_point"]
        return ""

    def init_points(
        self, point_names: List[str], constants: List[str]
    ) -> Dict[str, QPointF]:
        return {
            constant: self.get_circle_coordinates(point_name)
            for point_name, constant in zip(point_names, constants)
        }

    def init_center(self) -> None:
        self.center: QPointF = self.get_circle_coordinates("center_point")

    def init_handpoints(self) -> None:
        point_names = ["n_hand_point", "e_hand_point", "s_hand_point", "w_hand_point"]
        constants = [NORTH, EAST, SOUTH, WEST]
        self.handpoints: Dict[str, QPointF] = self.init_points(point_names, constants)

    def init_layer2_points(self) -> None:
        point_names = [
            "ne_layer2_point",
            "se_layer2_point",
            "sw_layer2_point",
            "nw_layer2_point",
        ]
        constants = [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST]
        self.layer2_points: Dict[str, QPointF] = self.init_points(
            point_names, constants
        )

    def mousePressEvent(self, event) -> None:
        event.ignore()

    def mouseMoveEvent(self, event) -> None:
        event.ignore()

    def mouseReleaseEvent(self, event) -> None:
        event.ignore()
