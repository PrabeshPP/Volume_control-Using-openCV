import math
import cv2 as cv
import numpy as np
import hand_detection_module as hd
import time
from ctypes import POINTER ,cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume

height,width=640,480
cap=cv.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)
cap.set(10,150)
current_time=0
post_time=0
detector=hd.detect_hand(detection=0.7)

devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(
    IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))



# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
minVol=volRange[0]
maxVol=volRange[1]
volBar=400
volPercentage=0


while True:


    ret,frame=cap.read()
    frame=cv.flip(frame,1)
    cv.rectangle(frame, (50, 150), (85, 400), (0, 0, 0), 2,cv.LINE_AA)
    frame1=detector.show_hand(frame)
    lm_list=detector.getposition(frame,False)
    if len(lm_list)!=0:
        x1,y1=lm_list[4][1],lm_list[4][2]
        x2,y2=lm_list[8][1],lm_list[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        cv.circle(frame,(x1,y1),5,(255,0,0),-1)
        cv.circle(frame, (x2, y2), 5, (255, 0, 0), -1)
        cv.line(frame,(x1,y1),(x2,y2),(255,0,255),2,cv.LINE_AA)
        cv.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
        length=math.hypot(x2-x1,y2-y1)
        vol=np.interp(length,[50,300],[minVol,maxVol])
        volume.SetMasterVolumeLevel(vol, None)
        volBar=np.interp(length,[50,300],[400,150])
        volPercentage=np.interp(length,[50,300],[0,100])
        if length<50:
            cv.circle(frame1, (cx, cy), 5, (0, 255, 0), -1)




    current_time=time.time()
    fps=1/(current_time-post_time)
    post_time=current_time
    cv.rectangle(frame,(50,int(volBar)),(85,400),(0,255,0),-1,cv.LINE_AA)
    cv.putText(frame,f"FPS:{str(int(fps))}",(10,40),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv.LINE_AA)
    cv.putText(frame1,f"{int(volPercentage)}%",(40,430),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv.LINE_AA)
    cv.imshow("video", frame1)
    if cv.waitKey(1)==ord('q'):
        break



cap.release()
cv.destroyAllWindows()