from pynput import keyboard
import pyautogui
import time


def auto_m2(toggle: bool, is_target_active: bool, am2_keycode: object=keyboard.Key.alt_gr) -> None:
    prev_press = time.time()
    
    def on_press(key):
        nonlocal prev_press
        
        if toggle.value:
            if is_target_active.value:
                current_press = time.time()
                if key == am2_keycode: 
                    if (current_press - prev_press) <= 0.3:
                        pyautogui.mouseDown(button="right")
                        prev_press = current_press
                    else:
                        pyautogui.mouseUp(button="right")
                        prev_press = current_press
        else:
            return False

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()