# python built in
import subprocess
import time

# site packages
import win32gui
import win32process
import psutil
import win32con
import win32ui
from PIL import Image, ImageOps


class GameVisionClass:

    def __init__(self, game_exe_proc_id, vision_model, parent_id_search=True):
        self.proc_id = game_exe_proc_id
        self.vision_model_path = vision_model
        self.states = dict()

        # get the handler of the exe id
        self.matched_handler = None
        self.get_exe_handle(parent_id_search)

    def get_exe_handle(self, search_parent_procs=True):
        # type: (bool) -> None
        """
        Find the handler ID associated with our target process ID and update class attribute

        Args:
            search_parent_procs (bool): should we check the parent process
            to see if that spawned the currently selected proc

        """

        def callback(hwnd, target_process_ids):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                _, found_proc_id = win32process.GetWindowThreadProcessId(hwnd)
                found_ids = [found_proc_id]
                if search_parent_procs:
                    process = psutil.Process(found_proc_id)
                    found_ids.append(process.ppid())
                for found_id in found_ids:
                    if found_id in target_process_ids:
                        self.matched_handler = hwnd
            return True

        win32gui.EnumWindows(callback, [self.proc_id])

    def capture_window(self):
        # type: () -> Image
        """
        Captures the active window of our given process

        Returns:
            (Image) A Pillow image object

        """

        # Get the device context for the entire window
        hwindc = win32gui.GetWindowDC(self.matched_handler)
        left, top, right, bot = win32gui.GetWindowRect(self.matched_handler)
        width = right - left
        height = bot - top

        # Create a device context into which we will draw the capture
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()

        # Create a blank bitmap image the same dimensions as the window
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)

        # BitBlt the window's contents into the bitmap's device context
        memdc.BitBlt((0, 0), (width, height), srcdc, (0, 0), win32con.SRCCOPY)

        # Convert the raw bits of the image into a format that Pillow understands
        bmpinfo = bmp.GetInfo()
        bmpstr = bmp.GetBitmapBits(True)
        image = Image.frombuffer('RGB',
                                 (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                                 bmpstr, 'raw', 'BGRX', 0, 1)
        image = ImageOps.grayscale(image)

        # Free up the device contexts and bitmap objects
        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(self.matched_handler, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())
        return image


if __name__ == "__main__":
    my_h_cure_exe_path = "E:\\holocure\\Game_depolyment\\HoloCure.exe"
    vision_model_path = "E:\\Python\\Ai_Knight\\screen_reader\\font_train\\trained_model\\hcure_font_model_4.traineddata"
    proc = subprocess.Popen(my_h_cure_exe_path)
    time.sleep(20)  # allow the proc to start
    proc_id = proc.pid
    vision = GameVisionClass(proc_id, vision_model_path)
    image = vision.capture_window()
    image.save("E:\\holocure\\game_images\\game_capture_001.png")