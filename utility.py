from mss.windows import MSS as mss
import numpy as np
import win32gui
import time


class Utility:
    def __init__(self):
        pass

    def get_sct(self, monitor: dict()) -> np.ndarray:
        """Gets a screenshot of the selected area
        
        Args:
            monitor (dict): screenshot capture area
            Example: {"top": 936, "left": 908, "width": 28, "height": 11}
        Returns:
            np.ndarray: returns an image of the selected area as numpy ndarray
        """
        with mss() as sct:
            return np.array(sct.grab(monitor))

    def get_target_window_info(self, toggle: bool, is_target_active: bool, window_rect: list) -> (bool, list):
        """Gets target window info

        Returns:
            Passes information to the following class attributes:
            window_rect: rect of target window
            is_target_active: true/false if target window foregrounded
        """
        while True:
            if toggle.value:
                foreground_window = win32gui.GetForegroundWindow()
                target_hwnd = win32gui.FindWindow("UnrealWindow", None)
                if target_hwnd:
                    if target_hwnd != foreground_window:
                        is_target_active.value = False
                        time.sleep(.5)
                    else:
                        is_target_active.value = True
                        rect = win32gui.GetWindowRect(target_hwnd)
                        window_rect[0] = rect[0] #posx
                        window_rect[1] = rect[1] #posy
                        window_rect[2] = rect[2] - rect[0] #width
                        window_rect[3] = rect[3] - rect[1] #height
                        time.sleep(.5)
                else:
                    time.sleep(5)
            else:
                break