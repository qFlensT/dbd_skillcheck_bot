from utility import Utility
import numpy as np
import cv2
from pynput.keyboard import Controller, KeyCode
from time import sleep


class AutoWigle(Utility):
    def __init__(self):
        super().__init__()

    def auto_wigle(self, toggle: bool, is_target_active: bool) -> None:
        """auto_wigle function
        NEED TO REWORK
        """
        low_white = np.array([250, 250, 250])
        high_white = np.array([255, 255, 255])

        monitor_arrow = {"top": 936, "left": 908, "width": 28, "height": 11}
        monitor_hand = {"top": 840, "left": 780, "width": 35, "height": 50}

        arrow = False # an arrow icon appears on the screen when you need to wigle

        while True:
            if toggle.value:
                if is_target_active:

                    arrow_img = cv2.cvtColor(self.get_sct(monitor_arrow), cv2.COLOR_BGR2RGB)
                    white_range_arrow = cv2.inRange(arrow_img, low_white, high_white)
                    white_range_arrow_cords = set(tuple(zip(np.where(white_range_arrow != 0)[0], np.where(white_range_arrow != 0)[1])))

                    if len(white_range_arrow_cords) > 18 and arrow == False: # 18 - number of pixels on the screen
                        arrow = True
                    if arrow:
                        Controller().press(KeyCode(0x41))
                        sleep(.05)
                        Controller().press(KeyCode(0x44))
                        sleep(.05)
                        Controller().release(KeyCode(0x41))
                        sleep(.05)
                        Controller().release(KeyCode(0x44))

                        hand_img = cv2.cvtColor(self.get_sct(monitor_hand), cv2.COLOR_BGR2RGB)
                        white_range_hand = cv2.inRange(hand_img, low_white, high_white)
                        white_range_hand_cords = set(tuple(zip(np.where(white_range_hand != 0)[0], np.where(white_range_hand != 0)[1])))

                        if len(white_range_hand_cords) < 400:
                            arrow = False
            else:
                break