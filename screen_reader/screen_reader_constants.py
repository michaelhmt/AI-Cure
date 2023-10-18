import pathlib
import os

own_path = pathlib.Path(__file__).parent.resolve()

TESSERACT_DEFAULT_WIN_INSTALL_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSERACT_LSTMF_WIN_EXE = r"C:\Program Files\Tesseract-OCR\lstmtraining.exe"
TESSERACT_BASE_EN_MODEL_PATH = os.path.join(own_path, "font_train/base_model/eng.traineddata")
TESSERACT_EN_LAST_CHECKPOINT = os.path.join(own_path, "font_train/base_model/eng.lstm")
TEST_IMAGE_GAME = "test/Test_image_game_001.png"

# assuming game is at 720p
# in game screen coords
SCORE = {"start_x": 590, "start_y": 57, "end_x": 623, "end_y": 87}
ENEMIES_KILLED = {"start_x": 590, "start_y": 57, "end_x": 691, "end_y": 87}
LVL = {"start_x": 590, "start_y": 57, "end_x": 691, "end_y": 87}
TIME = {"start_x": 590, "start_y": 57, "end_x": 691, "end_y": 87}

GAME_ROIS = {"score": SCORE,
             "killed": ENEMIES_KILLED,
             "lvl": LVL,
             "time": TIME}
