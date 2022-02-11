# TechVidvan Vehicle counting and Classification
# Import necessary packages

from cmath import pi
import cv2
import csv
import collections
from cv2 import WINDOW_NORMAL
import numpy as np
from tracker import *
from scipy.spatial import distance as dist
from PIL import Image
from math import sqrt

# path = "C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/imageprocessing/"
path = "D:/Ultimate-Real-Time-Traffic-Management-System/codes/imageprocessing/"

# Initialize Tracker
tracker = EuclideanDistTracker()

input_size = 320

# Detection confidence threshold
confThreshold =0.2
nmsThreshold= 0.2

font_color = (0, 0, 255)
font_size = 0.5
font_thickness = 2

# Middle cross line position
middle_line_position = 225   
up_line_position = middle_line_position - 15
down_line_position = middle_line_position + 15


# Store Coco Names in a list
classesFile = path + "coco.names"
classNames = open(classesFile).read().strip().split('\n')
print(classNames)
print(len(classNames))

# class index for our required detection classes
required_class_index = [2, 3, 5, 7]

detected_classNames = []

## Model Files
modelConfiguration = path +'yolov3-320.cfg'
modelWeigheights = path +'yolov3-320.weights'

# configure the network model
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeigheights)

# Configure the network backend

# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Define random colour for each class
np.random.seed(42)
colors = np.random.randint(0, 255, size=(len(classNames), 3), dtype='uint8')


# Function for finding the center of a rectangle
def find_center(x, y, w, h):
    x1=int(w/2)
    y1=int(h/2)
    cx = x+x1
    cy=y+y1
    return cx, cy
    
# List for store vehicle count information
temp_up_list = []
temp_down_list = []
up_list = [0, 0, 0, 0]
down_list = [0, 0, 0, 0]




# Function for count vehicle
def count_vehicle(box_id, img):

    x, y, w, h, id, index = box_id
    

    # Find the center of the rectangle for detection
    center = find_center(x, y, w, h)
    ix, iy = center
    
    # Find the current position of the vehicle
    if (iy > up_line_position) and (iy < middle_line_position):

        if id not in temp_up_list:
            temp_up_list.append(id)

    elif iy < down_line_position and iy > middle_line_position:
        if id not in temp_down_list:
            temp_down_list.append(id)
            
    elif iy < up_line_position:
        if id in temp_down_list:
            temp_down_list.remove(id)
            up_list[index] = up_list[index]+1

    elif iy > down_line_position:
        if id in temp_up_list:
            temp_up_list.remove(id)
            down_list[index] = down_list[index] + 1

    # Draw circle in the middle of the rectangle
    cv2.circle(img, center, 2, (0, 0, 255), -1)  # end here
    # print(up_list, down_list)

# Function for finding the detected objects from the network output
def postProcess(outputs,img):
    global detected_classNames 
    detected_classNames = []
    height, width = img.shape[:2]
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
   
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if classId in required_class_index:
                if confidence > confThreshold:
                    # print(classId)
                    w,h = int(det[2]*width) , int(det[3]*height)
                    x,y = int((det[0]*width)-w/2) , int((det[1]*height)-h/2)
                    boxes.append([x,y,w,h])
                    classIds.append(classId)
                    confidence_scores.append(float(confidence))

    # Apply Non-Max Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidence_scores, confThreshold, nmsThreshold)
    # print(classIds)
    for i in indices.flatten():
        x, y, w, h = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]
        print(x , " ", y)
        if(maxx < x):
            maxx = x
            xmaxy = y
        if(minx > x):
            minx = x
            xminy = y
        if(maxy < y):
            maxy =y
        if(miny > y):
            miny = y 
        # print(x,y,w,h)

        color = [int(c) for c in colors[classIds[i]]]
        name = classNames[classIds[i]]
        detected_classNames.append(name)
        # Draw classname and confidence score 
        cv2.putText(img,f'{name.upper()} {int(confidence_scores[i]*100)}%',(x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        # Draw bounding rectangle
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
        detection.append([x, y, w, h, required_class_index.index(classIds[i])])

    # Update the tracker for each object
    boxes_ids = tracker.update(detection)
    for box_id in boxes_ids:
        count_vehicle(box_id, img)
    return minx,maxx,maxy,miny,xmaxy,xminy

image_file = 'vehicle classification-image02.png'
def from_static_image(image):
    vehicle_area = 0
    img = cv2.imread(image)

    blob = cv2.dnn.blobFromImage(img, 1 / 255, (input_size, input_size), [0, 0, 0], 1, crop=False)

    # Set the input of the network
    net.setInput(blob)
    layersNames = net.getLayerNames()
    
    outputNames = ['yolo_82', 'yolo_94', 'yolo_106']
    
    # outputNames = [(layersNames[i[0] - 1]) for i in net.getUnconnectedOutLayers()]
    
    # Feed data to the network
    outputs = net.forward(outputNames)

    # Find the objects from the network output
    minx,maxx,maxy,miny, xmaxy, xminy = postProcess(outputs,img)
    breadth = maxx-minx
    height = maxy-miny
    print(maxx, " ", minx)  
    print(breadth)
    # road_area = breadth * height
    # ratio = (float)(road_area/vehicle_area)

    # count the frequency of detected classes
    frequency = collections.Counter(detected_classNames)
    f = dict(frequency)
    print(frequency)
    # Draw counting texts in the frame
    cv2.putText(img, "Car:        "+str(frequency['car']), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
    cv2.putText(img, "Motorbike:  "+str(frequency['motorbike']), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
    cv2.putText(img, "Bus:        "+str(frequency['bus']), (20, 80), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
    cv2.putText(img, "Truck:      "+str(frequency['truck']), (20, 100), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)


    # cv2.imshow("image", img)
    # cv2.waitKey(0)

    cv2.namedWindow('image',WINDOW_NORMAL)
    cv2.resizeWindow('image', 800,600) # to resize the output window
    cv2.imshow("image", img)
    
    #finding the breadth of a road in meters
    pixels = np.array(img)
    width, height, channels = pixels.shape
    actual_width = 5
    pixel_distance = sqrt((maxx - minx) ** 2 + (xmaxy - xminy) ** 2)
    actual_distance = (pixel_distance / width) * actual_width
    
    if(actual_distance <=3.75):
        actual_distance = 3.75  #single lane
    
    elif(actual_distance > 3.75 and actual_distance <=5.5):
        actual_distance = 5.5  #intermidiate lane
    
    elif(actual_distance > 5.5 and actual_distance <=7):
        actual_distance = 7    #double lane without kerbs
    
    elif(actual_distance > 7 and actual_distance <=7.5):
        actual_distance = 7.5  #double lane with kerbs
        
    elif(actual_distance > 7.5 and actual_distance <=11.25):
        actual_distance = 11.25  #three lane
        
    elif(actual_distance > 11.25 and actual_distance <=15):
        actual_distance = 15   #4 lane
        
    elif(actual_distance > 15 and actual_distance <=18.75):
        actual_distance = 18.75   #5lane
    
    elif(actual_distance > 18.75 and actual_distance <=22.5):
        actual_distance = 22.5     #6 lane
    
    cv2.waitKey(0)
    
    # save the data to a csv file
    # with open("static-data.csv", 'a') as f1:
    #     cwriter = csv.writer(f1)
    #     cwriter.writerow([image, frequency['car'], frequency['motorbike'], frequency['bus'], frequency['truck']])
    # f1.close()
    
    f1 ={}
    list1 = ['car','motorbike','bus', 'truck']
    for a in list1:
        if(a in f.keys()):
            pass
        else:
            f1[str(a)] = 0
    
    f1.update(f) 
    vehicle_area = f1['car']*8.245 + f1['motorbike']*1.834 + f1['bus']*35.7 + f1['truck']*51.8
    f1['breadth'] = actual_distance
    f1['vehicle_area'] = vehicle_area
    f1['miny'] = miny
    f1['maxy'] = maxy
    return f1

cv2.destroyAllWindows()

if __name__ == '__main__':
    # realTime()
    from_static_image("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/traffic-4.jpg")
    # from_static_image("D:/Ultimate-Real-Time-Traffic-Management-System/codes/videos/traffic-4.jpg")
