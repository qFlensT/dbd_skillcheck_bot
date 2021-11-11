from typing import Union
from utility import Utility
import numpy as np
import cv2
from pynput.keyboard import Controller, KeyCode
from time import sleep


def auto_skillcheck(toggle: bool, is_target_active: bool, 
                    window_rect: list, sct_monitor: Union[dict, str], keycode: object=KeyCode(0x43)):
    """auto_skillcheck function
    """
    
    low_white = np.array([250, 250, 250])
    high_white = np.array([255, 255, 255])

    low_red = np.array([160, 0, 0])
    high_red = np.array([255, 30, 30])
    
    last_rect = None
    utility = Utility()

    monitor = sct_monitor

    white_cords_buffer = set()

    while True:
        if toggle.value:
            if is_target_active.value:
                
                if (window_rect != last_rect) and (sct_monitor == "default"):
                    monitor = {"top": int(window_rect[3]/2 + window_rect[1] - 70), #screenshot capture area
                            "left": int(window_rect[2]/2 + window_rect[0] - 70), 
                            "width": 140, 
                            "height": 140}
                    last_rect = monitor.copy()

                img = cv2.cvtColor(utility.get_sct(monitor), cv2.COLOR_BGR2RGB)

                white_range = cv2.inRange(img, low_white, high_white)
                red_range = cv2.inRange(img, low_red, high_red)
                
                white_cords_array = np.where(white_range != 0)
                red_cords_array = np.where(red_range != 0)

                white_range_cords = set(tuple(zip(white_cords_array[0], white_cords_array[1])))
                red_range_cords = set(tuple(zip(red_cords_array[0], red_cords_array[1])))
                
                if len(white_range_cords) > 0:
                    white_cords_buffer.update(white_range_cords)
                
                if len(white_cords_buffer) > 0 and len(red_range_cords) > 0:
                    if red_range_cords.intersection(white_cords_buffer):
                        Controller().tap(keycode)
                        white_cords_buffer.clear()
                        sleep(1)
                        
                if len(red_range_cords) == 0:
                    white_cords_buffer.clear()
        else:
            break