import cv2
import numpy as np
import mss
from pynput.keyboard import Controller
from time import sleep
from multiprocessing import Process, Value, Array
import win32gui
from ctypes import c_bool, c_int


def GetTargetWindowInfo(isTargetActive:c_bool, WindowClassName:str, Rect:c_int):
    isTargetActive.value = False
    while True:
        ForegroundWindow = win32gui.GetForegroundWindow()
        target_hwnd = win32gui.FindWindow(WindowClassName, None)

        if target_hwnd != ForegroundWindow:
            isTargetActive.value = False
        else:
            isTargetActive.value = True
            rect = win32gui.GetWindowRect(target_hwnd)
            Rect[0] = rect[0] #posx
            Rect[1] = rect[1] #posy
            Rect[2] = rect[2] - rect[0] #width
            Rect[3] = rect[3] - rect[1] #height

def GenerateMaskSkillcheck(isTargetActive, Rect):
    low_white = np.array([250, 250, 250])
    high_white = np.array([255, 255, 255])

    low_red = np.array([160, 0, 0])
    high_red = np.array([255, 30, 30])

    # monitor_skillcheck = {"top": 470, "left": 890, "width": 140, "height": 140}

    cordsw = set()

    while True:
        if isTargetActive.value:
            monitor_skillcheck = {"top": int(Rect[3]/2 + Rect[1] - 70), "left": int(Rect[2]/2 + Rect[0] - 70), "width": 140, "height": 140}
            simg = np.array(mss.mss().grab(monitor_skillcheck))
            rgb_image = cv2.cvtColor(simg, cv2.COLOR_BGR2RGB)
            skillw = cv2.inRange(rgb_image, low_white, high_white)
            skillr = cv2.inRange(rgb_image, low_red, high_red)
            cordsr = set()
            yw, xw = np.where(skillw != 0)
            yr, xr = np.where(skillr != 0)

            for i in range(len(yw)):
                cordsw.add(f"{xw[i]}x{yw[i]}")
            for i in range(len(yr)):
                cordsr.add(f"{xr[i]}x{yr[i]}")

            if cordsr.intersection(cordsw):
                Controller().press("c")
                Controller().release("c")
                cordsw = set()

            if len(yw) == 0 and len(yr) == 0:
                cordsw = set()
            if len(cordsr) == 0:
                cordsw = set()
            cv2.imshow("mask", skillr + skillw)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                break

def GenerateMaskWigle(isTargetActive, Rect):
    low_white = np.array([250, 250, 250])
    high_white = np.array([255, 255, 255])

    arrow = False

    monitor_arrow = {"top": 936, "left": 908, "width": 28, "height": 11}
    monitor_hand = {"top": 840, "left": 780, "width": 35, "height": 50}

    while True:
        if isTargetActive.value:
            wimg = np.array(mss.mss().grab(monitor_arrow))
            rgb_image = cv2.cvtColor(wimg, cv2.COLOR_BGR2RGB)
            wiglew = cv2.inRange(rgb_image, low_white, high_white)
            yw, xw = np.where(wiglew != 0)
            if len(yw) > 18 and arrow == False:
                arrow = True
            if arrow:
                Controller().press("a")
                sleep(.05)
                Controller().press("d")
                sleep(.05)
                Controller().release("a")
                sleep(.05)
                Controller().release("d")

                himg = np.array(mss.mss().grab(monitor_hand))
                rgb_himg = cv2.cvtColor(himg, cv2.COLOR_BGR2RGB)
                handw = cv2.inRange(rgb_himg, low_white, high_white)
                yhw, xhw = np.where(handw != 0)

                if len(yhw) < 400:
                    arrow = False

            if cv2.waitKey(25) & 0xFF == ord("q"):
                break

            
def main():
    isTargetActive = Value(c_bool, False)
    Rect = Array(c_int, range(4))
    Process(target=GetTargetWindowInfo, args=(isTargetActive, "UnrealWindow", Rect)).start()
    Process(target=GenerateMaskSkillcheck, args=(isTargetActive, Rect)).start()
    # Process(target=GenerateMaskWigle, args=(isTargetActive, Rect)).start()
        
if __name__ == "__main__":
    main()