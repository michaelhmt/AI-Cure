# Site packages
import numpy as np
import cv2
from PIL import Image

# own modules
from screen_reader.screen_reader_constants import HCURE_ROIS
from screen_reader.game_screen_vision.state_object import GameVisualState

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MID_GRAY = (128, 128, 128)


def make_hcure_game_states():
    states = list()
    for name, roi in HCURE_ROIS.items():
        state = GameVisualState(name, roi)
        states.append(state)
    return states


def convert_cv2_to_pil(cv2_image):
    return Image.fromarray(cv2_image)


def convert_pil_to_cv2(pil_image, colour_mode=None):
    numpy_image = np.array(pil_image)
    if not colour_mode:
        colour_mode = cv2.COLOR_RGB2BGR
    cv2_image = cv2.cvtColor(numpy_image, colour_mode)
    return cv2_image


def mid_gray_non_white_blakcs(pil_image):
    # type: (Image.Image) -> Image.Image
    """
    Turn any pixel which isn't pure black or Pure White into a midtone Gray

    Args:
        pil_image (Image): The loaded image we want to operate on

    Returns:
        the processed image

    """
    pil_image = pil_image.convert('RGB')
    pixels = pil_image.load()
    for x_index in range(pil_image.width):
        for y_index in range(pil_image.height):
            current_pixel = pixels[x_index, y_index]
            if current_pixel != WHITE and current_pixel != BLACK:
                pixels[x_index, y_index] = MID_GRAY
    return pil_image
