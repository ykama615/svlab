# -*- coding: utf-8 -*-
import cv2
import numpy as np
import myCapture as mycap
import myPhysiology as myphy
import time

dev = 0

def main():
    cap = mycap.CameraSelector(dnum=dev, fps=30, size=[720, 1280])
    dlib = myphy.DlibFaceDetector()
    cvf  = myphy.cvFaceDetector()
    cstmf = myphy.customOneFaceDetector()

    while cap.isOpened():
        ret, fnum, frame = cap.read()

        if ret:
            '''
            ## Dlib and OpenCV Facemark API ######
            start = time.perf_counter()
            dets, _, _ = dlib.getFace(frame)
            print("dlib {:.3f}".format(time.perf_counter()-start))
            start = time.perf_counter()
            cvfs, _, _ = cvf.getFace(frame)
            print("cv2 {:.3f}".format(time.perf_counter()-start))

            if len(dets)>0:
                for i, face in enumerate(dets):
                    cv2.rectangle(frame, (face[0], face[1]), (face[0]+face[2], face[1]+face[3]), [0, 0, 255], 1)

                    parts = dlib.getFacemark_detection(frame, face)
                    for x,y in parts:
                        cv2.circle(frame, (x,y), 3, [128, 128, 255], -1)

            if len(cvfs)>0:
                for i, face in enumerate(cvfs):
                    cv2.rectangle(frame, (face[0], face[1]), (face[0]+face[2], face[1]+face[3]), [0, 255, 255], 1)

                    parts = cvf.getFacemark_detection(frame, face)
                    for x,y in parts:
                        cv2.circle(frame, (x,y), 3, [128, 255, 255], -1)
            '''
            cstmf.linkedImage(frame)

            #start = time.perf_counter()
            face = cstmf.getFace()
            #print("cstm {:.3f}".format(time.perf_counter()-start))

            if len(face)>0:
                cv2.rectangle(frame, (face[0], face[1]), (face[0]+face[2], face[1]+face[3]), [0, 0, 255], 1)

                #start = time.perf_counter()
                parts = cstmf.getFacemark_detection()
                #print("parts {:.3f}".format(time.perf_counter()-start))
                if len(parts)>0:
                    for x,y in parts:
                        cv2.circle(frame, (x,y), 3, [128, 128, 255], -1)


            cv2.imshow("video", frame)
        
        if cv2.waitKey(int(1000/cap.fps)) == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
