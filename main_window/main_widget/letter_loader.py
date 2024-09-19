from typing import TYPE_CHECKING
import pandas as pd
from Enums.letters import Letter
from data.constants import END_POS, IN, LETTER, START_POS
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class PictographDictLoader:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget

    def load_all_pictograph_dicts(self) -> dict[Letter, list[dict]]:
        csv_path = get_images_and_data_path("data\\PictographDataframe.csv")
        self.df = pd.read_csv(csv_path)
        self.df = self.df.sort_values(by=[LETTER, START_POS, END_POS])
        self.df = self.add_turns_and_ori_to_pictograph_dict(self.df)
        self.df = self.restructure_dataframe_for_new_json_format(self.df)
        letters = {
            self.get_letter_enum_by_value(letter_str): self.df[
                self.df[LETTER] == letter_str
            ].to_dict(orient="records")
            for letter_str in self.df[LETTER].unique()
        }
        # convert the turns to ints in the dict
        self._convert_turns_str_to_int_or_float(letters)
        return letters

    def _convert_turns_str_to_int_or_float(self, letters):
        for letter in letters:
            for motion in letters[letter]:
                motion["blue_attributes"]["turns"] = int(
                    motion["blue_attributes"]["turns"]
                )
                motion["red_attributes"]["turns"] = int(
                    motion["red_attributes"]["turns"]
                )

    def add_turns_and_ori_to_pictograph_dict(self, df: pd.DataFrame) -> pd.DataFrame:
        # Example logic for assigning turns and orientations; adjust according to your specific needs
        for index, row in df.iterrows():
            # Placeholder logic for turns and orientation assignments; replace with your actual logic
            df.at[index, "blue_turns"] = 0  # Assign turns as integer
            df.at[index, "red_turns"] = 0  # Assign turns as integer
            df.at[index, "blue_start_ori"] = IN  # Assuming IN is a predefined variable
            df.at[index, "red_start_ori"] = IN  # Assuming IN is a predefined variable
        return df

    def restructure_dataframe_for_new_json_format(
        self, df: pd.DataFrame
    ) -> pd.DataFrame:
        def nest_attributes(row, color_prefix):
            return {
                "motion_type": row[f"{color_prefix}_motion_type"],
                "start_ori": row[f"{color_prefix}_start_ori"],
                "prop_rot_dir": row[f"{color_prefix}_prop_rot_dir"],
                "start_loc": row[f"{color_prefix}_start_loc"],
                "end_loc": row[f"{color_prefix}_end_loc"],
                "turns": row[f"{color_prefix}_turns"],
            }

        df["blue_attributes"] = df.apply(
            lambda row: nest_attributes(row, "blue"), axis=1
        )
        df["red_attributes"] = df.apply(lambda row: nest_attributes(row, "red"), axis=1)

        # Drop the old, now unnecessary columns
        blue_columns = [
            "blue_motion_type",
            "blue_prop_rot_dir",
            "blue_start_loc",
            "blue_end_loc",
            "blue_turns",
            "blue_start_ori",
        ]
        red_columns = [
            "red_motion_type",
            "red_prop_rot_dir",
            "red_start_loc",
            "red_end_loc",
            "red_turns",
            "red_start_ori",
        ]
        df = df.drop(columns=blue_columns + red_columns)

        return df

    @staticmethod
    def get_letter_enum_by_value(letter_value: str) -> Letter:
        for letter in Letter.__members__.values():
            if letter.value == letter_value:
                return letter
        raise ValueError(f"No matching Letters enum for value: {letter_value}")
