# -*- coding: utf-8 -*-
import cv2
import myCapture as mycap
import myPhysiology as mp
import time

dev = 0

def main():
    cap = mycap.CameraSelector(dnum=dev, fps=60, size=[720, 1280])
    mpd = mp.MpDetector()

    while cap.isOpened():
        ret, fnum, frame = cap.read()
        start = time.perf_counter()

        if ret:
            detections = mpd.getFace(frame, False)
            for [box, keys] in detections:
                if box!=[]:
                    cv2.rectangle(frame, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), [0,255,0], 1)
                if keys!=[]:
                    for points in keys:
                        cv2.circle(frame, points, 3, [255,0,0], -1)
            ########################################################################################
            poses = mpd.getPose(frame)
            for point in poses:
                x, y, z, ret = point
                if ret:
                    scale = abs(int(5 * (z/cap.wt-1.0)))
                    cv2.circle(frame, [x, y], scale, [0,0,255], -1)
            ########################################################################################

            cv2.imshow("video", frame)
            if cv2.waitKey(int(1000/cap.fps)) == ord('q'):
                break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
