# -*- coding: utf-8 -*-
import cv2
import numpy as np
from . import dlib_face_detector as dfd
from . import mediapipe_detector as mpd

class customOneFaceDetector:
    def __init__(self):
        self.mp = mpd.MpDetector()
        self.df = dfd.DlibFaceDetector()

        self.__crop_base = []
        self.__crop_area = []
        self.__face = []

    def linkedImage(self, frame):
        self.__frame = frame.copy()
        self.__ht, self.__wt = frame.shape[:2]

    def getFace(self):
        if self.__frame == []:
            return []

        #if self.__crop_area == []:
        self.__crop_area = self.__frame
        self.__crop_base = [0, 0]

        dets = self.mp.getFace(self.__crop_area)
        if len(dets)>0:
            dets = self.__mp_alignment(dets)
        else:
            self.crop_area = self.__frame
            self.__crop_base = [0, 0]
            dets = self.mp.getFace(self.__crop_area)
            if len(dets)>0:
                dets = self.__mp_alignment(dets)
            else:
                dets, _, _ = self.df.getFace(self.__crop_area)
                if len(dets)==0:
                    return []
                else:
                    dets = dets[0]

        self.__face = [self.__crop_base[0]+dets[0], self.__crop_base[1]+dets[1], dets[2], dets[3]]
        sw = (int)(dets[2]/4)-1
        sh = (int)(dets[3]/4)-1

        x1 = max(0, dets[0]-sw)
        y1 = max(0, dets[1]-sh)
        x2 = min(dets[0]+dets[2]+sw, self.__wt)
        y2 = min(dets[1]+dets[3]+sh, self.__ht)

        self.__crop_base = [x1, y1]
        self.__crop_area = self.__frame[y1:y2, x1:x2]

        return self.__face

    def getFacemark_detection(self):
        if self.__frame == [] or self.__face == []:
            return []

        if self.__crop_area == []:
            self.__crop_area = self.__frame

        parts = self.df.getFacemark_detection(self.__frame, self.__face)

        return parts

    def __mp_alignment(self, dets):
        dets = dets[0][0]
        ht = int(dets[3]/10)
        wt = int(dets[2]/10)
        dets = [dets[0]-int(wt/2), dets[1]-int(ht/2), dets[2]+wt, dets[3]+ht]

        return dets