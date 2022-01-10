# Main idea is to use 
# 1. Frame Differencing
# 2. Image Thresholding
# 3. Contours Finding
# 4. Image Dilation

#importing modules
import os
import re
import cv2 # opencv library
import numpy as np
from os.path import isfile, join
import matplotlib.pyplot as plt

# 1. extract video frames
# Opens the inbuilt camera of laptop to capture video.
cap = cv2.VideoCapture('C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/cars.mp4')
i = 0

while(cap.isOpened()):
	ret, frame = cap.read()
	
	# This condition prevents from infinite looping
	# incase video ends.
	if ret == False:
		break
	
	# Save Frame by Frame into disk using imwrite method
	cv2.imwrite('C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/frames/Frame'+str(i)+'.jpg', frame)
	i += 1


# 2. import video frames
# get file names of the frames
col_frames = os.listdir('C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/frames/')

# sort file names
col_frames.sort(key=lambda f: int(re.sub('\D', '', f)))

# empty list to store the frames
col_images=[]

for j in col_frames:
    # read the frames
    img = cv2.imread('C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/frames/'+j)
    # append the frames to the list
    col_images.append(img)

# 3. 
# kernel for image dilation
kernel = np.ones((4,4),np.uint8)

# font style
font = cv2.FONT_HERSHEY_SIMPLEX

# directory to save the ouput frames
pathIn = "C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/outputframes/"

for i in range(len(col_images)-1):
    
    # frame differencing
    grayA = cv2.cvtColor(col_images[i], cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(col_images[i+1], cv2.COLOR_BGR2GRAY)
    diff_image = cv2.absdiff(grayB, grayA)
    
    # image thresholding
    ret, thresh = cv2.threshold(diff_image, 30, 255, cv2.THRESH_BINARY)
    
    # image dilation
    dilated = cv2.dilate(thresh,kernel,iterations = 1)
    
    # find contours
    contours, hierarchy = cv2.findContours(dilated.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    
    # shortlist contours appearing in the detection zone
    valid_cntrs = []
    for cntr in contours:
        x,y,w,h = cv2.boundingRect(cntr)
        if (x <= 200) & (y >= 10) & (cv2.contourArea(cntr) >= 25):
            if (y >= 20) & (cv2.contourArea(cntr) < 40):
                break
            valid_cntrs.append(cntr)
            
    # add contours to original frames
    dmy = col_images[i].copy()
    cv2.drawContours(dmy, valid_cntrs, -1, (127,200,0), 2)
    
    cv2.putText(dmy, "vehicles detected: " + str(len(valid_cntrs)), (10, 15), font, 0.3, (255, 255, 255), 1)
    cv2.line(dmy, (0, 10),(256,10),(100, 255, 255))
    cv2.imwrite(pathIn+str(i)+'.png',dmy)  

# 4 . video preparation
# specify video name
pathOut = 'vehicle_detection_v3.mp4'

# specify frames per second
fps = 14.0

# 5. 
frame_array = []
files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]

# 6. 
files.sort(key=lambda f: int(re.sub('\D', '', f)))

for i in range(len(files)):
    filename=pathIn + files[i]
    
    #read frames
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    
    #inserting the frames into an image array
    frame_array.append(img)

    # 7. 
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])

    out.release()


# releases resources
cap.release()
cv2.destroyAllWindows()

