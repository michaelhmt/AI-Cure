# python built in
import os
import pathlib
import shutil
import subprocess

# site packages
import cv2

# own modules
from screen_reader.screen_reader_constants import TESSERACT_DEFAULT_WIN_INSTALL_PATH, \
                                                  TESSERACT_LSTMF_WIN_EXE, TESSERACT_EN_LAST_CHECKPOINT
from screen_reader.font_train.training_utils import file_path_generator
import screen_reader.game_screen_vision.vision_utils as vision_utils

# psm 6 assume all the text data is on roughly the same line psm 3 the text can be anywhere
LSTM_CMD_PSM_6 = '"{tes_exe}" {train_image} {lstm_output} --psm 6 lstm.train'
LSTM_CMD_PSM_3 = '"{tes_exe}" {train_image} {lstm_output} --psm 3 lstm.train'
FINE_TUNE_CMD = 'start cmd.exe /c "{lstmf_train_exe}" ' \
                "--model_output {output_dir} " \
                "--traineddata {base_model} "\
                "--train_listfile {training_list} " \
                "--max_iterations {training_iterations} " \
                "--continue_from {last_check}   PAUSE"
NON_ALINGED_DATA_PREXIS = {"__none__"}

class FontTrainer:
    own_dir = pathlib.Path(__file__).parent.resolve()

    def __init__(self, training_data_dir, base_model, training_data_exts=("png", "jpg")):
        self.t_data_root = training_data_dir
        self.training_exts = training_data_exts
        self.base_model = base_model

        self.lstmf_dir = os.path.join(self.own_dir, "lstmf")
        self.lstmf_files = list()
        self.ready_to_train = False
        self.base_model = base_model
        self.model_dir = os.path.join(self.own_dir, "model_result")

        self.staged_training_files = list()

        try:
            os.makedirs(self.lstmf_dir)
        except FileExistsError:
            pass
        try:
            os.makedirs(self.model_dir)
        except FileExistsError:
            pass
        self.training_data = self.collect_training_data()

    def collect_training_data(self):
        # type: () -> list
        """
        Collect all valid training images

        Returns:
            (list): list of the path for all valid training images

        """
        return [path for path in file_path_generator(self.t_data_root)
                if self.is_valid_data(path)]

    def move_to_staging_and_gray_scale(self):
        staging_folder = os.path.join(self.own_dir, "data_staging")
        self.staged_training_files = list()

        for file_path in self.collect_training_data():
            base_name = os.path.basename(file_path)
            file_name = base_name.split(".")[0]
            path_no_ext = file_path.split(".")[0]
            box_file = f"{path_no_ext}.box"

            image_copy_path = os.path.join(staging_folder, base_name)
            shutil.copy(box_file, os.path.join(staging_folder, f"{file_name}.box"))
            gray_image = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2GRAY)
            treated_image = vision_utils.mid_gray_non_white_blakcs(vision_utils.convert_cv2_to_pil(gray_image))
            gray_image = vision_utils.convert_pil_to_cv2(treated_image)

            cv2.imwrite(image_copy_path, gray_image)
            self.staged_training_files.append(image_copy_path)


    def is_valid_data(self, file_path):
        # type: (str) -> bool
        """
        ensure a given file is of the correct image type and that
        .box and .txt files exist for it

        Args:
            file_path (str): path of the file to check

        Returns:
            (bool) True if the file is valid

        """
        path_no_ext = file_path.split(".")[0]
        ext = file_path.split(".")[1]
        box_file = f"{path_no_ext}.box"
        #txt_file = f"{path_no_ext}.txt"

        box_exists = os.path.exists(box_file)
        #txt_exists = os.path.exists(txt_file)
        ext_is_valid = ext in self.training_exts
        if box_exists and ext_is_valid:
            return True
        else:
            return False

    def make_lstmf_files(self):
        """
        Make lstmf files from the collected training data and output to lstmf dir.
        updates internal list of lstmf files

        """

        lstmf_file_list = list()
        for training_image_path in self.staged_training_files:
            image_name = os.path.basename(training_image_path).split(".")[0]
            lstmf_file_path = os.path.join(self.lstmf_dir, image_name)
            if any([True for prexs in NON_ALINGED_DATA_PREXIS if prexs in image_name]):
                cmd_template = LSTM_CMD_PSM_3
            else:
                cmd_template = LSTM_CMD_PSM_6

            cmd = cmd_template.format(tes_exe=TESSERACT_DEFAULT_WIN_INSTALL_PATH,
                                      train_image=training_image_path,
                                      lstm_output=lstmf_file_path)
            lstmf_file_list.append(f"{lstmf_file_path}.lstmf")
            print(f"Running lstmf command for {image_name} cmd is: {cmd}")
            subprocess.call(cmd)

        generated_files = list()
        for lstmf_file in lstmf_file_list:
            if not os.path.exists(lstmf_file):
                print(f"{os.path.basename(lstmf_file)} does not exist and failed training")
            else:
                generated_files.append(lstmf_file)
        self.lstmf_files = generated_files

    def fine_tune_training(self, steps):
        # type: (int) -> None
        """
        Finetune on top of an existing model with our created data

        Args:
            steps (int): max number of training iterations
        """

        if not self.ready_to_train or not self.lstmf_files:
            print("Model is not ready to be trained or no lstmf file have been created")

        # make training files list document
        training_file_list_txt = os.path.join(self.model_dir, "training_files.txt")
        with open(training_file_list_txt, "w+", newline="\n") as training_list_file:
            for lstmf_file in self.lstmf_files:
                # this needs to be unix line ending otherwise things get breaky
                training_list_file.write(lstmf_file + '\n')
        cmd = FINE_TUNE_CMD.format(lstmf_train_exe=TESSERACT_LSTMF_WIN_EXE,
                                   output_dir=os.path.join(self.model_dir, "hcure_font_model"),
                                   base_model=self.base_model,
                                   training_list=training_file_list_txt,
                                   training_iterations=steps,
                                   last_check=TESSERACT_EN_LAST_CHECKPOINT)

        # call the cmd and wait for this to finish will bring up a cmd window
        print(f"running {cmd}")
        subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    def train(self, steps=4000):
        # make and collect lstmf files for training
        self.move_to_staging_and_gray_scale()
        self.make_lstmf_files()
        self.ready_to_train = True
        self.fine_tune_training(steps=steps)

if __name__ == "__main__":
    current_dir = pathlib.Path(__file__).parent.resolve()
    training_data_dir = os.path.join(current_dir, "training_data")
    base_model = os.path.join(current_dir, "base_model/eng.traineddata")

    trainer = FontTrainer(training_data_dir, base_model)
    trainer.make_lstmf_files()
    trainer.train(steps=1900)
