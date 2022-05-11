import cv2
import myCapture as mycap

def main():
    cap = mycap.CameraSelector(99, 30, [100, 100])
    while cap.isOpened():
        ret, fnum, frame = cap.read()

        if ret:
            cv2.imshow("video", frame)
            if cv2.waitKey(int(1000/cap.fps)) == ord('q'):
                break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
