# python built in
import subprocess
import time
import os
import numpy
import pathlib


# site packages
import win32gui
import win32process
import psutil
import win32con
import win32ui
import cv2
import pytesseract
from PIL import Image

# own modules
import project_constants
from states.state_object import BaseGameState
from screen_reader.game_screen_vision.state_object import GameVisualState as VisualGameState
from memory_reader.game_state import MemoryGameState

from screen_reader.game_screen_vision.vision_class import GameVisionClass
from screen_reader.screen_reader_constants import ScreenReadException
from memory_reader.GameMemoryClass import GameMemoryClass

import screen_reader.screen_reader_constants as screen_reader_constants
from screen_reader.game_screen_vision.vision_utils import make_hcure_game_states
from screen_reader.font_train.training_utils import str_is_similar
import screen_reader.game_screen_vision.vision_utils as vision_utils



class BaseGameInterface:

    def __init__(self, game_exe_proc_id, config, parent_app, game_states=None, parent_id_search=True):
        self.proc_id = game_exe_proc_id
        self._current_state = None
        self._states = game_states or list()
        self._config = config
        self._last_image = None

        self.blank_state = BaseGameState("No State found", dict(), None)

        # get the handler of the exe id
        self.matched_handler = None
        self.get_exe_handle(parent_id_search)
        self.app_instance = parent_app

    def switch_to_new_game_window(self, new_proc_id):
        self.proc_id = new_proc_id
        self.get_exe_handle()

    def get_exe_handle(self, search_parent_procs=True):
        # type: (bool) -> None
        """
        Find the handler ID associated with our target process ID and update class attribute

        Args:
            search_parent_procs (bool): should we check the parent process
            to see if that spawned the currently selected proc

        """

        def callback(hwnd, target_process_ids):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                _, found_proc_id = win32process.GetWindowThreadProcessId(hwnd)
                found_ids = [found_proc_id]
                if search_parent_procs:
                    process = psutil.Process(found_proc_id)
                    found_ids.append(process.ppid())
                for found_id in found_ids:
                    if found_id in target_process_ids:
                        self.matched_handler = hwnd
            return True

        win32gui.EnumWindows(callback, [self.proc_id])

    def get_last_image(self, clear=True):
        last_image = self._last_image
        if clear:
            self._last_image = None
        return last_image

    def get_window_array(self):
        # type: () -> numpy.ndarray

        """
        Captures the active window of our given process

        Returns:
            (Image) A Pillow image object

        """

        # Get the device context for the entire window
        try:
            hwindc = win32gui.GetWindowDC(self.matched_handler)
        except Exception:
            raise ScreenReadException("Could not find attached Window")
        left, top, right, bot = win32gui.GetWindowRect(self.matched_handler)
        width = right - left
        height = bot - top

        # Create a device context into which we will draw the capture
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()

        # Create a blank bitmap image the same dimensions as the window
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)

        # BitBlt the window's contents into the bitmap's device context
        memdc.BitBlt((0, 0), (width, height), srcdc, (0, 0), win32con.SRCCOPY)

        # Convert the raw bits of the image into a format that Pillow understands
        bmpinfo = bmp.GetInfo()
        bmpstr = bmp.GetBitmapBits(True)

        # Create a numpy array from the raw string
        image_np = numpy.frombuffer(bmpstr, dtype=numpy.uint8)
        image_np = image_np.reshape((bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4))

        # Free up the device contexts and bitmap objects
        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(self.matched_handler, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())

        self._last_image = image_np
        return image_np

    def focus_game(self):
        # Try to bring the window to the foreground
        win32gui.SetForegroundWindow(self.matched_handler)
        # If the window is minimized, restore it
        if win32gui.IsIconic(self.matched_handler):
            win32gui.ShowWindow(self.matched_handler, win32con.SW_RESTORE)

    def get_window_size(self):
        window_array = self.get_window_array()
        shape = window_array.shape
        return shape[0], shape[1]

    @property
    def current_state(self):
        if not self._current_state:
            return self.blank_state
        return self._current_state

    def add_states(self, states):
        # type: (list[GameState]) -> None
        self._states.extend(states)

    def clear_states(self):
        self._states.clear()

    @property
    def loaded_states(self):
        return [state.name for state in self._states]

    def find_current_state(self):
        """
        Loops through the currently loaded states and determines which one if any is currently active.
        """

        for this_state in self._states: # type: BaseGameState
            this_state_interface = this_state.interface
            in_this_state = this_state_interface.state_is_active(this_state)
            if in_this_state:
                self._current_state = this_state
                return True

    def get_current_state_info(self):
        """
        If a state is currently set will loop through the state rois and report the value of each one.
        """
        if not self._current_state:
            print("No current state set, skipping")
            return

        state_interface = self._current_state.interface
        state_info = state_interface.get_current_state_info(self._current_state)
        return state_info

    def add_known_states(self):
        """
        Implement on the specific game subclass

        """
        pass


if __name__ == "__main__":
    from screen_reader.screen_reader_constants import HCURE_ROIS
    import apps.hcure_utils as hcure_utils
    import config.hcure_config as hcure_config

    # make visual states
    states = list()

    config_path = project_constants.CONFIG_PATH
    config = hcure_config.HcureConfig(config_path)
    game_proc = hcure_utils.start_hcure(config)
    game_interface = BaseGameInterface(game_proc)


    vision_model = config.get_vision_model_path()
    game_vision_interface = GameVisionClass(game_interface.get_window_array, vision_model)
    for name, roi in HCURE_ROIS.items():
        state = VisualGameState(name, roi, game_vision_interface)
        states.append(state)

    from memory_reader.mem_addresses import IN_GAME_STATES

    memory_interface = GameMemoryClass()
    # make memory states
    for name, addresses in IN_GAME_STATES.items():
        state = MemoryGameState(name, addresses, memory_interface)
        states.append(state)

    print(states)


