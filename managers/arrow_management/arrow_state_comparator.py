
class ArrowStateComparator:
    def __init__(self, arrow_manager):
        self.arrow_manager = arrow_manager

    def compare_states(self, current_state, candidate_state):
        # Convert candidate_state to a format similar to current_state for easier comparison
        candidate_state_dict = {
            'arrows': []
        }

        for entry in candidate_state:
            if 'color' in entry and 'motion_type' in entry:
                candidate_state_dict['arrows'].append({
                    'color': entry['color'],
                    'motion_type': entry['motion_type'],
                    'rotation_direction': entry['rotation_direction'],
                    'quadrant': entry['quadrant'],
                    'turns': entry.get('turns', 0)
                })

        # Now compare the two states
        if len(current_state['arrows']) != len(candidate_state_dict['arrows']):
            return False

        for arrow in current_state['arrows']:
            matching_arrows = [candidate_arrow for candidate_arrow in candidate_state_dict['arrows']
                               if all(arrow.get(key) == candidate_arrow.get(key) for key in ['color', 'motion_type', 'quadrant', 'rotation_direction'])]
            if not matching_arrows:
                return False

        return True

    def find_optimal_locations(self, current_state, matching_letters):
        for variations in matching_letters:
            if self.compare_states(current_state, variations):
                return next((d for d in variations if 'optimal_red_location' in d and 'optimal_blue_location' in d), None)
        return None
