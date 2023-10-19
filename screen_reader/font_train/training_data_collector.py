# # python built in
import time
import os
import pathlib
import shutil

# site packages
import pyautogui
import keyboard

# own modules
import screen_reader.font_train.training_utils as training_utils

TIME_COORDS = {"x": 1224, "y":426, "width": 110, "height": 35}

class Collector:
    own_path = pathlib.Path(__file__).parent.resolve()

    def __init__(self, coords, training_data_name, default_box_file=None):
        self.target = coords
        self.data_name = training_data_name
        self.default_box = default_box_file

        self.output_path_dir = os.path.join(self.own_path, "data_capture", self.data_name)
        if not os.path.exists(self.output_path_dir):
            os.makedirs(self.output_path_dir)

    def capture_data(self, delay_time=2, prefix_name=None, overwrite=False):

        counter = 0

        while True:
            if keyboard.is_pressed("q"):
                print("exiting capture")
                break

            region = (self.target["x"], self.target["y"],
                      self.target["width"], self.target["height"])

            print("Took screenshot")
            screen_shot = pyautogui.screenshot(region=region)

            prefix = prefix_name or "screenshot_capture"
            screenshot_output = os.path.join(self.output_path_dir, f"{prefix}_{counter}.png")
            if os.path.exists(screenshot_output) and not overwrite:
                counter += 1
                continue

            screen_shot.save(screenshot_output)
            if self.default_box:
                box_path = screenshot_output.split(".")[0] + ".box"
                shutil.copy(self.default_box, box_path)

            counter += 1

            time.sleep(delay_time)

        if not self.default_box:
            self.make_box_files()

    def make_box_files(self):
        training_utils.make_box_file_for_dir(self.output_path_dir)
        training_utils.validiate_empty_box_files(self.output_path_dir)


if __name__ == "__main__":
    data_collector = Collector(TIME_COORDS, "hcure_time_counter",
                               default_box_file="E:\\Python\\Ai_Knight\\screen_reader\\font_train\\data_capture\\default_time_Box.box")
    data_collector.capture_data(delay_time=6)
    #data_collector.make_box_files()
