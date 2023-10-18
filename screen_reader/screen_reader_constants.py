TESSERACT_DEFAULT_WIN_INSTALL_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
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
