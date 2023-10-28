# python built in
import os
import subprocess
import pathlib
import shutil
import time
from typing import Union, Generator

# site packages
import cv2
import fuzzywuzzy.fuzz
from fuzzywuzzy import fuzz

# own modules
from screen_reader.screen_reader_constants import TESSERACT_DEFAULT_WIN_INSTALL_PATH

BOX_CMD = "{tes_exe} {image_path} {box_path} batch.nochop makebox"
DEFAULT_BOX = os.path.join(pathlib.Path(__file__).parent.resolve(), "default_box.box")
GAME_CAPTURES_DIR = os.path.join(pathlib.Path(__file__).parent.resolve(), "game_captures")

LEVEL_UP_Y_LINE_COORDS = (362, 286, 235, 196, 154, 115, 75, 35)
BIG_LINE_Y_COORDS = (362,)

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

def file_path_generator(dir_path):
    # type: (str) -> Generator[str, None, None]
    """
    convince function for iterating across a dir and
    getting back the full file path and not the name

    Args:
        dir_path (str): path to the dir we want to iterate

    """
    if not os.path.exists(dir_path):
        raise OSError(f"given path {dir_path} does not exist and cannot be iterated")
    for file_name in os.listdir(dir_path):
        full_path = os.path.join(dir_path, file_name)
        if os.path.isfile(full_path):
            yield full_path

def extract_line_image_and_boxes(img_path, box_path, y_coord, height, output_img_path, output_box_path, threshold=5):
    # Load the image
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)

    # box files use a different coord system (bottom left) flip the Y coord to be image space


    y_coord_new = img.shape[:2][0] - y_coord
    y_start = y_coord_new
    y_end = y_coord_new + height + 1
    print(f"cropping region {y_start} to {y_end}")
    cropped_img = img[y_start:y_end, :]

    # Save the cropped image
    print(f"saving {output_img_path}")
    cv2.imwrite(output_img_path, cropped_img)

    new_boxes = []
    tokens = []
    with open(box_path, 'r') as f:
        lines = f.readlines()
        threshold_range = list(range(y_coord-threshold, y_coord+threshold))
        box_y_coord_start = y_coord - height
        print(f"threshold_range is {threshold_range}")
        for line in lines:
            parts = line.strip().split(' ')
            char, x1, y1, x2, y2 = parts[0], int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4])

            # Check if this box's Y coordinates are close to the target Y coordinate
            if y2 in threshold_range:
                print(f"{char} is with in range of target ")
                # Adjust Y coordinates

                y1_new = y1 - box_y_coord_start - 1
                y2_new = y2 - box_y_coord_start + 1
                tokens.append(char)
                new_boxes.append(f"{char} {x1} {y1_new} {x2} {y2_new}\n")
    tokens_str = "".join(tokens)

    # Write the new boxes to the output box file
    with open(output_box_path, 'w') as f:
        print(f"writing {output_box_path} with {tokens_str}")
        f.writelines(new_boxes)

def slice_level_up_screen(output_dir):
    data = "E:\\Python\\Ai_Knight\\screen_reader\\font_train\\data_capture\\hcure_level_up\\bad"
    for image_path in file_path_generator(data):
        path_bits = image_path.split(".")
        if path_bits[-1] == "png":
            box_path = f"{path_bits[0]}.box"
            for index, y_coord in enumerate(LEVEL_UP_Y_LINE_COORDS):
                print("_________________________________")
                base_name = os.path.basename(image_path).split(".")[0]
                output_file_path = os.path.join(output_dir, f"{base_name}_{str(index)}.png")
                box_file_out_put = os.path.join(output_dir, f"{base_name}_{str(index)}.box")
                print(f"with Y coord {y_coord}, will make {output_file_path} using {image_path} box_path is {box_file_out_put}")
                if y_coord in BIG_LINE_Y_COORDS:
                    height = 55
                else:
                    height = 24
                extract_line_image_and_boxes(image_path, box_path,
                                             y_coord, height, output_file_path,
                                             box_file_out_put)


def dynamic_threshold(string_length):
    """Calculate dynamic threshold based on string length."""

    min_threshold = 65
    max_threshold = 85

    # Linear interpolation between min and max thresholds
    # This will start at min_threshold for string_length = 1
    # and gradually increase to max_threshold as string_length increases
    threshold = min_threshold + (max_threshold - min_threshold) * (string_length - 1) / 100
    return min(max_threshold, threshold)


def str_is_similar(string_to_check, str_to_compare, threshold=None):
    if not threshold:
        threshold = dynamic_threshold(min(len(string_to_check), len(str_to_compare)))
    return threshold <= fuzzywuzzy.fuzz.ratio(string_to_check, str_to_compare)


if __name__ == "__main__":
    #make_game_captures_box_files()
    slice_level_up_screen("E:\\Python\\Ai_Knight\\screen_reader\\font_train\\data_capture\\hcure_level_up")