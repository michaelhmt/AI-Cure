# python built in
import subprocess
import time

# site packages
import pydirectinput
import pygetwindow

# project modules
from config.hcure_config import HcureConfig
from screen_reader.screen_reader_constants import HCURE_ROIS
from memory_reader.mem_addresses import IN_GAME_STATES, STATE_CHECK_KEY
from screen_reader.game_screen_vision.vision_class import GameVisionClass
from memory_reader.GameMemoryClass import GameMemoryClass

from screen_reader.game_screen_vision.state_object import GameVisualState as VisualGameState
from memory_reader.game_state import MemoryGameState

def start_hcure(config):
    # start the app
    exe_path = config.get_exe_path()
    proc = subprocess.Popen(exe_path)
    time.sleep(8)
    game_window = pygetwindow.getWindowsWithTitle("HoloCure")[0]
    game_window.activate()

    # get us past the opening and into char select
    for _ in range(3):
        pydirectinput.press("enter")
        time.sleep(0.4)

    return proc

def make_hcure_states(config, proc_id, interface):

    states = list()

    memory_interface = GameMemoryClass(proc_id)
    # make memory states
    for name, addresses in IN_GAME_STATES.items():
        print(f"state key of {STATE_CHECK_KEY} is in addresses?: {STATE_CHECK_KEY in addresses}")
        state = MemoryGameState(name, addresses, memory_interface)
        states.append(state)

    vision_model = config.get_vision_model_path()
    game_vision_interface = GameVisionClass(interface.get_window_array, vision_model)
    for name, roi in HCURE_ROIS.items():
        state = VisualGameState(name, roi, game_vision_interface)
        states.append(state)

    return states

def char_select_to_game():
    game_window = pygetwindow.getWindowsWithTitle("HoloCure")[0]
    game_window.activate()

    # select endless mode
    pydirectinput.press("d")

    # skip outfit and level selections and get into game
    pydirectinput.press("enter")
    pydirectinput.press("enter")
    pydirectinput.press("enter")
    pydirectinput.press("enter")
    pydirectinput.press("enter")

if __name__ == "__main__":
    config_path = "E:\\Python\\Ai_Knight\\config.yaml"
    config_object = HcureConfig(config_path)
    #start_hcure(config_object)
    char_select_to_game()





