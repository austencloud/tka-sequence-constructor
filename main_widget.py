import os
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QGraphicsScene, QGraphicsView, QLabel, QFrame, QWidget
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QEvent
from objects.arrow import Arrow
from objects.staff import Staff
from objects.grid import Grid
from managers.arrow_manager import Arrow_Manager
from managers.staff_manager import Staff_Manager
from managers.svg_manager import Svg_Manager
from managers.json_manager import Json_Manager
from managers.sequence_manager import Sequence_Manager
from views.graphboard_view import Graphboard_View
from views.arrowbox_view import ArrowBox_View
from views.propbox_view import PropBox_View
from generator import Pictograph_Generator
from info_tracker import Info_Tracker
from exporter import Exporter
from pictograph_selector import Pictograph_Selector
from init.init_letter_buttons import Init_Letter_Buttons
from init.init_action_buttons import Init_Action_Buttons
from init.init_arrowbox import Init_ArrowBox
from init.init_layout import Init_Layout
from init.init_propbox import Init_PropBox
from init.init_sequence_scene import Init_Sequence_Scene
from key_bindings import Key_Bindings
from settings import *

class Main_Widget(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        
        self.main_window = main_window
        self.arrows = []
        self.main_widget = self
        self.exporter = None
        self.sequence_manager = None
        self.graphboard_view = None

        self.key_bindings = Key_Bindings()
        self.graphboard_scene = QGraphicsScene()
        self.svg_manager = Svg_Manager()
        self.staff_manager = Staff_Manager(self.graphboard_scene)
        self.arrow_manager = Arrow_Manager(None, self.graphboard_view, self.staff_manager)
        self.json_manager = Json_Manager(self.graphboard_scene)
        self.info_label = QLabel(self.main_window)
        self.info_tracker = Info_Tracker(None, self.info_label, self.staff_manager, self.json_manager)
        self.grid = Grid('images\\grid\\grid.svg')
        self.exporter = Exporter(self.graphboard_view, self.graphboard_scene, self.staff_manager, self.grid)
        self.graphboard_view = Graphboard_View(self.graphboard_scene, self.grid, self.info_tracker, self.staff_manager, self.svg_manager, self.arrow_manager, self, None, self.sequence_manager, self.exporter, self.json_manager)
       
        Init_Layout(self, self.main_window)

        self.generator = Pictograph_Generator(self.staff_manager, self.graphboard_view, self.graphboard_scene, self.info_tracker, self.main_window, self, self.exporter, self.json_manager, self.grid)
        self.arrow_manager.connect_to_graphboard(self.graphboard_view)
        self.info_tracker.connect_graphboard_view(self.graphboard_view)
        self.staff_manager.connect_info_tracker(self.info_tracker)
        
        Init_ArrowBox(self, main_window)
        Init_PropBox(self, main_window, self.staff_manager)
        
        self.staff_manager.connect_grid(self.grid)
        self.staff_manager.connect_graphboard_view(self.graphboard_view)
        self.staff_manager.connect_propbox_view(self.propbox_view)
        self.staff_manager.init_graphboard_staffs(self.graphboard_view)
        self.staff_manager.init_propbox_staffs(self.propbox_scene)
        
        Init_Action_Buttons(self, self.main_window)
        self.connect_info_tracker()
        Init_Sequence_Scene(self)
        Init_Letter_Buttons(self, self.main_window)

        self.setFocus()

        self.arrow_manager.connect_info_tracker(self.info_tracker)
        self.graphboard_view.connect_generator(self.generator)
        self.main_window.installEventFilter(self)

### CONNECTORS ###

    def connect_info_tracker(self):
        self.main_window.info_layout.addWidget(self.info_label)

### EVENTS ###

    def show_pictograph_selector(self, letter):
        # Fetch all possible combinations for the clicked letter
        # Assuming self.generator.letters is the dictionary containing all combinations
        combinations = self.generator.letters.get(letter, [])
        
        if not combinations:
            print(f"No combinations found for letter {letter}")
            return
        
        # Create and show the Pictograph_Selector dialog
        dialog = Pictograph_Selector(combinations, letter, self.graphboard_view, self)
        result = dialog.exec()
        
        if result == QDialog.accepted:
            # TODO: Handle the selected pictograph
            pass


    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.KeyPress:  # Adjusted to the new enumeration access method
            self.key_bindings.keyPressEvent(event, self.graphboard_view)
            return True
        return super().eventFilter(source, event)