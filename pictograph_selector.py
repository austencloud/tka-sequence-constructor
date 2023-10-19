from PyQt6.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from views.pictograph_view import Pictograph_View

class Pictograph_Selector(QDialog):
    def __init__(self, combinations, letter, main_widget):
        super().__init__(main_widget)
        self.setWindowTitle(f"{letter} Variations:")
        
        layout = QVBoxLayout()
        grid_layout = QGridLayout()
        letter_label = QLabel(f"{letter} Variations:")
        letter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(20)
        letter_label.setFont(font)
        layout.addWidget(letter_label)
        
        
        row = 0
        col = 0
        for i, combination in enumerate(combinations):
            pictograph = Pictograph_View(main_widget)
            pictograph.populate_pictograph(combination)
            grid_layout.addWidget(pictograph, row, col)
                    
            col += 1
            if col >= 4:
                col = 0
                row += 1
        
        layout.addLayout(grid_layout)
        self.setLayout(layout)

    def select_pictograph(self):
        # TODO: Logic to get the selected pictograph and close the dialog
        self.accept()
        

