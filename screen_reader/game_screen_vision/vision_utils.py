# own modules
from screen_reader.screen_reader_constants import HCURE_ROIS
from screen_reader.game_screen_vision.state_object import GameState

def make_hcure_game_states():
    states = list()
    for name, roi in HCURE_ROIS.items():
        state = GameState(name, roi)
        states.append(state)
    return states