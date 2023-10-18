# python built in
import os
import subprocess
import pathlib
import shutil

# own modules
from screen_reader.screen_reader_constants import TESSERACT_DEFAULT_WIN_INSTALL_PATH

BOX_CMD = "{tes_exe} {image_path} {image_name} batch.nochop makebox"
DEFAULT_BOX = os.path.join(pathlib.Path(__file__).parent.resolve(), "default_box.box")

def make_box_file_for_dir(root_dir, image_exts=("png", "jpg"), output_dir=False):
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
                                 image_name=box_output)
            subprocess.Popen(cmd)

def validiate_empty_box_files(root_dir):
    for file_name in os.listdir(root_dir):
        file_ext = file_name.split(".")[-1]
        file_path = os.path.join(root_dir, file_name)
        if file_ext == "box" and int(os.path.getsize(file_path)) == 0:
            print(f"Replacing bad box for {file_name}")
            os.remove(file_path)
            shutil.copy(DEFAULT_BOX, file_path)

