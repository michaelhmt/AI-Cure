import pathlib
import os

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
ENEMIES_KILLED = {"start_x": 1024, "start_y": 64, "end_x": 1085, "end_y": 99}
LVL = {"start_x": 1217, "start_y": 8, "end_x": 1262, "end_y": 32}
TIME = {"start_x": 590, "start_y": 57, "end_x": 691, "end_y": 87}
LVL_TEXT = {"start_x": 1182, "start_y": 36, "end_x": 1221, "end_y": 68, STATE_CHECK_RESULTS_STR: "LV:"}

# pause screen coords
CHAR_NAME = {"start_x": 160, "start_y": 275, "end_x": 364, "end_y": 304}

# char select coords
SCREEN_HEADER = {"start_x": 452, "start_y": 53, "end_x": 838, "end_y": 97, STATE_CHECK_RESULTS_STR: "CHOOSE YOUR IDOL"}
SELECTED_NAME = {"start_x": 45, "start_y": 445, "end_x": 309, "end_y": 477}

# main menu
PLAY_BUTTON = {"start_x": 1011, "start_y": 249, "end_x": 1119, "end_y": 286, STATE_CHECK_RESULTS_STR: "Play"}

GAME_ROIS = {"killed": ENEMIES_KILLED,
             "lvl": LVL,
             "time": TIME,
             STATE_CHECK_ROI_KEY: LVL_TEXT}
MAIN_MENU_ROIS = {STATE_CHECK_ROI_KEY: PLAY_BUTTON}
CHAR_SELECT_RIOS = {"selected": SELECTED_NAME,
                    STATE_CHECK_ROI_KEY: SCREEN_HEADER}

HCURE_ROIS = {"game_screen": GAME_ROIS, "main_menu": MAIN_MENU_ROIS, "char_select": CHAR_SELECT_RIOS}


