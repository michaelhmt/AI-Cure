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
from screen_reader.game_screen_vision.state_object import GameVisualState
import screen_reader.screen_reader_constants as screen_reader_constants
from screen_reader.game_screen_vision.vision_utils import make_hcure_game_states
from screen_reader.font_train.training_utils import str_is_similar
import screen_reader.game_screen_vision.vision_utils as vision_utils

class GameVisionClass:
    own_path = pathlib.Path(__file__).parent.resolve()
    test_data_dir = os.path.join(own_path, "test_data")

    def __init__(self,image_method, vision_model, parent_id_search=True):
        self.image_reterivial_method = image_method
        vision_model = vision_model.replace("\\", "/")
        self.vision_model_path = vision_model
        self.model_data_dir = str()
        self.model_name = str()

        self.states = dict()
        self.current_state = None
        self.treat_image = False
        self.testing = False

        if not os.path.exists(self.test_data_dir):
            try:
                os.makedirs(self.test_data_dir)
            except OSError:
                pass

        # get the handler of the exe id
        self.matched_handler = None
        self.prep_tesseract()

    def prep_tesseract(self):
        """
        Run once to set tesseract up
        """
        tessract_install_path = screen_reader_constants.TESSERACT_DEFAULT_WIN_INSTALL_PATH
        pytesseract.pytesseract.tesseract_cmd = tessract_install_path

        self.model_data_dir = os.path.dirname(self.vision_model_path)
        self.model_name = os.path.basename(self.vision_model_path).split(".")[0]


    def capture_window(self, check_this_roi=None):
        # type: (bool) -> Image

        # Reshape the numpy array to match the image dimensions.
        # The 'BGRX' suggests the image is 4-channel with the last being ignored.
        image_np = self.image_reterivial_method()

        # Drop the fourth channel (X) and convert to grayscale using OpenCV
        opencv_image_gray = cv2.cvtColor(image_np[:, :, :3], cv2.COLOR_BGR2GRAY)
        treated_image = vision_utils.mid_gray_non_white_blakcs(vision_utils.convert_cv2_to_pil(opencv_image_gray))
        gray_image = vision_utils.convert_pil_to_cv2(treated_image)

        if self.testing:
            self.save_to_debug_folder(gray_image, roi_to_write=check_this_roi)
        return gray_image

    def get_window_size(self):
        window_array = self.image_reterivial_method()
        shape = window_array.shape
        return shape[0], shape[1]


    def save_to_debug_folder(self, image, roi_to_write=None):
        """
       Saves the image to debug folder annotates with state rois and guessed values if the state has any

        Args:
            image (cv2.image): loaded cv2 image
        """

        save_path = os.path.join(self.test_data_dir, f"vision_debug_image_{str(len(os.listdir(self.test_data_dir)) + 1).zfill(4)}.png")
        if self.current_state:
            for roi_name, roi_coords in self.states[self.current_state]:
                self.draw_rio(image, roi_name, roi_coords)
        elif roi_to_write:
            for roi_name, roi_coords in roi_to_write.items():
                self.draw_rio(image, roi_name, roi_coords)
        cv2.imwrite(save_path, image)

    def draw_rio(self, image, roi_name, roi_coords):
        cv2.rectangle(image,
                      (roi_coords['start_x'], roi_coords['start_y']),
                      (roi_coords['end_x'], roi_coords['end_y']),
                      (0, 0, 255), 2)
        cv2.putText(image,
                    f"{roi_name}:  {self.check_roi(roi_coords, image)}",
                    (roi_coords['start_x'], roi_coords['start_y'] - 18),
                    cv2.FONT_HERSHEY_PLAIN, 1.1, (0, 0, 255), 2, cv2.LINE_AA)

    def check_roi(self, roi_coords, image):
        # type: (dict[str, int], Image) -> str
        """
        check a single region of interest from the loaded image

        Args:
            roi_coords (dict): dict for the coord data for the roi
            image(Image): The image we will extract the roi from

        Returns:
            (str) found text from the roi

        """
        roi = image[roi_coords['start_y']:roi_coords['end_y'],
                    roi_coords['start_x']:roi_coords['end_x']]

        collected_str = pytesseract.image_to_string(roi, lang=self.model_name,
                                               config=f"--tessdata-dir {self.model_data_dir} --psm 6")
        collected_str = collected_str.replace("\n", "")
        return collected_str

    def state_is_active(self, state_to_check):
        """
        Loops through the currently loaded states and determines which one if any is currently active.
        """

        results = dict()

        test_roi, expected_result = state_to_check.state_check()
        current_screen = self.capture_window(check_this_roi={"State Check": test_roi})
        result_str = self.check_roi(test_roi, current_screen)

        in_this_state = str_is_similar(result_str, expected_result)
        result = {"expected_result": expected_result,
                  "gathered_result": result_str,
                  "in_this_game_state": str_is_similar(result_str, expected_result),
                  "state_name": state_to_check.name}

        return in_this_state
        # self.current_state = None
        # for state_name, state_result in results.items():
        #     if state_result['in_this_game_state']:
        #         if not self.current_state:
        #             self.current_state = state_result['state_name']
        #         else:
        #             self.current_state = None
        #             print("cannot determine game state")

    def get_current_state_info(self, state):
        """
        If a state is currently set will loop through the state rois and report the value of each one.
        """
        current_screen = self.capture_window()
        state_report = dict()
        for roi_name, roi_coords in state:
            state_report[roi_name] = self.check_roi(roi_coords, current_screen)

        return state_report




if __name__ == "__main__":
    my_h_cure_exe_path = project_constants.HCURE_GAME_EXE
    vision_model_path = project_constants.HCURE_OCR_MODEL_PATH
    proc = subprocess.Popen(my_h_cure_exe_path)
    time.sleep(15)  # allow the proc to start
    proc_id = proc.pid
    vision = GameVisionClass(proc_id, vision_model_path)
    vision.treat_image = True
    vision.testing = True
    vision.add_states(make_hcure_game_states())
    vision.find_current_state()

    count = 0
    while True:
        if count > 8:
            count = 0
            print("checking state")
            vision.find_current_state()
        else:
            count += 1
        vision.get_current_state_info()

