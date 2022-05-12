# -*- coding: utf-8 -*-
import time
import ctypes
import win32gui
import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab

class CameraSelector:
    __device: int
    __cap: cv2.VideoCapture
    __frame_seed: float
    fps: int
    wt: int
    ht: int
    __titleflag: bool
    __bbox = []

    def __init__(self, dnum, fps, size, box=None):
        if dnum is not None:
            self.__device = dnum
        else:
            self.__device = 0

        if fps is not None:
            self.fps = fps
        else:
            self.fps = 30

        if size is not None:
            self.wt = size[0]
            self.ht = size[1]
        else:
            self.ht = -1
            self.wt = -1

        if box is not None:
            if len(box) != 4:
                self.__scarea = [-1, -1, -1, -1]
            self.__scarea = box
            self.__titleflag = True
        else:
            self.__scarea = [-1, -1, -1, -1]
            self.__titleflag = False

        self.camera_connect()

    def __set_seed(self):
        self.__frame_seed = time.perf_counter()

    def camera_connect(self):
        if self.__device == 99:
            self.__scflag = False
            self.__cap = None
        elif self.__device >= 0:
            self.__cap = cv2.VideoCapture(self.__device)
            self.__cap.set(cv2.CAP_PROP_FPS, self.fps)
            if self.ht > 0 and self.wt > 0:
                self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.wt)
                self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.ht)

        self.__set_seed()
        self.printStatus()

        return self.__cap

    def printStatus(self):
        print("-----------------------------------------")
        if self.__device == 99:
            print("ScreenCapture")
            print("Ctrl+Click: Window Select")
            print("Shift+Click: Area Select")
            self.fps = 30
            print("-----------------------------------------")
            return
        
        if self.__device >= 0:
            self.wt = self.__cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.ht = self.__cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            fps = self.__cap.get(cv2.CAP_PROP_FPS)
            print("Camera(", self.__device, ")")

        print(self.ht, "x", self.wt, "@", fps)
        if fps != self.fps:
            print("CAUTION: fps cannot be set to the specified value")
            self.fps = fps
        print("-----------------------------------------")

    def read(self):
        if self.__device == 99:
            if self.__titleflag:
                self.__titleflag = False
                print(self.__scarea)
                x0, y0, x1, y1 = self.__scarea[0], self.__scarea[1], self.__scarea[0] + \
                    self.__scarea[2], self.__scarea[1]+self.__scarea[3]
                self.__bbox = (x0, y0, x1, y1)
            elif self.__getCtrlClick():
                self.__titleflag = False
                # print(pyautogui.position())
                print(win32gui.GetWindowText(
                    win32gui.GetForegroundWindow()))
                x0, y0, x1, y1 = win32gui.GetWindowRect(
                    win32gui.GetForegroundWindow())
                self.__bbox = (x0, y0, x1, y1)
            elif self.__getShiftClick():
                self.__titleflag = False
                # print(pyautogui.position())
                if self.__scarea == [-1, -1, -1, -1]:
                    self.__scarea = [
                        0, 0, pyautogui.size()[0], pyautogui.size()[1]]
                print(self.__scarea)
                x0, y0, x1, y1 = self.__scarea[0], self.__scarea[1], self.__scarea[0] + \
                    self.__scarea[2], self.__scarea[1]+self.__scarea[3]
                self.__bbox = (x0, y0, x1, y1)

            fnum = int((time.perf_counter()-self.__frame_seed)*self.fps)
            if len(self.__bbox) != 0:
                fnum = int((time.perf_counter()-self.__frame_seed)*self.fps)
                frame = cv2.cvtColor(np.asarray(ImageGrab.grab(
                    self.__bbox, all_screens=True)), cv2.COLOR_RGB2BGR)
                return True, fnum, frame
            else:
                return False, fnum, None

        elif self.__device >= 0:
            ret, frame = self.__cap.read()
            fnum = int((time.perf_counter()-self.__frame_seed)*self.fps)
            return ret, fnum, frame#cv2.flip(frame, 1)

    def isOpened(self):
        if self.__device == 99:
            return True
        elif self.__device >= 0:
            return self.__cap.isOpened()
        elif self.__device == -1:
            return (self.__cap.get_device() != None)

    def release(self):
        if self.__device == 99:
            return True
        elif self.__device >= 0:
            return self.__cap.release()
        elif self.__device == -1:
            return (self.pipeline.stop())

    def __getCtrlClick(self):
        #Ctrl + Click
        return bool(ctypes.windll.user32.GetAsyncKeyState(0x01) == 0x8000 & ctypes.windll.user32.GetAsyncKeyState(0x11) == 0x8000)

    def __getShiftClick(self):
        #Shift + Click
        return bool(ctypes.windll.user32.GetAsyncKeyState(0x01) == 0x8000 & ctypes.windll.user32.GetAsyncKeyState(0x10) == 0x8000)
