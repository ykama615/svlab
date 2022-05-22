# -*- coding: utf-8 -*-
import cv2
import numpy as np
from os.path import dirname, abspath

class cvFaceDetector:
    def __init__(self):
        self.detector = cv2.CascadeClassifier(dirname(abspath(__file__))+"/learned_model/haarcascades/haarcascade_frontalface_default.xml")
        self.predictor = cv2.face.createFacemarkLBF()
        self.predictor.loadModel(dirname(abspath(__file__))+"/learned_model/lbfmodel.yaml")

    def getFace(self, frame):
        dets = self.detector.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 1.1, 5)

        return dets, None, len(dets)

    def getFacemark_detection(self, frame, dets):
        ret, landmarks = self.predictor.fit(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), np.array([dets]))
        parts = np.array(landmarks[0][0], dtype=np.int32)

        return parts
