from PyQt6.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout
from graph_editor.graphboard_view import Graphboard_View
from graph_editor.arrowbox_view import ArrowBox_View
from pictograph_generator import Pictograph_Generator
from graph_editor.propbox_view import PropBox_View
from graph_editor.info_tracker import Info_Tracker
from exporter import Exporter
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtGui import QPalette, QColor
from letter_buttons_frame import Letter_Buttons_Frame
from action_buttons_frame import Action_Buttons_Frame
class Graph_Editor_Widget(QWidget):
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window

        # Create the frame and set its style
        self.graph_editor_frame = QFrame()
        self.graph_editor_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.graph_editor_frame.setLineWidth(1)
        palette = self.graph_editor_frame.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
        self.graph_editor_frame.setPalette(palette)

        # Create a main horizontal layout for the graph_editor_frame
        frame_layout = QHBoxLayout(self.graph_editor_frame)

        # Create individual vertical layouts
        objectbox_layout = QVBoxLayout()  # For arrowbox and propbox
        graphboard_layout = QVBoxLayout()  # For the graph board view
        action_buttons_layout = QVBoxLayout()  # For action buttons
        info_tracker_layout = QVBoxLayout()  # For the info tracker
        
        # Create and add contents to the frame_layout
        self.graphboard_view = Graphboard_View(main_widget, self)
        self.exporter = Exporter(main_widget.staff_manager, main_widget.grid, self.graphboard_view)
        self.info_tracker = Info_Tracker(main_widget, self.graphboard_view)
        self.propbox_view = PropBox_View(main_widget)
        self.arrowbox_view = ArrowBox_View(main_widget, self.graphboard_view, self.info_tracker)
        self.pictograph_generator = Pictograph_Generator(main_widget, self.graphboard_view, self.info_tracker)
        self.letter_buttons_frame = Letter_Buttons_Frame(main_widget)
        self.action_buttons = Action_Buttons_Frame(main_widget)
        
        # Add widgets to the object box layout.
        objectbox_layout.addWidget(self.arrowbox_view)
        objectbox_layout.addWidget(self.propbox_view)

        # Add the graph board view to its layout
        graphboard_layout.addWidget(self.graphboard_view)

        # Add the action buttons frame to its layout
        action_buttons_layout.addWidget(self.action_buttons)  # self.action_buttons is an instance of Action_Buttons_Frame

        # Add the info tracker to its layout
        info_tracker_layout.addWidget(self.info_tracker.info_label)

        # Add the individual vertical layouts to the main horizontal layout
        frame_layout.addLayout(objectbox_layout)
        frame_layout.addLayout(graphboard_layout)
        frame_layout.addLayout(action_buttons_layout)
        frame_layout.addLayout(info_tracker_layout)

        self.graph_editor_frame.setLayout(frame_layout)  # This line is crucial.
        self.main_window.graph_editor_layout.addWidget(self.graph_editor_frame)
