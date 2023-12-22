# python built in
import subprocess
import time

# site packages
import pydirectinput
import pygetwindow

# project modules
from config.hcure_config import HcureConfig


def start_hcure(config):
    # start the app
    exe_path = config.get_exe_path()
    proc = subprocess.Popen(exe_path)
    time.sleep(3)
    game_window = pygetwindow.getWindowsWithTitle("HoloCure")[0]
    game_window.activate()

    # get us past the opening and into char select
    for _ in range(3):
        pydirectinput.press("enter")
        time.sleep(0.4)

    return proc

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





