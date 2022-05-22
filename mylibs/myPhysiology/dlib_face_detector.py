# -*- coding: utf-8 -*-
import cv2
import numpy as np
import dlib
from imutils import face_utils
from os.path import dirname, abspath

class DlibFaceDetector:
    def __init__(self):
        #self.detector = dlib.simple_object_detector("./learned_model/detector.svm")
        #self.predictor = dlib.shape_predictor(dirname(abspath(__file__))+"/learned_model/predictor.dat")
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(dirname(abspath(__file__))+"/learned_model/shape_predictor_68_face_landmarks.dat")

    def getFace(self, frame):
        dets, scores, _ = self.detector.run(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 1)
        faces = []
        for n in range(len(dets)):
            faces.append([dets[n].left(), dets[n].top(), dets[n].width(), dets[n].height()])

        return faces, scores, len(dets)

    def getFacemark_detection(self, frame, face):
        dets = dlib.rectangle(left=face[0], right=face[0]+face[2], top=face[1], bottom=face[1]+face[2])

        parts = face_utils.shape_to_np(self.predictor(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), dets), dtype=np.int32)

        return parts
