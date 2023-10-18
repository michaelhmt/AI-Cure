# python built in
import os.path
import pathlib
import shutil

# site packages
from PIL import Image, ImageDraw, ImageFont

# own modules
from screen_reader.font_train.training_utils import make_box_file_for_dir, validiate_empty_box_files

BASE_SHEET = os.path.join(pathlib.Path(__file__).parent.resolve(),
                          "training_sheet_base.txt")
FONT_MAP = {"text": "BestTen-CRT.otf",
            "numbers": "PixelMplus12-Regular.ttf"}
BASE_DATA_ROOT = os.path.join(pathlib.Path(__file__).parent.resolve(), "base_data")
GAME_CAPTURES_ROOT = os.path.join(pathlib.Path(__file__).parent.resolve(), "game_captures")
TRAINING_DATA_MAIN = os.path.join(pathlib.Path(__file__).parent.resolve(), "training_data")

class FontTraining:
    own_path = pathlib.Path(__file__).parent.resolve()

    def make_base_data(self):

        if not os.path.exists(BASE_SHEET):
            print(f"base sheet not found at: {BASE_SHEET}")
            return
        if os.path.exists(BASE_DATA_ROOT):
            # if the training data has been run clear it and start again
            shutil.rmtree(BASE_DATA_ROOT)
        os.makedirs(BASE_DATA_ROOT)

        with open(BASE_SHEET, "r") as base_sheet:
            # we will create a training image for every line of text in the base sheet
            for index, line in enumerate(base_sheet.readlines()):
                data_number = index + 1
                if line.replace(" ", "").replace("\n", "").isnumeric():
                    font_file = FONT_MAP["numbers"]
                else:
                    font_file = FONT_MAP["text"]
                font_path = os.path.join(self.own_path, "fonts", font_file)
                file_name = f"h_cure_font_train_{data_number}"
                image_out_path = os.path.join(BASE_DATA_ROOT, f"{file_name}.png")
                text_out_path = os.path.join(BASE_DATA_ROOT, f"{file_name}.txt")
                image_width = len(line) * 12 + 12
                self.make_image(line, font_path, image_out_path, image_width)
                with open(text_out_path, "w+") as text_result:
                    text_result.write(line)

        make_box_file_for_dir(BASE_DATA_ROOT)
        validiate_empty_box_files(BASE_DATA_ROOT)


    @staticmethod
    def make_image(text, font_path, image_path, width):
        image = Image.new('RGB', (width,40), color='white')
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, 20)

        draw.text((10, 10), text, font=font, fill='white',
                  stroke_width=2, stroke_fill='black')
        image.save(image_path)


if __name__ == "__main__":
    training_obj = FontTraining()
    training_obj.make_base_data()