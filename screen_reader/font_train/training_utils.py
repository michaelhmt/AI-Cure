# python built in
import os
import subprocess
import pathlib
import shutil
import time
from typing import Union

# own modules
from screen_reader.screen_reader_constants import TESSERACT_DEFAULT_WIN_INSTALL_PATH

BOX_CMD = "{tes_exe} {image_path} {box_path} batch.nochop makebox"
DEFAULT_BOX = os.path.join(pathlib.Path(__file__).parent.resolve(), "default_box.box")
GAME_CAPTURES_DIR = os.path.join(pathlib.Path(__file__).parent.resolve(), "game_captures")


def make_box_file_for_dir(root_dir, image_exts=("png", "jpg"), output_dir=False):
    # type: (str, tuple, Union[bool, str]) -> None
    """
    iterate through the files in a dir if they match our images,
    make a box file for them using Tesseract.

    Args:
        root_dir (str): The path of the dir to search
        image_exts (tuple): all valid file exts
        output_dir (str): dir to place our outputted box files,
                          if False, will use the root_dir

    """

    # we won't recursively search....yet
    for file_name in os.listdir(root_dir):
        file_ext = file_name.split(".")[-1]
        if file_ext in image_exts:
            if not output_dir:
                output_dir = root_dir

            image_name = file_name.split(".")[0]
            box_output = os.path.join(output_dir, image_name)

            cmd = BOX_CMD.format(tes_exe=TESSERACT_DEFAULT_WIN_INSTALL_PATH,
                                 image_path=os.path.join(root_dir, file_name),
                                 box_path=box_output)
            subprocess.Popen(cmd)

def validiate_empty_box_files(root_dir):
    # type: (str) -> None
    """
    Search through and replace any empty box file with a default box file
    will need to be manually corrected.

    Args:
        root_dir (str): Path of the dir to search

    """

    for file_name in os.listdir(root_dir):
        file_ext = file_name.split(".")[-1]
        file_path = os.path.join(root_dir, file_name)
        if file_ext == "box" and int(os.path.getsize(file_path)) == 0:
            print(f"Replacing bad box for {file_name}")
            os.remove(file_path)
            shutil.copy(DEFAULT_BOX, file_path)

def make_game_captures_box_files(override=False):
    # type: (bool) -> None
    """
    Convince method for generating box files for the game captures' folder.

    Args:
        override (bool): If a .box already exists, can we override it with the one we make?

    """
    for file_name in os.listdir(GAME_CAPTURES_DIR):
        file_ext = file_name.split(".")[-1]
        if file_ext in ("png", "jpg"):
            file_base_name = file_name.split(".")[0]
            box_file_path = os.path.join(GAME_CAPTURES_DIR, f"{file_base_name}.box")
            if os.path.exists(box_file_path) and not override:
                continue
            file_path = os.path.join(GAME_CAPTURES_DIR, file_name)
            cmd = BOX_CMD.format(tes_exe=TESSERACT_DEFAULT_WIN_INSTALL_PATH,
                                 image_path=file_path,
                                 box_path=os.path.join(GAME_CAPTURES_DIR, file_base_name))
            print(f"running: {cmd}")
            subprocess.Popen(cmd)
            time.sleep(0.3)
    validiate_empty_box_files(GAME_CAPTURES_DIR)

if __name__ == "__main__":
    make_game_captures_box_files()