import collections
import csv
import threading
import cv2

from numpy import empty
import pandas as pd
import numpy as np
import vehicle_count
import time
import queue
import math
import os

que = queue.Queue()

def greatestLaneCount(arr):
    if(len(arr) ==0 ):
        # arr = os.listdir("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/images_for_loop/")
        arr = os.listdir("D:/Ultimate-Real-Time-Traffic-Management-System/codes/videos/images_for_loop/")
    
    # path = "C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/images_for_loop/"
    path = "D:/Ultimate-Real-Time-Traffic-Management-System/codes/videos/images_for_loop/"
    
    freq1 = vehicle_count.from_static_image(path  + arr[0])
    # freq1 = vehicle_count.from_static_image("D:/Ultimate-Real-Time-Traffic-Management-System/codes/videos/testing.jpg")
    sum1 = freq1['car'] + freq1['motorbike'] + freq1['bus'] + freq1['truck']
    miny1 = freq1['miny']
    maxy1 = freq1['maxy']
    VA1 = freq1['vehicle_area']
    B1 = freq1['breadth']
    road_length1 = freq1['height']
    density1 = float (VA1/ (B1 * road_length1)) * 100.0

    freq2 = vehicle_count.from_static_image(path  + arr[1])
    # freq2 = vehicle_count.from_static_image("D:/Ultimate-Real-Time-Traffic-Management-System/codes/videos/testing.jpg")
    sum2 = freq2['car'] + freq2['motorbike'] + freq2['bus'] + freq2['truck']
    miny2 = freq2['miny']
    maxy2 = freq2['maxy']
    VA2 = freq2['vehicle_area']
    B2 = freq2['breadth']
    road_length2 = freq2['height']
    density2 = float (VA2/ (B2 * road_length2)) * 100.0

    freq3 = vehicle_count.from_static_image(path  + arr[2])
    # freq3 = vehicle_count.from_static_image("D:/Ultimate-Real-Time-Traffic-Management-System/codes/videos/testing.jpg")
    sum3 = freq3['car'] + freq3['motorbike'] + freq3['bus'] + freq3['truck']
    miny3 = freq3['miny']
    maxy3 = freq3['maxy']
    VA3 = freq3['vehicle_area']
    B3 = freq3['breadth']
    road_length3 = freq3['height']
    density3 = float (VA3/ (B3 * road_length3)) * 100.0

    freq4 = vehicle_count.from_static_image(path  + arr[3])
    # freq4 = vehicle_count.from_static_image("D:/Ultimate-Real-Time-Traffic-Management-System/codes/videos/testing.jpg")
    sum4 = freq4['car'] + freq4['motorbike'] + freq4['bus'] + freq4['truck']
    miny4 = freq4['miny']
    maxy4 = freq4['maxy']
    VA4 = freq4['vehicle_area']
    B4 = freq4['breadth']
    road_length4 = freq4['height']
    density4 = float (VA4/ (B4 * road_length4)) * 100.0
    
    one = arr[0]
    two = arr[1]
    three = arr[2]
    four = arr[3]
    arr.remove(one)
    arr.remove(two)
    arr.remove(three)
    arr.remove(four)
    Breadth = [B1, B2, B3, B4]
    freq = [freq1, freq2, freq3, freq4]
    road_length = [road_length1,road_length2, road_length3, road_length4]
    density = [density1, density2, density3, density4]
    print(density)
    return density, Breadth, road_length,freq,arr


def yellow(G, R, s):
    print("t4 yellow started")
    Y = G #green lane becomes yellow for 10 sec
    if(s <= 15):
        time.sleep(5)
    else:
        time.sleep(10) 
    R.append(Y) #now after 10 sec yellow is turned to red 
    print("t4 yellow ended")
   
def green(G, s):
    print("t1 green started")
    G = G
    time.sleep(s)
    print("t1 green ended")

def Red(R, s):
    print("t2 red started")
    R = R
    time.sleep(s)
    print("t2 red ended")

def find_next_green_Lane(density5): #make sure this thread takes less than 10 sec so that we are ready with next green lane number before the yellow turns into red
    print("t5 greenlanefind started")
    
    density, Breadth5, road_length5 , freq, arr = greatestLaneCount(density5['arr'])
    density5['density'] = density
    density5['Breadth'] = Breadth5
    density5['road_length'] = road_length5
    density5['freq'] = freq
    density5['arr'] = arr
    return density5 
    
    

def setting(G,R,s, arr):
    if(s <= 15):
        t1= threading.Thread(target=green, args= (G, math.ceil(s/2)))
    else:
        t1= threading.Thread(target=green, args= (G, s-10))
    t2= threading.Thread(target=Red, args= (R, s))
    t1.start()
    t2.start()
    t4 = threading.Thread(target=yellow, args = (G,R,s))  #starting yellow for 10sec
    density5={'arr' : arr}
    t5 = threading.Thread(target=lambda q, arg1: q.put(find_next_green_Lane(density5)), args=(que,density5)) 
    t5.start()
    t5.join()
    print("t5 ended")
    t1.join() #to make sure that t1 i.e green thread has completed
    t4.start()
    t2.join()
    t4.join()
    result = que.get() 
    
    return result


def newG(G):
    Index = [0,0,0,0] #for row indexes of last occurences of 1,2,3,4
    one,two,three,four = True,True,True,True
    time_count = [0,0,0,0]
    # df = pd.read_csv("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/static-data.csv",header=None)
    df = pd.read_csv("D:/Ultimate-Real-Time-Traffic-Management-System/static-data.csv",header=None)
    df1 = pd.DataFrame(df,index=None)  
    csvfile = df1.to_numpy().tolist()          
    # print(csvfile)
    j = len(csvfile)-1
    for a in csvfile[-1::-1]:
        print(a, " a")
        if(a[0] == 1 and one is True and j>0):
            Index[0] = csvfile.index(a)
            j=j-1
            one = False
        if(a[0] == 2 and two is True and j>0):
            Index[1] = csvfile.index(a)
            j=j-1
            two = False
        if(a[0] == 3 and three is True and j>0):
            Index[2] = csvfile.index(a)
            j=j-1
            three = False
        if(a[0] == 4 and four is True and j>0):
            Index[3] = csvfile.index(a)
            j=j-1
            four = False
        if(j==0 or ((one is False) and (two is False) and (three is False) and (four is False))):
            break
                
    print(Index,"index check")  
    consider = [0,1,2,3]
    rowlast = csvfile[-1]
    consider.remove(rowlast[0]-1)
    for i in consider:
        print([x[2] for x in csvfile[Index[i]+1 : len(csvfile)] ])
        time_count[i]= sum([x[2] for x in csvfile[Index[i]+1 : len(csvfile)] ]) #sum of all the time_counts of the lanes
    maxcount = max(time_count) #max time_count of the lanes
    if(maxcount>=140): #if maxcount is greater than 140 then we have to consider all the lanes
        G = time_count.index(maxcount)+1 #lane number
        print(G, " G changed for 140") #lane number
    return G    
        
def Find_If_Any_Lane_140(density,Breadth, road_length,freq, arr , G, R):
    with open('static-data.csv', 'r',newline="") as read_obj:  #if max density comes of same lane then don't consider that lane and check again for rest of the lanes
        print(" in case 1 int type G code")
        csv_reader = csv.reader(read_obj)
        row1 = list(csv_reader)[-1]
        
        print("in")
        if(G == int(row1[0])):
            print("Same G as previous lane so ignoring this G and changing")
            print(density)
            density[G-1] = 0
            print(density)
            which_lane_to_choose(density,Breadth, road_length,freq, arr , G, R)
        G = newG(G)           
        
    return G

#assuming side 1 has red ,side 2 has green, side 3 has red, side 4 has red as an initial case
   
def which_lane_to_choose(density,Breadth, road_length, freq, arr,G, R):
    if(max(density) >= maxdensity): #case1 when max number of vehicles is greater than maxcount 
        print("In case 1")
        G = density.index(max(density))+1 #give the lane number to green signal to turn that signal green   
        G = Find_If_Any_Lane_140(density,Breadth, road_length,freq, arr , G, R)
        AllLane2 = [1,2,3,4]
        AllLane2.remove(G)
        R = AllLane2 #to turn all the other lanes red      
        print(G, " ", R)
        seconds = (road_length[G-1]/3.2) + 5
        
        # save the data to a csv file
        with open("static-data.csv", 'a', newline="") as f1:
            cwriter = csv.writer(f1)
            cwriter.writerow([ G , R , seconds])
        f1.close()
        
        result = setting(G,R,seconds, arr)
        density = result['density']
        Breadth = result['Breadth']
        road_length = result['road_length']
        freq = result['freq']
        arr = result['arr']
        which_lane_to_choose(density,Breadth, road_length,freq, arr , G, R)

    if(max(density) < 7.0): #clockwise
        print("In case 2")
        G = density.index(max(density))+1
        G = Find_If_Any_Lane_140(density,Breadth, road_length,freq, arr , G, R)
                
        AllLane2 = [1,2,3,4]
        AllLane2.remove(G)
        R = AllLane2
        print(G, " ", R)
        seconds = 5
        
        # save the data to a csv file
        with open("static-data.csv", 'a',newline="") as f1:
            cwriter = csv.writer(f1)
            cwriter.writerow([ G , R , int(math.ceil(seconds/2) + 5)])
        f1.close()
    
        
        result = setting(G,R,seconds, arr)
        density = result['density']
        Breadth = result['Breadth']
        road_length = result['road_length']
        freq = result['freq']
        arr = result['arr']
        which_lane_to_choose(density, Breadth, road_length, freq, arr, G, R)

    elif(max(density) < maxdensity): #when all the lanes have count less than maxcount than less time will be given but the algorithm remains same
        print("In case 3")
        G = density.index(max(density))+1 #give the lane number to green signal to turn that signal green
        
        G = Find_If_Any_Lane_140(density,Breadth, road_length,freq, arr , G, R) 
        
        AllLane2 = [1,2,3,4]
        AllLane2.remove(G)
        R = AllLane2 #to turn all the other lanes red
        print(G, " ", R)
        freq_required = freq[density.index(max(density))]
        if(Breadth[G-1] <=3.75):
            lane = 1
    
        elif(Breadth[G-1] > 3.75 and Breadth[G-1] <=5.5):
            lane = 2
    
        elif(Breadth[G-1] > 5.5 and Breadth[G-1] <=7):
            lane = 2
    
        elif(Breadth[G-1] > 7 and Breadth[G-1] <=7.5):
            lane =2
        
        elif(Breadth[G-1] > 7.5 and Breadth[G-1] <=11.25):
            lane = 3
        
        elif(Breadth[G-1] > 11.25 and Breadth[G-1] <=15):
            lane = 4
        
        elif(Breadth[G-1] > 15 and Breadth[G-1] <=18.75):
            lane  =5
    
        elif(Breadth[G-1] > 18.75 and Breadth[G-1] <=22.5):
            lane = 6
        time1 = math.ceil((math.ceil(freq_required['car']/lane)*4.5+(freq_required['car']-(1*2)))/3.2)
        seconds = min(time1, 10)
        
        if(seconds <= 15):
            with open("static-data.csv", 'a',newline="") as f1:
                cwriter = csv.writer(f1)
                cwriter.writerow([ G , R , int(math.ceil(seconds/2) + 5)])
            f1.close()
        else:
            # save the data to a csv file
            with open("static-data.csv", 'a',newline="") as f1:
                cwriter = csv.writer(f1)
                cwriter.writerow([ G , R , seconds])
            f1.close()
        
        result = setting(G,R,seconds, arr)
        density = result['density']
        Breadth = result['Breadth']
        road_length = result['road_length']
        freq = result['freq']
        arr = result['arr']
        which_lane_to_choose(density, Breadth, road_length, freq, arr, G, R)
  
if __name__ == '__main__':
    AllLane = [1,2,3,4]         
    maxdensity = 50.0      #threshold
    # arr = os.listdir("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/images_for_loop/")
    arr = os.listdir("D:/Ultimate-Real-Time-Traffic-Management-System/codes/videos/images_for_loop")
    density ,Breadth, road_length, freq, arr = greatestLaneCount(arr)
    G = 1
    R = [2,3,4]
    Y = 0
    which_lane_to_choose(density, Breadth, road_length, freq, arr , G, R)