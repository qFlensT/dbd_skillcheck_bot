from pynput import keyboard
import pyautogui
import time


class AutoM1:
    def __init__(self):
        pass

    def auto_m1(self, toggle: bool, is_target_active: bool, am1_keycode: object=keyboard.Key.alt_l) -> None:
        prev_press = time.time()

        def on_press(key):
            nonlocal prev_press
            if toggle.value:
                if is_target_active:
                    current_press = time.time()

                    if key == am1_keycode:
                        if (current_press - prev_press) <= 0.3: # looking for doubleclick
                            pyautogui.mouseDown()
                            prev_press = current_press
                        else:
                            prev_press = current_press
                            pyautogui.mouseUp()
            else:
                return False
    
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()