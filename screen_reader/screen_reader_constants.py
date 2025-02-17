import pathlib
import os


class ScreenReadException(Exception):
    pass


own_path = pathlib.Path(__file__).parent.resolve()

TESSERACT_DEFAULT_WIN_INSTALL_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSERACT_LSTMF_WIN_EXE = r"C:\Program Files\Tesseract-OCR\lstmtraining.exe"
TESSERACT_BASE_EN_MODEL_PATH = os.path.join(own_path, "font_train/base_model/eng.traineddata")
TESSERACT_EN_LAST_CHECKPOINT = os.path.join(own_path, "font_train/base_model/eng.lstm")
TEST_IMAGE_GAME = "test/Test_image_game_001.png"

STATE_CHECK_ROI_KEY = "state_check"
STATE_CHECK_RESULTS_STR = "expected_value"

# assuming game is at 720p
# in game screen coords
ENEMIES_KILLED = {"start_x": 1028, "start_y": 101, "end_x": 1088, "end_y": 127}
LVL = {"start_x": 1224, "start_y": 39, "end_x": 1287, "end_y": 66}
TIME = {"start_x": 601, "start_y": 89, "end_x": 693, "end_y": 114}
LVL_TEXT = {"start_x": 1182, "start_y": 36, "end_x": 1221, "end_y": 68, STATE_CHECK_RESULTS_STR: "LV:"}

# pause screen coords
CHAR_NAME = {"start_x": 160, "start_y": 275, "end_x": 364, "end_y": 304}

# char select coords
SCREEN_HEADER = {"start_x": 452, "start_y": 53, "end_x": 838, "end_y": 97, STATE_CHECK_RESULTS_STR: "CHOOSEROPFMNAOOIL"}
SELECTED_NAME = {"start_x": 52, "start_y": 474, "end_x": 382, "end_y": 509}

# level up
LEVEL_UP_TEXT = {"start_x": 136, "start_y": 229, "end_x": 348, "end_y": 280, STATE_CHECK_RESULTS_STR: "VEEUPI"} # I hate this

# main menu
PLAY_BUTTON = {"start_x": 1011, "start_y": 249, "end_x": 1119, "end_y": 286, STATE_CHECK_RESULTS_STR: "Play"}

ENEMIES_KILLED_KEY = "killed"
LVL_KEY = "lvl"
TIME_KEY = "time"
SELECTED_CHAR_KEY = "selected"
LEVEL_UP = "level_up"

# keys
GAME_KEYS = (ENEMIES_KILLED_KEY, LVL_KEY, TIME_KEY)
CHAR_SELECT_KEYS = (SELECTED_CHAR_KEY,)
ALL_KEYS = (ENEMIES_KILLED_KEY, LVL_KEY, TIME_KEY, SELECTED_CHAR_KEY)

# 136 229
#348 280

# state infos
GAME_ROIS = {ENEMIES_KILLED_KEY: ENEMIES_KILLED,
             LVL_KEY: LVL,
             TIME_KEY: TIME,
             STATE_CHECK_ROI_KEY: LVL_TEXT}
MAIN_MENU_ROIS = {STATE_CHECK_ROI_KEY: PLAY_BUTTON}
CHAR_SELECT_RIOS = {SELECTED_CHAR_KEY: SELECTED_NAME,
                    STATE_CHECK_ROI_KEY: SCREEN_HEADER}
LEVEL_UP_RIOS = {LEVEL_UP: LEVEL_UP_TEXT,
                 STATE_CHECK_ROI_KEY: LEVEL_UP_TEXT}

HCURE_ROIS = {"char_select": CHAR_SELECT_RIOS}
# HCURE_ROIS = {"char_select": CHAR_SELECT_RIOS,
#               "level_up": LEVEL_UP_RIOS}
