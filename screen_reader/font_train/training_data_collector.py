# # python built in
import time
import os
import pathlib
import shutil

# site packages
import pyautogui

# own modules
import project_constants
import screen_reader.font_train.training_utils as training_utils

TIME_COORDS = {"x": 1224, "y":426, "width": 110, "height": 35}
LVL_COORDS_UP = {"x": 701, "y":554, "width": 313, "height": 382}
LVL = {"x": 1809, "y":374, "width": 100, "height": 33}
EUIP_COORDS = {"x": 1224, "y":426, "width": 110, "height": 35}

class Collector:
    own_path = pathlib.Path(__file__).parent.resolve()

    def __init__(self, coords, training_data_name, default_box_file=None, ):
        self.target = coords
        self.data_name = training_data_name
        self.default_box = default_box_file

        self.output_path_dir = os.path.join(self.own_path, "data_capture", self.data_name)
        if not os.path.exists(self.output_path_dir):
            os.makedirs(self.output_path_dir)

    def capture_one(self, prefix_name=None, overwrite=True):
        prefix = prefix_name or "screenshot_capture"

        image_number = 0
        while True:
            screenshot_output = os.path.join(self.output_path_dir, f"{prefix}_{str(image_number).zfill(3)}.png")
            if os.path.exists(screenshot_output) and not overwrite:
                image_number += 1
                continue
            else:
                break
        self.capture_image(screenshot_output)

    def capture_image(self, output_path):
        region = (self.target["x"], self.target["y"],
                  self.target["width"], self.target["height"])

        print("Took screenshot")
        screen_shot = pyautogui.screenshot(region=region)
        screen_shot.save(output_path)
        if self.default_box:
            box_path = output_path.split(".")[0] + ".box"
            shutil.copy(self.default_box, box_path)

    def capture_data(self, delay_time=2, prefix_name=None, overwrite=False):

        counter = 0

        while True:
            print("Took screenshot")

            prefix = prefix_name or "screenshot_capture"
            screenshot_output = os.path.join(self.output_path_dir, f"{prefix}_{counter}.png")
            if os.path.exists(screenshot_output) and not overwrite:
                continue
            self.capture_image(screenshot_output)

            counter += 1

            time.sleep(delay_time)

        if not self.default_box:
            self.make_box_files()

    def make_box_files(self, custom_model=None):
        training_utils.make_box_file_for_dir(self.output_path_dir, custom=custom_model)
        training_utils.validiate_empty_box_files(self.output_path_dir)


if __name__ == "__main__":
    #default_box_file=project_constants.DEFAULT_BOX
    data_collector = Collector(TIME_COORDS, "hcure_time_counter_set_02")
    #data_collector.capture_data()
    #data_collector.capture_one(prefix_name="hcure_level_number", overwrite=False)
    data_collector.make_box_files(project_constants.HCURE_OCR_MODEL_PATH)
