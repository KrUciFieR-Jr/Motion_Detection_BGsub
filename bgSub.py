import numpy as np
import cv2
import time
cap = cv2.VideoCapture('alone.mp4')
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
ret, frame = cap.read()
fgmask1= fgbg.apply(frame)
c=0
no_of_frames=1
t_start_array = []
t_end_array = []
thresh_prev=np.array([[0]])
notStarted=True
while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    no_of_frames +=1
    try:
        sparse = fgmask-fgmask1
    except TypeError:
        for i in range(0,len(t_end_array)):
            print(no_of_frames)
            with open('output.txt','a') as f:
                f.write("Start: "+str(round(t_start_array[i]/1000.0*no_of_frames))
                    +" End: "+str(round(t_end_array[i]/1000.0*no_of_frames))
                    +" Difference: "+str(round(abs(t_start_array[i]-t_end_array[i])/1000.0*no_of_frames))
                    +"\n")
    thresh = cv2.threshold(sparse,25,255,cv2.THRESH_BINARY)[1]
    m=thresh.shape[0]*thresh.shape[1]
    thresh_avg = np.sum(np.sum(thresh,axis=0,keepdims=True),axis=1,keepdims=True)/m
    print(thresh_avg)
    if(thresh_avg-thresh_prev==0 and notStarted==True and thresh_avg>2):
        print("Started")
        t_start = time.time()
        t_start_array.append(t_start)
        notStarted=False
        print(t_start)
    if(thresh_avg-thresh_prev==0 and notStarted==False and thresh_avg==0):
        print("End")
        notStarted=True
        t_end = time.time()
        t_end_array.append(t_end)        
    cv2.imshow('frame',fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    fgmask1=fgmask
    thresh_prev=thresh_avg
cap.release()
cv2.destroyAllWindows()