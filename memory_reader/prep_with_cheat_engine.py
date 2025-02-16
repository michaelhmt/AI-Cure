import os
import time
import subprocess

# site packages
import pygetwindow
import pyautogui
import win32gui
import win32process
import win32api

import project_constants


REPORT_MAKER_TABLE = project_constants.CHEAT_ENGINE_TABLE_PATH
CONFIRM_WINDOW_YES_BUTTON = {"window_name": "Confirmation", "x": 364, "y":140}
CHEAT_ENGINE_TABLE_MID = {"window_name": "Cheat Engine 7.5", "x": 697, "y":776}
CHEAT_ENGINE_FILE_MENU = {"window_name": "Cheat Engine 7.5", "x": 23, "y":55}
CHEAT_ENGINE_FILE_RECENT = {"window_name": "Cheat Engine 7.5", "x": 76, "y":382}
CHEAT_ENGINE_MOST_RECENT = {"window_name": "Cheat Engine 7.5", "x": 506, "y":382}

TABLE_WRITE_REPORT = {"window_name": "Cheat Engine 7.5", "x": 40, "y":900}


def start_cheat_engine_task():
    """
    You must make a windows task for Cheat engine that runs with admin privileges

    Returns:

    """
    task_name = "cheat_engine_start_python_no_admin"
    try:
        # Create the task (You might need to adjust the scheduling options according to your needs)

        # To run the task on demand, it's initially scheduled for a time in the past. Now, change the trigger to 'On demand'.
        proc = subprocess.run(["schtasks", "/run", "/tn", task_name], check=True)
        return proc
    except subprocess.SubprocessError as e:
        print(f"Failed to create task: {e}")

class CheatEngineHoloCure:

    def __init__(self):
        self.app_window = None
        self.cheat_engine_proc = self.start_cheat_engine()

    def load_report_table(self):
        self.start_cheat_engine()

    def get_window_and_click_target(self, window_name, relative_x, relative_y, click=True):

        hwnd = win32gui.FindWindow(None, window_name)
        rect = win32gui.GetWindowRect(hwnd)

        absolute_point_x = rect[0] + relative_x
        absolute_point_y = rect[1] + relative_y
        pyautogui.moveTo(absolute_point_x, absolute_point_y, duration=0.5)
        print(f"moved mouse to x:{absolute_point_x}, y:{absolute_point_y}")
        if click:
            time.sleep(0.2)
            pyautogui.click()

    def make_window_active(self, window_name):
        self.app_window = pygetwindow.getWindowsWithTitle(window_name)[0]
        self.app_window.activate()

    def force_close_window(self, title):
        # Find the window by its title
        hwnd = win32gui.FindWindow(None, title)
        if hwnd:
            # Get the process ID of the window
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            # Open the process with terminate rights
            handle = win32api.OpenProcess(1, False, pid)
            # Terminate the process
            win32api.TerminateProcess(handle, -1)
            win32api.CloseHandle(handle)
            print(f"Process with PID {pid} terminated.")
        else:
            print(f"Window with title '{title}' not found.")

    # so this is dumb but we have to operate cheat engine using only the mouse
    def start_cheat_engine(self):
        # start the app
        cheat_engine = start_cheat_engine_task()
        time.sleep(2)

        # load the table
        target_info = CHEAT_ENGINE_FILE_MENU
        self.make_window_active(target_info["window_name"])
        self.get_window_and_click_target(target_info["window_name"],
                                         target_info["x"],
                                         target_info["y"])

        target_info = CHEAT_ENGINE_FILE_RECENT
        self.make_window_active(target_info["window_name"])
        self.get_window_and_click_target(target_info["window_name"],
                                         target_info["x"],
                                         target_info["y"])

        target_info = CHEAT_ENGINE_MOST_RECENT
        self.make_window_active(target_info["window_name"])
        self.get_window_and_click_target(target_info["window_name"],
                                         target_info["x"],
                                         target_info["y"])

        # click yes on confirm window
        target_info = CONFIRM_WINDOW_YES_BUTTON
        self.make_window_active(target_info["window_name"])
        self.get_window_and_click_target(target_info["window_name"],
                                         target_info["x"],
                                         target_info["y"])
        time.sleep(3)
        target_info = CHEAT_ENGINE_TABLE_MID
        self.make_window_active(target_info["window_name"])
        self.get_window_and_click_target(target_info["window_name"],
                                         target_info["x"],
                                         target_info["y"],
                                         click=False)
        pyautogui.scroll(-1000000)
        time.sleep(1)

        target_info = TABLE_WRITE_REPORT
        self.make_window_active(target_info["window_name"])
        self.get_window_and_click_target(target_info["window_name"],
                                         target_info["x"],
                                         target_info["y"])
        time.sleep(3)
        self.force_close_window(target_info["window_name"])

if __name__ == "__main__":
    cheat_engine = CheatEngineHoloCure()