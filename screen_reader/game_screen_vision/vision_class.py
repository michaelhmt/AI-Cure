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
from PIL import Image, ImageOps

# own modules
from screen_reader.game_screen_vision.state_object import GameState
import screen_reader.screen_reader_constants as screen_reader_constants
from screen_reader.game_screen_vision.vision_utils import make_hcure_game_states
from screen_reader.font_train.training_utils import str_is_similar
import screen_reader.game_screen_vision.vision_utils as vision_utils

class GameVisionClass:
    own_path = pathlib.Path(__file__).parent.resolve()
    test_data_dir = os.path.join(own_path, "test_data")

    def __init__(self, game_exe_proc_id, vision_model, parent_id_search=True):
        self.proc_id = game_exe_proc_id
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
        self.get_exe_handle(parent_id_search)
        self.prep_tesseract()

    def prep_tesseract(self):
        """
        Run once to set tesseract up
        """
        tessract_install_path = screen_reader_constants.TESSERACT_DEFAULT_WIN_INSTALL_PATH
        pytesseract.pytesseract.tesseract_cmd = tessract_install_path

        self.model_data_dir = os.path.dirname(self.vision_model_path)
        self.model_name = os.path.basename(self.vision_model_path).split(".")[0]

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

    def get_window_array(self):
        # type: () -> numpy.ndarray

        """
        Captures the active window of our given process

        Returns:
            (Image) A Pillow image object

        """

        # Get the device context for the entire window
        hwindc = win32gui.GetWindowDC(self.matched_handler)
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

        return image_np


    def capture_window(self):
        # type: () -> Image

        # Reshape the numpy array to match the image dimensions.
        # The 'BGRX' suggests the image is 4-channel with the last being ignored.
        image_np = self.get_window_array()

        # Drop the fourth channel (X) and convert to grayscale using OpenCV
        opencv_image_gray = cv2.cvtColor(image_np[:, :, :3], cv2.COLOR_BGR2GRAY)
        treated_image = vision_utils.mid_gray_non_white_blakcs(vision_utils.convert_cv2_to_pil(opencv_image_gray))
        gray_image = vision_utils.convert_pil_to_cv2(treated_image)

        if self.testing:
            self.save_to_debug_folder(gray_image)
        return gray_image

    def get_window_size(self):
        window_array = self.get_window_array()
        shape = window_array.shape
        return shape[0], shape[1]


    def save_to_debug_folder(self, image):
        """
       Saves the image to debug folder annotates with state rois and guessed values if the state has any

        Args:
            image (cv2.image): loaded cv2 image
        """

        save_path = os.path.join(self.test_data_dir, f"vision_debug_image_{str(len(os.listdir(self.test_data_dir)) + 1).zfill(4)}.png")
        if self.current_state:
            for roi_name, roi_coords in self.states[self.current_state]:
                cv2.rectangle(image,
                              (roi_coords['start_x'], roi_coords['start_y']),
                              (roi_coords['end_x'], roi_coords['end_y']),
                              (0, 0, 255), 2)
                cv2.putText(image,
                            f"{roi_name}:  {self.check_roi(roi_coords, image)}",
                            (roi_coords['start_x'], roi_coords['start_y'] - 18),
                            cv2.FONT_HERSHEY_PLAIN, 1.1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imwrite(save_path, image)

    def add_states(self, states):
        # type: (list[GameState]) -> None
        for state in states:
            self.states[state.name] = state

    def clear_states(self):
        self.states.clear()

    @property
    def loaded_states(self):
        return list(self.states.keys())

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

    def find_current_state(self):
        """
        Loops through the currently loaded states and determines which one if any is currently active.
        """

        results = dict()
        current_screen = self.capture_window()
        for state in self.states.values(): # type: GameState
            test_roi, expected_result = state.state_check()
            result_str = self.check_roi(test_roi, current_screen)

            result = {"expected_result": expected_result,
                      "gathered_result": result_str,
                      "in_this_game_state": str_is_similar(result_str, expected_result),
                      "state_name": state.name}
            results[state.name] = result

        self.current_state = None
        for state_name, state_result in results.items():
            if state_result['in_this_game_state']:
                if not self.current_state:
                    self.current_state = state_result['state_name']
                else:
                    self.current_state = None
                    print("cannot determine game state")

    def get_current_state_info(self):
        """
        If a state is currently set will loop through the state rois and report the value of each one.
        """
        if not self.current_state:
            print("No current state set, skipping")
            return

        state_report = dict()
        current_frame = self.capture_window()
        for roi_name, roi_coords in self.states[self.current_state]:
            state_report[roi_name] = self.check_roi(roi_coords, current_frame)




if __name__ == "__main__":
    my_h_cure_exe_path = "E:\\holocure\\Game_depolyment\\HoloCure.exe"
    vision_model_path = "E:\\Python\\Ai_Knight\\screen_reader\\font_train\\trained_model\\hcure_font_model_6.traineddata"
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

