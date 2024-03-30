# python built in
import os.path
import subprocess
import time
import pprint

# site packages
import pydirectinput
import pygetwindow

# project modules
import project_constants
from config.hcure_config import HcureConfig
from screen_reader.screen_reader_constants import HCURE_ROIS
from memory_reader.mem_addresses import IN_GAME_STATES, STATE_CHECK_KEY
from screen_reader.game_screen_vision.vision_class import GameVisionClass
from memory_reader.GameMemoryClass import GameMemoryClass
from memory_reader.prep_with_cheat_engine import CheatEngineHoloCure

from screen_reader.game_screen_vision.state_object import GameVisualState as VisualGameState
from memory_reader.game_state import MemoryGameState

def start_hcure(config):
    # type: (HcureConfig) -> subprocess.Popen
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

def make_hcure_states(memory_interface, game_vision_interface):

    states = list()

    high_prio_states = list()

    # make memory states
    for name, addresses in IN_GAME_STATES.items():
        print(f"state key of {STATE_CHECK_KEY} is in addresses?: {STATE_CHECK_KEY in addresses}")
        state = MemoryGameState(name, addresses, memory_interface)
        states.append(state)

    for name, roi in HCURE_ROIS.items():
        state = VisualGameState(name, roi, game_vision_interface)
        if name in ("level_up"):
            # states that have to be check in front of others
            # in the case of level_up it's a state that can occur during gameplay so we need to check for it
            # before we check for gameplay state
            high_prio_states.append(state)
        else:
            states.append(state)

    new_state_order = list()
    if high_prio_states:
        for state in high_prio_states:
            states.insert(0, state)

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

def get_game_state_from_cheat_engine_report(proc_id):
    report_target = f"C:\\ai_knight\\cheat_engine_report_{proc_id}.txt"
    cheat_engine = CheatEngineHoloCure()
    cheat_engine.start_cheat_engine()

    if not os.path.exists(report_target):
        print(f"could not find created report for {report_target}")
        return

    with open(report_target, "r") as report_file:
        report_data = dict()
        report_lines = report_file.readlines()
        for line in report_lines:
            line = line.strip()
            try:
                data_name, data_value = line.split(",")
            except ValueError:
                continue
            if "???" in data_value or "()" in data_value:
                continue

            pointer_address = data_value.split("P->")[-1]
            clean_name = data_name.split("Name: ")[-1]
            report_data[clean_name] = pointer_address
    return report_data

def clear_files_in_report_folder():
    report_folder = "C:\\ai_knight"
    # Ensure the folder exists
    if not os.path.exists(report_folder):
        return

    # List all the entries in the folder
    for entry in os.listdir(report_folder):
        # Construct full entry path
        entry_path = os.path.join(report_folder, entry)
        # Check if it's a file and delete it
        if os.path.isfile(entry_path):
            os.remove(entry_path)

if __name__ == "__main__":

    config_path = project_constants.CONFIG_PATH
    config_object = HcureConfig(config_path)
    h_cure_proc = start_hcure(config_object)
    proc_id = h_cure_proc.pid

    time.sleep(15)
    print(f"making report for {proc_id}")
    cheat_engine_report = get_game_state_from_cheat_engine_report(proc_id)
    pprint.pprint(cheat_engine_report)

    #char_select_to_game()






