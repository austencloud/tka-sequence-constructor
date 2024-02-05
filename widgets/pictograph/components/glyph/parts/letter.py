from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsRectItem
from PyQt6.QtGui import QPen
from .utils import load_svg_item

from Enums import LetterType
from typing import TYPE_CHECKING

from constants import Type1, Type2, Type3, Type4, Type5, Type6

if TYPE_CHECKING:
    from ..glyph import GlyphManager

# Common base path for SVG files
SVG_BASE_PATH = "images/letters_trimmed"

# Mapping of letter types to SVG paths
SVG_PATHS = {
    Type1: f"{SVG_BASE_PATH}/Type1/{{letter}}.svg",
    Type2: f"{SVG_BASE_PATH}/Type2/{{letter}}.svg",
    Type3: f"{SVG_BASE_PATH}/Type2/{{letter[0]}}.svg",
    Type4: f"{SVG_BASE_PATH}/Type4/{{letter}}.svg",
    Type5: f"{SVG_BASE_PATH}/Type4/{{letter[0]}}.svg",
    Type6: f"{SVG_BASE_PATH}/Type6/{{letter}}.svg",
}

class LetterHandler:
    def __init__(self, glyph: "GlyphManager") -> None:
        self.glyph = glyph
        self.letter_item = QGraphicsSvgItem(self.glyph)
        self.renderer = None

    def render(self) -> None:
        if not self.glyph.pictograph.letter:
            return
        letter_type = LetterType.get_letter_type(self.glyph.pictograph.letter)
        svg_path = SVG_PATHS.get(letter_type, "")
        svg_path = svg_path.format(letter=self.glyph.pictograph.letter)
        self.renderer = QSvgRenderer(svg_path)
        if self.renderer.isValid():
            self.letter_item.setSharedRenderer(self.renderer)

    def position_letter(self) -> None:
        x = int(self.letter_item.boundingRect().height() / 2)
        y = int(
            self.glyph.pictograph.height()
            - (self.letter_item.boundingRect().height() * 1.5)
        )
        self.letter_item.setPos(x, y)
