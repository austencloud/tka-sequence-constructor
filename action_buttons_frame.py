from PyQt6.QtWidgets import QPushButton, QFrame
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import QSize
from settings import GRAPHBOARD_SCALE
from PyQt6.QtWidgets import QVBoxLayout

class Action_Buttons_Frame(QFrame):
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window

        button_font = QFont('Helvetica', 14)
        button_size = int(80 * GRAPHBOARD_SCALE)
        icon_size = QSize(int(60 * GRAPHBOARD_SCALE), int(60 * GRAPHBOARD_SCALE))
        self.action_buttons_layout = QVBoxLayout()
        
        # Configuration for each button
        buttons_config = [
            ("images/icons/update_locations.png", "Update Position", 
             lambda: self.main_widget.json_manager.update_optimal_locations_in_json(*self.main_widget.graphboard_view.get_current_arrow_positions())),
            ("images/icons/delete.png", "Delete", 
             lambda: self.main_widget.arrow_manager.delete_arrow(self.main_widget.graphboard_scene.selectedItems())),
            ("images/icons/rotate_right.png", "Rotate Right", 
             lambda: self.main_widget.arrow_manager.rotate_arrow('right', self.main_widget.graphboard_scene.selectedItems())),
            ("images/icons/rotate_left.png", "Rotate Left", 
             lambda: self.main_widget.arrow_manager.rotate_arrow('left', self.main_widget.graphboard_scene.selectedItems())),
            ("images/icons/mirror.png", "Mirror", 
             lambda: self.main_widget.arrow_manager.mirror_arrow(self.main_widget.graphboard_scene.selectedItems())),
            ("images/icons/swap.png", "Swap Colors", 
             lambda: self.main_widget.arrow_manager.swap_colors(self.main_widget.graphboard_scene.selectedItems())),
            ("images/icons/select_all.png", "Select All", 
             lambda: self.main_widget.graphboard_view.select_all_items()),
            ("images/icons/add_to_sequence.png", "Add to Sequence", 
             lambda: self.main_widget.sequence_view.add_to_sequence(self.main_widget.graphboard_view))
        ]

        # Function to create a configured button
        def create_configured_button(icon_path, tooltip, on_click):
            button = QPushButton(QIcon(icon_path), "")
            button.setToolTip(tooltip)
            button.setFont(button_font)
            button.setFixedSize(button_size, button_size)
            button.setIconSize(icon_size)
            button.clicked.connect(on_click)
            return button

        # Create and add buttons to the layout
        for icon, tooltip, action in buttons_config:
            button = create_configured_button(icon, tooltip, action)
            self.action_buttons_layout.addWidget(button)
            
        self.main_window.action_buttons_layout = self.action_buttons_layout # passes the layout to the main window
