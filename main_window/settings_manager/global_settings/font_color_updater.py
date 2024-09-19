from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget

if TYPE_CHECKING:
    from ...main_widget.learn_widget.base_classes.base_lesson_widget import (
        BaseLessonWidget,
    )
    from ...main_widget.top_builder_widget.sequence_builder.auto_builder.circular.circular_auto_builder_frame import (
        CircularAutoBuilderFrame,
    )
    from ...main_widget.top_builder_widget.sequence_builder.auto_builder.freeform.freeform_auto_builder_frame import (
        FreeformAutoBuilderFrame,
    )
    from ...main_widget.main_widget import MainWidget
    from splash_screen import SplashScreen


class FontColorUpdater:
    def update_main_widget_font_colors(
        self, main_widget: "MainWidget", bg_type: str
    ) -> None:
        font_color = self.get_font_color(bg_type)
        self._apply_widget_colors(main_widget, font_color)

    def update_splash_screen_font_colors(
        self, splash_screen: "SplashScreen", bg_type: str
    ) -> None:
        font_color = self.get_font_color(bg_type)
        splash_screen_labels = [
            splash_screen.title_label,
            splash_screen.currently_loading_label,
            splash_screen.created_by_label,
            splash_screen.progress_bar.percentage_label,
            splash_screen.progress_bar.loading_label,
        ]
        self._apply_font_colors(splash_screen_labels, font_color)

    @staticmethod
    def get_font_color(bg_type: str) -> str:
        """Return the appropriate font color based on the background type."""
        return (
            "black" if bg_type in ["Rainbow", "AuroraBorealis", "Aurora"] else "white"
        )

    @staticmethod
    def _apply_font_color(widget: QWidget, color: str) -> None:
        widget.setStyleSheet(f"color: {color};")

    def _apply_font_colors(self, widgets: list[QWidget], color: str) -> None:
        for widget in widgets:
            self._apply_font_color(widget, color)

    def _apply_widget_colors(self, main_widget: "MainWidget", font_color: str) -> None:
        """Apply font colors to all relevant sections of the main widget."""
        self._update_sequence_widget(main_widget, font_color)
        self._update_sequence_builder(main_widget, font_color)
        self._update_dictionary_widget(main_widget, font_color)
        self._update_learn_widget(main_widget, font_color)

    def _update_sequence_widget(
        self, main_widget: "MainWidget", font_color: str
    ) -> None:
        sequence_widget = main_widget.top_builder_widget.sequence_widget
        self._apply_font_colors(
            [sequence_widget.current_word_label, sequence_widget.difficulty_label],
            font_color,
        )

    def _update_sequence_builder(
        self, main_widget: "MainWidget", font_color: str
    ) -> None:
        sequence_builder = main_widget.top_builder_widget.sequence_builder

        manual_labels = [
            sequence_builder.manual_builder.start_pos_picker.choose_your_start_pos_label,
            sequence_builder.manual_builder.advanced_start_pos_picker.choose_your_start_pos_label,
        ]

        freeform_labels = self._get_freeform_builder_labels(
            sequence_builder.auto_builder.freeform_builder_frame
        )
        circular_labels = self._get_circular_builder_labels(
            sequence_builder.auto_builder.circular_builder_frame
        )

        self._apply_font_colors(
            manual_labels + freeform_labels + circular_labels, font_color
        )

    def _get_freeform_builder_labels(
        self, freeform_builder_frame: "FreeformAutoBuilderFrame"
    ) -> list[QWidget]:
        return [
            freeform_builder_frame.level_selector.level_label,
            freeform_builder_frame.length_adjuster.length_label,
            freeform_builder_frame.length_adjuster.length_value_label,
            freeform_builder_frame.turn_intensity_adjuster.intensity_label,
            freeform_builder_frame.turn_intensity_adjuster.intensity_value_label,
            freeform_builder_frame.continuous_rotation_toggle.continuous_label,
            freeform_builder_frame.continuous_rotation_toggle.random_label,
        ]

    def _get_circular_builder_labels(
        self, circular_builder_frame: "CircularAutoBuilderFrame"
    ) -> list[QWidget]:
        return [
            circular_builder_frame.level_selector.level_label,
            circular_builder_frame.length_adjuster.length_label,
            circular_builder_frame.length_adjuster.length_value_label,
            circular_builder_frame.turn_intensity_adjuster.intensity_label,
            circular_builder_frame.turn_intensity_adjuster.intensity_value_label,
            circular_builder_frame.rotation_type_toggle.halved_label,
            circular_builder_frame.rotation_type_toggle.quartered_label,
            circular_builder_frame.continuous_rotation_toggle.continuous_label,
            circular_builder_frame.continuous_rotation_toggle.random_label,
            circular_builder_frame.permutation_type_toggle.rotated_label,
            circular_builder_frame.permutation_type_toggle.mirrored_label,
        ]

    def _update_dictionary_widget(
        self, main_widget: "MainWidget", font_color: str
    ) -> None:
        dictionary = main_widget.dictionary_widget
        sort_widget = dictionary.browser.options_widget.sort_widget

        dictionary_labels = [
            sort_widget.sort_by_label,
            dictionary.preview_area.word_label,
            dictionary.preview_area.variation_number_label,
            dictionary.browser.progress_bar.loading_label,
            dictionary.browser.progress_bar.percentage_label,
        ]
        self._apply_font_colors(dictionary_labels, font_color)

        sort_widget.style_buttons()
        sort_widget.style_labels()
        dictionary.browser.nav_sidebar.set_styles()
        dictionary.preview_area.image_label.style_placeholder()
        dictionary.browser.initial_selection_widget.filter_choice_widget.resize_filter_choice_widget()

        for thumbnail_box in dictionary.browser.scroll_widget.thumbnail_boxes.values():
            self._apply_font_color(thumbnail_box.word_label, font_color)
            thumbnail_box.word_label.reload_favorite_icon()
            self._apply_font_color(thumbnail_box.variation_number_label, font_color)

    def _update_learn_widget(self, main_widget: "MainWidget", font_color: str) -> None:
        learn_widget = main_widget.learn_widget
        self._apply_font_color(learn_widget.lesson_selector.title_label, font_color)
        self._apply_font_colors(
            list(learn_widget.lesson_selector.description_labels.values()), font_color
        )

        lesson_widgets: list[BaseLessonWidget] = [
            learn_widget.lesson_1_widget,
            learn_widget.lesson_2_widget,
            learn_widget.lesson_3_widget,
        ]
        for lesson_widget in lesson_widgets:
            self._apply_font_color(lesson_widget.question_widget, font_color)
            self._apply_font_color(lesson_widget.progress_label, font_color)
            self._apply_font_color(lesson_widget.result_label, font_color)