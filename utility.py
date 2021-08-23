from mss.windows import MSS as mss
import numpy as np


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