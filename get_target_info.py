import win32gui
import time


def get_target_window_info(toggle: bool, is_target_active: bool, window_rect: list) -> (bool, list):
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