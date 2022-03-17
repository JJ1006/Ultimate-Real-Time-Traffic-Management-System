# TechVidvan Vehicle counting and Classification
# Import necessary packages

from cmath import pi
from this import d
import cv2
import csv
import collections
from cv2 import WINDOW_NORMAL
import numpy as np
from tracker import *
from scipy.spatial import distance as dist
from PIL import Image
from math import sqrt

path = "C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/imageprocessing/"
# path = "D:/Ultimate-Real-Time-Traffic-Management-System/codes/imageprocessing/" # path

# Initialize Tracker
tracker = EuclideanDistTracker()

input_size = 320 # input size for the network

# Detection confidence threshold
confThreshold =0.2 # confidence threshold
nmsThreshold= 0.2 # Function for drawing the detected objects

font_color = (0, 0, 255) # font color
font_size = 0.5 # font size
font_thickness = 2 # font thickness

# Middle cross line position
middle_line_position = 225 # middle line position
up_line_position = middle_line_position - 15 # Function for finding the center of a rectangle
down_line_position = middle_line_position + 15 # down line position


# Store Coco Names in a list
classesFile = path + "coco.names" # classes file
classNames = open(classesFile).read().strip().split('\n') # list of class names
print(classNames) # print class names
print(len(classNames)) # Function for drawing the detected objects

# class index for our required detection classes
required_class_index = [2, 3, 5, 7] # required class index

detected_classNames = [] 

## Model Files
modelConfiguration = path +'yolov3-320.cfg' # model configuration file
modelWeigheights = path +'yolov3-320.weights' # model weights file

# configure the network model
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeigheights) # read the network model

# Configure the network backend

# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Define random colour for each class
np.random.seed(42) # random seed
colors = np.random.randint(0, 255, size=(len(classNames), 3), dtype='uint8') # random color for each class


# Function for finding the center of a rectangle
def find_center(x, y, w, h): # find center of a rectangle
    x1=int(w/2) # x1
    y1=int(h/2) # y1
    cx = x+x1 # cx
    cy=y+y1 # cy
    return cx, cy # return cx, cy
    
# List for store vehicle count information
temp_up_list = [] # temp up list
temp_down_list = [] # temp down list
up_list = [0, 0, 0, 0] # up list
down_list = [0, 0, 0, 0] # down list




# Function for count vehicle
def count_vehicle(box_id, img): # count vehicle

    x, y, w, h, id, index = box_id # x, y, w, h, id, index
    

    # Find the center of the rectangle for detection
    center = find_center(x, y, w, h) # center
    ix, iy = center # ix, iy
    
    # Find the current position of the vehicle
    if (iy > up_line_position) and (iy < middle_line_position): # if iy > up_line_position and iy < middle_line_position

        if id not in temp_up_list: # if id not in temp_up_list
            temp_up_list.append(id) # append id to temp_up_list

    elif iy < down_line_position and iy > middle_line_position: # if iy < down_line_position and iy > middle_line_position
        if id not in temp_down_list: # if id not in temp_down_list
            temp_down_list.append(id) # append id to temp_down_list
            
    elif iy < up_line_position: # if iy < up_line_position
        if id in temp_down_list: # if id in temp_down_list
            temp_down_list.remove(id) # remove id from temp_down_list
            up_list[index] = up_list[index]+1 # up_list[index] = up_list[index]+1

    elif iy > down_line_position: # if iy > down_line_position
        if id in temp_up_list: # if id in temp_up_list
            temp_up_list.remove(id) # remove id from temp_up_list
            down_list[index] = down_list[index] + 1 # down_list[index] = down_list[index] + 1

    # Draw circle in the middle of the rectangle
    cv2.circle(img, center, 2, (0, 0, 255), -1)  # end here
    # print(up_list, down_list)

# Function for finding the detected objects from the network output
def postProcess(outputs,img): # after process
    global detected_classNames  
    detected_classNames = [] # detected_classNames
    height, width = img.shape[:2] # height, width
    boxes = [] 
    classIds = []
    confidence_scores = []
    detection = []
    minx=100
    maxx=0
    maxy=0
    miny = 100
    xminy=0
    xmaxy=0
    ymaxx=0
    yminx=0
   
    for output in outputs: # for output in outputs
        for det in output: # for det in output
            scores = det[5:] # scores
            classId = np.argmax(scores) # classId
            confidence = scores[classId] # confidence
            if classId in required_class_index: # if classId in required_class_index
                if confidence > confThreshold: # if confidence > confThreshold
                    # print(classId) # print classId
                    w,h = int(det[2]*width) , int(det[3]*height) # w, h
                    x,y = int((det[0]*width)-w/2) , int((det[1]*height)-h/2) # x, y
                    boxes.append([x,y,w,h]) # boxes.append([x,y,w,h])
                    classIds.append(classId) 
                    confidence_scores.append(float(confidence)) 

    # Apply Non-Max Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidence_scores, confThreshold, nmsThreshold) # indices
    # print(classIds)
    if len(indices) <= 0: # if len(indices) <= 0
        minx=0
        maxx=0
        maxy=0
        miny = 0
        xminy=0
        xmaxy=0
        ymaxx=0
        yminx=0
        return minx,maxx,maxy,miny,xmaxy,xminy,ymaxx,yminx
    else:   
        for i in indices.flatten():
            x, y, w, h = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]
            if(maxx < x):
                maxx = x
                xmaxy = y
            if(minx > x):
                minx = x
                xminy = y
            if(maxy < y):
                maxy =y
                ymaxx =x
            if(miny > y):
                miny = y 
                yminx = x
            # print(x,y,w,h)

            color = [int(c) for c in colors[classIds[i]]] # color
            name = classNames[classIds[i]] # name
            detected_classNames.append(name) # detected_classNames.append(name)
            # Draw classname and confidence score 
            cv2.putText(img,f'{name.upper()} {int(confidence_scores[i]*100)}%',(x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1) # end here

            # Draw bounding rectangle
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 1) # end here
            detection.append([x, y, w, h, required_class_index.index(classIds[i])]) # detection.append([x, y, w, h, required_class_index.index(classIds[i])])

    # Update the tracker for each object
        boxes_ids = tracker.update(detection) # boxes_ids
        for box_id in boxes_ids: # for box_id in boxes_ids
            count_vehicle(box_id, img) # count_vehicle
        return minx,maxx,maxy,miny,xmaxy,xminy,ymaxx,yminx # return minx,maxx,maxy,miny,xmaxy,xminy,ymaxx,yminx

image_file = 'vehicle classification-image02.png' # image_file
def from_static_image(image): # from_static_image
    vehicle_area = 0 # vehicle_area
    img = cv2.imread(image) # img

    blob = cv2.dnn.blobFromImage(img, 1 / 255, (input_size, input_size), [0, 0, 0], 1, crop=False) # blob

    # Set the input of the network
    net.setInput(blob) # net.setInput(blob)
    layersNames = net.getLayerNames() # layersNames
    
    outputNames = ['yolo_82', 'yolo_94', 'yolo_106'] # outputNames
    
    # outputNames = [(layersNames[i[0] - 1]) for i in net.getUnconnectedOutLayers()]
    
    # Feed data to the network
    outputs = net.forward(outputNames) # outputs

    # Find the objects from the network output
    minx,maxx,maxy,miny, xmaxy, xminy, ymaxx, yminx = postProcess(outputs,img) # minx,maxx,maxy,miny, xmaxy, xminy, ymaxx, yminx
    if(minx ==0 and maxx ==0 and maxy ==0 and miny ==0 and xmaxy ==0 and xminy ==0 and ymaxx ==0 and yminx ==0): 
        f = {'car' : 0, 'motorbike' : 0, 'bus' : 0, 'truck' : 0 } 
        print(f)
        f1 = f 
        actual_distance = 1 
        road_length = 1
    else:
        # count the frequency of detected classes
        frequency = collections.Counter(detected_classNames)
        f = dict(frequency) # f
        print(frequency) # print frequency
        # Draw counting texts in the frame
        cv2.putText(img, "Car:        "+str(frequency['car']), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness) # end here
        cv2.putText(img, "Motorbike:  "+str(frequency['motorbike']), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness) # end here
        cv2.putText(img, "Bus:        "+str(frequency['bus']), (20, 80), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness) # end here
        cv2.putText(img, "Truck:      "+str(frequency['truck']), (20, 100), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness) # end here


        # cv2.imshow("image", img)
        # cv2.waitKey(0)

        cv2.namedWindow('image',WINDOW_NORMAL) # cv2.namedWindow('image',WINDOW_NORMAL)
        cv2.resizeWindow('image', 800,600) # to resize the output window
        cv2.imshow("image", img) # cv2.imshow("image", img)
    
        #finding the breadth of a road in meters
        pixels = np.array(img) # pixels
        width, height, channels = pixels.shape # width, height, channels
        actual_width = 5 # actual_width
        pixel_distance = sqrt((maxx - minx) ** 2 + (xmaxy - xminy) ** 2) # pixel_distance
        actual_distance = (pixel_distance / width) * actual_width  # actual_distance
        road_length = 0 # road_length
    
        if(actual_distance <=3.75):
            actual_distance = 3.75  #single lane 17 cars in one lane and 2m ahead clearance
            road_length = 76.5 + (2 * 16)
    
        elif(actual_distance > 3.75 and actual_distance <=5.5):
            actual_distance = 5.5  #intermidiate lane cosidered 12 cars in 1 line and 5 cars parallel 
            road_length = 54 + (2 * 11)
    
        elif(actual_distance > 5.5 and actual_distance <=7):
            actual_distance = 7    #double lane without kerbs 9 cars in 1 line and 2m ahead clearance
            road_length = 40.5 + (2 * 8)
    
        elif(actual_distance > 7 and actual_distance <=7.5):
            actual_distance = 7.5  #double lane with kerbs 9 cars in 1 line and 2m ahead clearance
            road_length = 40.5 + (2 * 8)
        
        elif(actual_distance > 7.5 and actual_distance <=11.25):
            actual_distance = 11.25  #three lane keeping 51 cars as traffic so 17 cars per lane and 2m ahead clearance
            road_length = 76.5 + (2 * 16)
        
        elif(actual_distance > 11.25 and actual_distance <=15):
            actual_distance = 15   #4 lane 51 cars as traffic so 13 cars per lane and 2m ahead clearance
            road_length = 58.5 + (2 * 12)
        
        elif(actual_distance > 15 and actual_distance <=18.75):
            actual_distance = 18.75   #5lane 51 cars as traffic so 11 cars per lane and 2m ahead clearance
            road_length = 49.5 + (10 * 2)
    
        elif(actual_distance > 18.75 and actual_distance <=22.5):
            actual_distance = 22.5     #6 lane 51 cars as traffic so 9 cars per lane and 2m ahead clearance
            road_length = 40.5 + (2 * 8)
    
        cv2.waitKey(0) # cv2.waitKey(0)
    
    # save the data to a csv file
    # with open("static-data.csv", 'a') as f1:
    #     cwriter = csv.writer(f1)
    #     cwriter.writerow([image, frequency['car'], frequency['motorbike'], frequency['bus'], frequency['truck']])
    # f1.close()
    
        f1 ={} # f1
        list1 = ['car','motorbike','bus', 'truck']
        for a in list1:
            if(a in f.keys()):
                pass
            else:
                f1[str(a)] = 0
    
        f1.update(f)  # updating f1
    vehicle_area = (float)(f1['car']*8.245 + f1['motorbike']*1.834 + f1['bus']*35.7 + f1['truck']*51.8)
    f1['breadth'] = actual_distance
    f1['height'] = road_length
    f1['vehicle_area'] = vehicle_area
    f1['miny'] = miny
    f1['maxy'] = maxy
    return f1

cv2.destroyAllWindows() 

if __name__ == '__main__': # main fuction
    # realTime()
    from_static_image("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/example2.jpg")
    # from_static_image("D:/Ultimate-Real-Time-Traffic-Management-System/codes/videos/traffic-4.jpg") 
