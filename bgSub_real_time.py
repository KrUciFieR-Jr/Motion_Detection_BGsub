import numpy as np
import cv2
import time
cap = cv2.VideoCapture('assign.mp4')
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
ret, frame = cap.read()
fgmask1= fgbg.apply(frame)
c=0
no_of_frames=1
thresh_prev=np.array([[0]])
notStarted=True
while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    no_of_frames +=1
    sparse = fgmask-fgmask1
    thresh = cv2.threshold(sparse,25,255,cv2.THRESH_BINARY)[1]
    m=thresh.shape[0]*thresh.shape[1]
    thresh_avg = np.sum(np.sum(thresh,axis=0,keepdims=True),axis=1,keepdims=True)/m
    print(thresh_avg)
    if(thresh_avg-thresh_prev==0 and notStarted==True and thresh_avg>2):
    	print("Started")
    	t_start = time.ctime()
    	notStarted=False
    	print(t_start)
    if(thresh_avg-thresh_prev==0 and notStarted==False and thresh_avg==0):
    	print("End")
    	c=0
    	notStarted=True
    	t_end = time.ctime()
    	with open('outptu.txt','a+') as f:
    		f.write('Start: '+t_start+" End: "+t_end
    				+" Difference: "+str(abs((int(t_end[11:13])-int(t_start[11:13]))))+":"
    				+str(abs((int(t_end[14:16])-int(t_start[14:16]))))+":"
    				+str((abs(int(t_end[17:19])-int(t_start[17:19]))))
    				+"\n")
    cv2.imshow('frame',fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    fgmask1=fgmask
    thresh_prev=thresh_avg
f.close()
cap.release()
cv2.destroyAllWindows()