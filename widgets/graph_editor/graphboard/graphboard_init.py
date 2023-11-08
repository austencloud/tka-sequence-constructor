from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QPen
from PyQt6.QtWidgets import QGraphicsView
from objects.grid import Grid
from objects.staff.staff import RedStaff, BlueStaff
from settings.numerical_constants import *
from settings.string_constants import *
from events.context_menu_handler import ContextMenuHandler
from utilities.manipulators import Manipulators
from utilities.export_handler import ExportHandler


class GraphboardInit:
    def __init__(self, graphboard):
        self.graphboard = graphboard
        self.init_view()
        self.init_grid()
        self.init_staffs()
        self.init_handlers()
        self.init_letterbox()
        self.init_quadrants()

    def init_view(self):
        view = QGraphicsView()
        view.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        view.setFixedSize(
            int(GRAPHBOARD_WIDTH * GRAPHBOARD_SCALE),
            int(GRAPHBOARD_HEIGHT * GRAPHBOARD_SCALE),
        )
        view.setScene(self.graphboard)
        view.scale(GRAPHBOARD_SCALE, GRAPHBOARD_SCALE)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.wheelEvent = lambda event: None
        self.graphboard.view = view

    def init_grid(self):
        grid = Grid(GRID_PATH)
        grid_width = grid.boundingRect().width()
        scene_width = self.graphboard.width()
        padding = (scene_width - grid_width) / 2
        grid_position = QPointF(padding, padding)
        grid.setPos(grid_position)
        self.graphboard.addItem(grid)
        grid.init_handpoints()
        self.graphboard.grid = grid
        self.graphboard.padding = padding

    def init_staffs(self):
        staffs = []

        red_staff_dict = {
            COLOR: RED,
            LOCATION: NORTH,
            LAYER: 1,
        }
        blue_staff_dict = {
            COLOR: BLUE,
            LOCATION: SOUTH,
            LAYER: 1,
        }

        self.graphboard.red_staff = RedStaff(self.graphboard, red_staff_dict)
        self.graphboard.blue_staff = BlueStaff(self.graphboard, blue_staff_dict)

        self.graphboard.addItem(self.graphboard.red_staff)
        self.graphboard.addItem(self.graphboard.blue_staff)

        staffs.extend([self.graphboard.red_staff, self.graphboard.blue_staff])
        self.graphboard.staffs = staffs
        self.graphboard.hide_all_staffs()

    def init_handlers(self):
        self.graphboard.manipulators = Manipulators(self.graphboard)
        self.graphboard.export_manager = ExportHandler(
            self.graphboard.grid, self.graphboard
        )
        self.graphboard.context_menu_manager = ContextMenuHandler(self.graphboard)
        self.graphboard.drag = self.graphboard.main_widget.drag

    def init_letterbox(self):
        self.graphboard.letters = self.graphboard.main_widget.letters
        self.graphboard.letter_renderers = {}
        self.graphboard.addItem(self.graphboard.letter_item)

    def init_quadrants(self):
        grid_center = self.graphboard.grid.get_circle_coordinates("center_point")

        self.graphboard.grid_center_x = grid_center.x() + self.graphboard.padding
        self.graphboard.grid_center_y = grid_center.y() + self.graphboard.padding

        self.graphboard.ne_boundary = (
            self.graphboard.grid_center_x,
            0,
            GRAPHBOARD_WIDTH,
            self.graphboard.grid_center_y,
        )
        self.graphboard.se_boundary = (
            self.graphboard.grid_center_x,
            self.graphboard.grid_center_y,
            GRAPHBOARD_WIDTH,
            GRAPHBOARD_HEIGHT,
        )
        self.graphboard.sw_boundary = (
            0,
            self.graphboard.grid_center_y,
            self.graphboard.grid_center_x,
            GRAPHBOARD_HEIGHT,
        )
        self.graphboard.nw_boundary = (
            0,
            0,
            self.graphboard.grid_center_x,
            self.graphboard.grid_center_y,
        )
