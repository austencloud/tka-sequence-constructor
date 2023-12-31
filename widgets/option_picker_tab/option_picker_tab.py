from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout
import pandas as pd

from constants import END_POS, START_POS
from .option_picker_scroll_area import OptionPickerScrollArea

from widgets.option_picker_tab.option_picker_filter_frame import OptionPickerFilterTab
if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class OptionPickerTab(QFrame):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.pictograph_df = self.load_and_sort_data("PictographDataFrame.csv")
        self.setup_ui()

    def setup_ui(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.filter_tab = OptionPickerFilterTab(self)
        self.scroll_area = OptionPickerScrollArea(self.main_widget, self)
        self.layout.addWidget(self.filter_tab)
        self.layout.addWidget(self.scroll_area)
        self.scroll_area.show()

    def resize_option_picker_tab(self) -> None:
        self.scroll_area.resize_option_picker_scroll()

    def load_and_sort_data(self, file_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            df.set_index([START_POS, END_POS], inplace=True)
            df.sort_index(inplace=True)
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error
