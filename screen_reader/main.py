# python built in
import os.path
import matplotlib.pyplot as plt

# site packages
import cv2
import pytesseract

# own modules
import screen_reader_constants


class ScreenReaderBase():
    """
    Class for read test of an image
    """

    def __init__(self):
        self.image = None
        tessract_install_path = screen_reader_constants.TESSERACT_DEFAULT_WIN_INSTALL_PATH
        pytesseract.pytesseract.tesseract_cmd = tessract_install_path


    def load_image(self, image_path):
        # type: (str) -> None
        """
        Load an image an convert image into OpenCv2 and convert it to Grayscale

        :param image_path:
        :return:
        """

        # load the image and convert to grayscale
        image = cv2.cvtColor(cv2.imread(image_path),
                             cv2.COLOR_BGR2GRAY)
        image_thresh = cv2.adaptiveThreshold(image, 155, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY, 11, 2)
        self.image = image


    def image_analysis(self, image_path):
        self.load_image(image_path)
        image_analysis = dict()

        for roi_name, roi_coords in screen_reader_constants.GAME_ROIS.items():
            image_analysis[roi_name] = self.check_roi(roi_coords, debug_show=True)

        print(f"analysis of {os.path.basename(image_path)}: {image_analysis}")


    def check_roi(self, roi_coords, debug_show=False):
        # type: (dict[str, int], bool) -> str
        roi = self.image[roi_coords['start_y']:roi_coords['end_y'],
                         roi_coords['start_x']:roi_coords['end_x']]

        if debug_show:
            plt.imshow(roi, cmap='gray', interpolation='bicubic')
            plt.show()

        collected_str = pytesseract.image_to_string(roi, config='--psm 12')
        print(f"found this string {collected_str}")
        return collected_str


if __name__ == "__main__":
    import pathlib
    screen_reader = ScreenReaderBase()

    test_image = os.path.join(pathlib.Path(__file__).parent.resolve(),
                              screen_reader_constants.TEST_IMAGE_GAME)
    screen_reader.image_analysis(test_image)

