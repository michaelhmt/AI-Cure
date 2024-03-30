import os
# always make sure this is at the root of the project
base_dir = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = f"{base_dir}\\config.yaml"
CHEAT_ENGINE_TABLE_PATH = f"{base_dir}\\memory_reader\\table_report.CT"
HCURE_GAME_EXE = f"{base_dir}\\Game_depolyment\HoloCure.exe"
HCURE_OCR_MODEL_PATH = f"{base_dir}\\screen_reader\\font_train\\trained_model\\hcure_font_model_5.traineddata"
IMAGE_MISC_TRAING_DIR = f"{base_dir}\\screen_reader\\font_train\\data_capture\\misc_training"
DEFAULT_BOX = f"{base_dir}\\screen_reader\\font_train\\data_capture\\hcure_level_up\\back-up\\default_box.box"
LEVEL_UP_IMAGES = f"{base_dir}\\screen_reader\\font_train\\data_capture\\hcure_level_up\\bad"
LEVEL_UP_OUT_PUT_DIR = f"{base_dir}\\screen_reader\\font_train\\data_capture\\hcure_level_uaadawp"