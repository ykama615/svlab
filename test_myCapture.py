import cv2
import win32gui
import argparse
import myCapture as mycap


def main(args):
    if args.name!=None:
        mcapp = win32gui.FindWindow(None, args.name)
        args.box = win32gui.GetWindowRect(mcapp)
        args.device= 99
    cap = mycap.CameraSelector(args.device, args.fps, args.size, args.box)

    while cap.isOpened():
        ret, fnum, frame = cap.read()

        if ret:
            cv2.imshow("video", frame)
            if cv2.waitKey(int(1000/cap.fps)) == ord('q'):
                break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    parser = argparse.ArgumentParser(
        description="--name \'window_name\' \n --device \'camera_num(99 is screen capture)\' \n--fps num")
    parser.add_argument('--name', type=str,
                        help="--name \'window_name\'")
    parser.add_argument('--device', type=int,
                        help="--device \'camera_num(99 is screen capture)\'")
    parser.add_argument('--fps', type=int)
    def stype(ssize): return list(map(int, ssize.split(',')))
    parser.add_argument('--size', type=stype, help="width,height")
    parser.add_argument('--box', type=stype, help="x,y,width,height")
    args = parser.parse_args()
    main(args)

