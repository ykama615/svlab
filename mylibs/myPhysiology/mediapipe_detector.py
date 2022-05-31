# -*- coding: utf-8 -*-
import cv2
import numpy as np
import mediapipe as mp
from typing import List

class MpDetector:
    hflag = False
    pflag = False
    lhand_points: List
    rhand_points: List
    sresults = []

    def __init__(self, detection=0.2, tracking=0.2):
        self.hands = mp.solutions.hands.Hands(
            min_detection_confidence=detection, min_tracking_confidence=tracking)
        self.pose = mp.solutions.pose.Pose(
            static_image_mode=False, model_complexity=1, enable_segmentation=False , min_detection_confidence=detection, min_tracking_confidence=tracking)
        self.fmesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=detection)
        self.face = mp.solutions.face_detection.FaceDetection(
            model_selection=0, min_detection_confidence=detection)
        self.segment = mp.solutions.selfie_segmentation.SelfieSegmentation(
            model_selection=0)

    def getFace(self, frame, getkeys=True):
        ht, wt, _ = frame.shape
        results = self.face.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        rpoint_list = []
        face_box = []
        face_keypoints = []
        if results.detections is not None:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                face_box = [int(bbox.xmin*wt), int(bbox.ymin*ht), int(bbox.width*wt), int(bbox.height*ht)]
                if getkeys:
                    for i, landmark in enumerate(results.detections[0].location_data.relative_keypoints):
                        x = max(1, min(int(landmark.x * wt), wt-1))
                        y = max(1, min(int(landmark.y * ht), ht-1))
                        face_keypoints.append([int(x), int(y)])
                rpoint_list.append([face_box, face_keypoints])
        return rpoint_list

    def getHand(self, frame):
        ht, wt, _ = frame.shape
        results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        rpoint_list = []
        lhand_points = []
        rhand_points = []
        if results.multi_hand_landmarks is not None:
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                if results.multi_handedness[i].classification[0].label == "Left":
                    for i, landmark in enumerate(hand_landmarks.landmark):
                        x = max(1, min(int(landmark.x * wt), wt-1))
                        y = max(1, min(int(landmark.y * ht), ht-1))
                        lhand_points.append([int(x), int(y), landmark.z])
                elif results.multi_handedness[i].classification[0].label == "Right":
                    for i, landmark in enumerate(hand_landmarks.landmark):
                        x = max(1, min(int(landmark.x * wt), wt-1))
                        y = max(1, min(int(landmark.y * ht), ht-1))
                        rhand_points.append([int(x), int(y), landmark.z])
            rpoint_list.append([lhand_points, rhand_points])
        return rpoint_list

    def getPose(self, frame): # Mediapipe can detect only one person.
        ht, wt, _ = frame.shape
        results = self.pose.process(frame)
        pose_points = []
        if results.pose_landmarks is not None:
            for i, point in enumerate(results.pose_landmarks.landmark):
                x = min(int(point.x * wt), wt-1)
                y = min(int(point.y * ht), ht-1)
                z = int(point.z * wt)
                pose_points.append([x, y, z, point.visibility])
        return pose_points

    def getSegmentImage(self, frame, bgimage=[], dep=0.5):
        res = []
        if len(self.sresults) != 0:
            print("done")
            return res

        self.sresults = self.segment.process(frame)

        if self.sresults.segmentation_mask is not None:
            condition = np.stack(
                (self.sresults.segmentation_mask, )*3, axis=-1) > dep
            if len(bgimage) == 0:
                bg = np.ones(frame.shape, dtype=np.uint8)*255
            else:
                bg = bgimage
            res = np.where(condition, frame, bg)

        self.sresults = []

        return res
