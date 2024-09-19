from typing import TYPE_CHECKING
from utilities.path_helpers import get_images_and_data_path
from PyQt6.QtSvg import QSvgRenderer
from objects.arrow.arrow import Arrow
from data.constants import CLOCK, COUNTER, IN, OUT, FLOAT  # Add FLOAT here

if TYPE_CHECKING:
    from objects.graphical_object.svg_manager.graphical_object_svg_manager import (
        SvgManager,
    )


class ArrowSvgManager:
    def __init__(self, manager: "SvgManager"):
        self.manager = manager

    def update_arrow_svg(self, arrow: "Arrow") -> None:
        svg_file = self._get_arrow_svg_file(arrow)
        svg_data = self.manager.load_svg_file(svg_file)
        colored_svg_data = self.manager.color_manager.apply_color_transformations(
            svg_data, arrow.color
        )
        self._setup_arrow_svg_renderer(arrow, colored_svg_data)

    def _get_arrow_svg_file(self, arrow: "Arrow") -> str:
        start_ori = arrow.motion.start_ori
        if arrow.motion.motion_type == FLOAT:  # Handle the float case
            return get_images_and_data_path("images/arrows/float.svg")
        if start_ori in [IN, OUT]:
            turns = float(arrow.motion.turns)
            return get_images_and_data_path(
                f"images/arrows/{arrow.motion.motion_type}/from_radial/"
                f"{arrow.motion.motion_type}_{turns}.svg"
            )
        elif start_ori in [CLOCK, COUNTER]:
            return get_images_and_data_path(
                f"images/arrows/{arrow.motion.motion_type}/from_nonradial/"
                f"{arrow.motion.motion_type}_{float(arrow.motion.turns)}.svg"
            )

    def _setup_arrow_svg_renderer(self, arrow: "Arrow", svg_data: str) -> None:
        renderer = QSvgRenderer()
        renderer.load(svg_data.encode("utf-8"))
        arrow.setSharedRenderer(renderer)
        arrow.update()