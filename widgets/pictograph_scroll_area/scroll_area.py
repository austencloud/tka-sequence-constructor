from typing import TYPE_CHECKING, Dict, Union
from PyQt6.QtWidgets import (
    QScrollArea,
    QWidget,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt
from utilities.TypeChecking.TypeChecking import Letters
from widgets.pictograph_scroll_area.scroll_area_pictograph_factory import (
    ScrollAreaPictographFactory,
)
from ..ig_tab.ig_scroll.ig_pictograph import IGPictograph
from ..pictograph_scroll_area.scroll_area_section_manager import (
    ScrollAreaSectionManager,
)
from .scroll_area_display_manager import ScrollAreaDisplayManager
from .scroll_area_filter_manager import ScrollAreaFilterTabManager

if TYPE_CHECKING:
    from ..ig_tab.ig_tab import IGTab
    from ..option_picker_tab.option_picker_tab import OptionPickerTab
    from ..main_widget import MainWidget


class ScrollArea(QScrollArea):
    def __init__(
        self, main_widget: "MainWidget", parent_tab: Union["IGTab", "OptionPickerTab"]
    ) -> None:
        super().__init__(parent_tab)
        self.main_widget = main_widget
        self.parent_tab = parent_tab
        self.letters = self.main_widget.letters
        self.pictographs: Dict[Letters, IGPictograph] = {}
        self._setup_ui()
        self._setup_managers()

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_arrow_placements)
        # self.timer.start(1000)

    def _setup_managers(self) -> None:
        self.display_manager = ScrollAreaDisplayManager(self)
        self.filter_tab_manager = ScrollAreaFilterTabManager(self)
        self.section_manager = ScrollAreaSectionManager(self)
        self.pictograph_factory = ScrollAreaPictographFactory(self)

    def _setup_ui(self) -> None:
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.layout: QVBoxLayout = QVBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.container.setStyleSheet("background-color: #f2f2f2;")
        self.setWidget(self.container)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def update_pictographs(self) -> None:
        deselected_letters = self.pictograph_factory.get_deselected_letters()

        # Remove pictographs associated with deselected letters
        for letter in deselected_letters:
            self.pictograph_factory.remove_deselected_letter_pictographs(letter)

        # Update display after processing deselections
        self.display_manager.cleanup_unused_pictographs()
        self.section_manager.organize_pictographs_by_type()

    def _only_deselection_occurred(self, deselected_letters, selected_letters) -> bool:
        if not deselected_letters:
            return False
        if not selected_letters:
            return True

        current_pictograph_letters = {key.split("_")[0] for key in self.pictographs}

        return (
            len(deselected_letters) > 0
            and len(selected_letters) == len(current_pictograph_letters) - 1
        )

    def update_arrow_placements(self) -> None:
        for pictograph in self.pictographs.values():
            pictograph.arrow_placement_manager.update_arrow_placement()

    def resize_scroll_area(self) -> None:
        for section in self.section_manager.sections.values():
            section.resize_scroll_area_section()