# python built in
import os.path
import pathlib
import matplotlib.pyplot as plt
import json

# site packages
import cv2
import pytesseract

# own modules
import screen_reader.screen_reader_constants as screen_reader_constants
from screen_reader.font_train.training_utils import file_path_generator
from screen_reader.font_train.training_utils import str_is_similar

class FontTester():
    """
    Class for read test of an image
    """
    own_path = pathlib.Path(__file__).parent.resolve()
    test_data_dir = os.path.join(own_path, "test_data")

    def __init__(self, model_to_test):
        tessract_install_path = screen_reader_constants.TESSERACT_DEFAULT_WIN_INSTALL_PATH
        pytesseract.pytesseract.tesseract_cmd = tessract_install_path

        model_to_test = model_to_test.replace("\\", "/")

        self.model_data_dir = os.path.dirname(model_to_test)
        self.model_name = os.path.basename(model_to_test).split(".")[0]

        self.test_files = [f for f in file_path_generator(self.test_data_dir) if f.split(".")[-1] == "png"]
        with open(os.path.join(self.test_data_dir, "results.json"), "r")  as results_file:
            self.answer_sheet = json.load(results_file)

    def test_data(self):
        results = list()
        for test_file in self.test_files:
            image =cv2.cvtColor(cv2.imread(test_file), cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(image, lang=self.model_name,
                                               config=f"--tessdata-dir {self.model_data_dir} --psm 6")
            text = text.replace("\n", "")
            image_name = os.path.basename(test_file).split(".")[0]
            answer = self.answer_sheet.get(image_name, "").replace("\n", "")
            result = {"match": str_is_similar(text, answer),
                      "expected result:": answer,
                      "actual result:": text}
            results.append(result)
        self.display_results(results)

    def display_results(self, results):
        failed = list()
        passed = list()
        for result in results:
            print(result)
            if result['match']:
                passed.append(result)
            else:
                failed.append(result)

        print(f"success rate is {len(passed) / len(results) *100}%, "
              f"fail rate is {len(failed) / len(results) *100}%")

if __name__ == "__main__":
    tester = FontTester(os.path.join(pathlib.Path(__file__).parent.resolve(), "trained_model/hcure_font_model_4"))
    tester.test_data()

# HCure Time coords (on my screen)
# top Left: X:1224, Y:426
# bottom right: 1327, Y:457
# box 110 wide and 35 tall to be safe
#