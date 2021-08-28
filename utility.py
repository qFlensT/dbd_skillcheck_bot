from PyQt5.QtWidgets import QFileDialog
from mss.windows import MSS as mss
import numpy as np
from os import getcwd


class Utility:
    def __init__(self) -> None:
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
        
    def get_file_path(self, parent) -> str:
        file_path = QFileDialog.getOpenFileName(parent, "Open Image",
                                                getcwd(), "Image files (*.jpg *.png)")[0]
        return file_path