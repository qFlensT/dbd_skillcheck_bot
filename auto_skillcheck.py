from utility import Utility
import numpy as np
import cv2
from pynput.keyboard import Controller, KeyCode
from time import sleep


class AutoSkillCheck(Utility):
    def __init__(self):

        super().__init__()

    def auto_skillcheck(self, toggle: bool, is_target_active: bool, 
                        window_rect: list, keycode: object=KeyCode(0x43)):
        """auto_skillcheck function
        """
        low_white = np.array([250, 250, 250])
        high_white = np.array([255, 255, 255])

        low_red = np.array([160, 0, 0])
        high_red = np.array([255, 30, 30])

        white_cords_buffer = set()

        while True:
            if toggle.value:
                if is_target_active.value:
                    monitor = {"top": int(window_rect[3]/2 + window_rect[1] - 70), #screenshot capture area
                            "left": int(window_rect[2]/2 + window_rect[0] - 70), 
                            "width": 140, 
                            "height": 140}

                    img = cv2.cvtColor(self.get_sct(monitor), cv2.COLOR_BGR2RGB)

                    white_range = cv2.inRange(img, low_white, high_white)
                    red_range = cv2.inRange(img, low_red, high_red)

                    white_range_cords = set(tuple(zip(np.where(white_range != 0)[0], np.where(white_range != 0)[1])))
                    red_range_cords = set(tuple(zip(np.where(red_range != 0)[0], np.where(red_range != 0)[1])))
                    
                    if len(white_range_cords) > 0:
                        white_cords_buffer.update(white_range_cords)
                    
                    if len(white_cords_buffer) > 0 and len(red_range_cords) > 0:
                        if red_range_cords.intersection(white_cords_buffer):
                            Controller().press(keycode)
                            Controller().release(keycode)
                            white_cords_buffer = set()
                            sleep(1)
                            
                    if len(red_range_cords) == 0:
                        white_cords_buffer = set()
            else:
                break