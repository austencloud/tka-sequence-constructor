from typing import Dict, List, Tuple

import pandas as pd
from dataframes.dataframe_generators.base_dataframe_generator import (
    BaseDataFrameGenerator,
)

from constants import *
from utilities.TypeChecking.Letters import Type4_letters


class Type4Generator(BaseDataFrameGenerator):
    def __init__(self) -> None:
        super().__init__(Type4_letters)
        self.create_Type4_dataframes()

    def create_Type4_dataframes(self) -> pd.DataFrame:
        all_data = []
        for letter in self.letters:
            data = self.create_dataframe(letter)
            all_data.extend(data)
            print("Generated dataframes for letter:", letter)
        return pd.DataFrame(all_data)

    def create_dataframe(self, letter) -> List[Dict]:
        data = []
        if letter == "Λ":
            data = self.create_dataframes_for_Λ(letter)
        else:
            data += self.create_dataframes_for_letter(letter, DASH, STATIC)
            data += self.create_dataframes_for_letter(letter, STATIC, DASH)
        return data

    def create_dataframes_for_letter(self, letter, red_motion_type, blue_motion_type):
        dash_handpath_tuple_map = self.get_dash_tuple_map()

        data = []
        red_prop_rot_dir = "no_rot"
        blue_prop_rot_dir = "no_rot"
        for start_loc, end_loc in dash_handpath_tuple_map:
            if red_motion_type == STATIC:
                red_start_loc, red_end_loc = self.get_static_locations(
                    letter, start_loc, end_loc
                )
                blue_start_loc, blue_end_loc = start_loc, end_loc
            elif blue_motion_type == STATIC:
                blue_start_loc, blue_end_loc = self.get_static_locations(
                    letter, start_loc, end_loc
                )
                red_start_loc, red_end_loc = start_loc, end_loc
            else:
                red_start_loc, red_end_loc = start_loc, end_loc
                blue_start_loc, blue_end_loc = start_loc, end_loc

            start_pos, end_pos = self.get_Type1_start_and_end_pos(
                red_start_loc, red_end_loc, blue_start_loc, blue_end_loc
            )
            data.append(
                {
                    LETTER: letter,
                    START_POS: start_pos,
                    END_POS: end_pos,
                    BLUE_MOTION_TYPE: blue_motion_type,
                    BLUE_PROP_ROT_DIR: blue_prop_rot_dir,
                    BLUE_START_LOC: blue_start_loc,
                    BLUE_END_LOC: blue_end_loc,
                    RED_MOTION_TYPE: red_motion_type,
                    RED_PROP_ROT_DIR: red_prop_rot_dir,
                    RED_START_LOC: red_start_loc,
                    RED_END_LOC: red_end_loc,
                }
            )
        return data

    def create_dataframes_for_Λ(self, letter):
        data = []
        # Λ specific logic for dash and static hand locations
        dash_handpath_tuple_map = self.get_dash_tuple_map()
        for dash_start_loc, dash_end_loc in dash_handpath_tuple_map:
            # Create variations where dash and static hands are at different locations
            data += self.create_Λ_variations(letter, dash_start_loc, dash_end_loc)
        return data

    def create_Λ_variations(self, letter, dash_start_loc, dash_end_loc):
        variations = []
        static_locs = self.get_static_locations_for_Λ(dash_start_loc, dash_end_loc)

        for static_loc in static_locs:
            # Dash motion variations
            variations.append(
                self.create_variation_dict(
                    letter,
                    dash_start_loc,
                    dash_end_loc,
                    static_loc,
                    static_loc,
                    DASH,
                    STATIC,
                )
            )

            # Static motion variations
            variations.append(
                self.create_variation_dict(
                    letter,
                    static_loc,
                    static_loc,
                    dash_start_loc,
                    dash_end_loc,
                    STATIC,
                    DASH,
                )
            )

        return variations

    def get_static_locations_for_Λ(self, dash_start_loc, dash_end_loc) -> List[str]:
        """Gets valid static locs for Λ based on dash's start and end locs."""
        static_location_map = {
            (NORTH, SOUTH): [EAST, WEST],
            (EAST, WEST): [NORTH, SOUTH],
            (SOUTH, NORTH): [EAST, WEST],
            (WEST, EAST): [NORTH, SOUTH],
        }
        return static_location_map.get((dash_start_loc, dash_end_loc), [])

    def create_variation_dict(
        self,
        letter,
        red_start_loc,
        red_end_loc,
        blue_start_loc,
        blue_end_loc,
        red_motion_type,
        blue_motion_type,
    ):
        start_pos, end_pos = self.get_Type1_start_and_end_pos(
            red_start_loc, red_end_loc, blue_start_loc, blue_end_loc
        )
        return {
            LETTER: letter,
            START_POS: start_pos,
            END_POS: end_pos,
            BLUE_MOTION_TYPE: blue_motion_type,
            BLUE_PROP_ROT_DIR: "no_rot",
            BLUE_START_LOC: blue_start_loc,
            BLUE_END_LOC: blue_end_loc,
            RED_MOTION_TYPE: red_motion_type,
            RED_PROP_ROT_DIR: "no_rot",
            RED_START_LOC: red_start_loc,
            RED_END_LOC: red_end_loc,
        }

    def get_static_locations(
        self, letter, dash_start_loc, dash_end_loc
    ) -> Tuple[Locations]:
        if letter == "Φ":
            static_start_loc, static_end_loc = dash_start_loc, dash_start_loc
        elif letter == "Ψ":
            static_start_loc, static_end_loc = dash_end_loc, dash_end_loc
        elif letter == "Λ":
            pass
        return static_start_loc, static_end_loc


Type4Generator()
