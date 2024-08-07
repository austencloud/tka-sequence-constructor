class SequencePropertiesChecker:
    def __init__(self, sequence):
        self.sequence = sequence
        self.ends_at_start_pos = False
        self.is_permutable = False
        self.is_rotational_permutation = False
        self.is_mirrored_permutation = False
        self.is_colorswapped_permutation = False

    def check_properties(self):
        if not self.sequence:
            return {
                "is_circular": False,
                "is_permutable": False,
                "is_rotational_permutation": False,
                "is_mirrored_permutation": False,
                "is_colorswapped_permutation": False,
            }

        self.ends_at_start_pos = self._check_ends_at_start_pos()
        self.is_permutable = self._check_is_permutable()
        self.is_rotational_permutation = self._check_is_rotational_permutation()
        self.is_mirrored_permutation = self._check_is_mirrored_permutation()
        self.is_colorswapped_permutation = self._check_is_colorswapped_permutation()

        return {
            "is_circular": self.ends_at_start_pos,
            "is_permutable": self.is_permutable,
            "is_rotational_permutation": self.is_rotational_permutation,
            "is_mirrored_permutation": self.is_mirrored_permutation,
            "is_colorswapped_permutation": self.is_colorswapped_permutation,
        }

    def _check_ends_at_start_pos(self) -> bool:
        start_position = self.sequence[0]["end_pos"]  # Assuming the first position
        current_position = self.sequence[-1]["end_pos"]  # Assuming the last position
        return current_position == start_position

    def _check_is_permutable(self) -> bool:
        start_position = self.sequence[0]["end_pos"].rstrip("0123456789")
        current_position = self.sequence[-1]["end_pos"].rstrip("0123456789")
        return current_position == start_position

    def _check_is_rotational_permutation(self) -> bool:
        letter_sequence = [entry["letter"] for entry in self.sequence if "letter" in entry]
        unique_letters = set(letter_sequence)
        for letter in unique_letters:
            occurrences = [i for i, x in enumerate(letter_sequence) if x == letter]
            if len(occurrences) > 1:
                for i in range(1, len(occurrences)):
                    prev = self.sequence[occurrences[i - 1]]
                    curr = self.sequence[occurrences[i]]
                    if not self._is_rotational_permutation(prev, curr):
                        return False
        return True

    def _is_rotational_permutation(self, prev, curr) -> bool:
        return (
            prev["blue_attributes"]["motion_type"] == curr["blue_attributes"]["motion_type"]
            and prev["blue_attributes"]["prop_rot_dir"] == curr["blue_attributes"]["prop_rot_dir"]
            and prev["red_attributes"]["motion_type"] == curr["red_attributes"]["motion_type"]
            and prev["red_attributes"]["prop_rot_dir"] == curr["red_attributes"]["prop_rot_dir"]
        )

    def _check_is_mirrored_permutation(self) -> bool:
        # Add logic to determine if the sequence is a mirrored permutation
        pass

    def _check_is_colorswapped_permutation(self) -> bool:
        # Add logic to determine if the sequence is a color-swapped permutation
        pass

    def get_properties(self):
        return {
            "is_circular": self.ends_at_start_pos,
            "is_permutable": self.is_permutable,
            "is_rotational_permutation": self.is_rotational_permutation,
            "is_mirrored_permutation": self.is_mirrored_permutation,
            "is_colorswapped_permutation": self.is_colorswapped_permutation,
        }
