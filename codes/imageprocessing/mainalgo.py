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

def greatestLaneCount(arr): #this function is used to find the greatest lane count in the last 10 seconds
    if(len(arr) ==0 ): #if there is no data in the last 10 seconds
        arr = os.listdir("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/images_for_loop/")
        # arr = os.listdir("D:/Ultimate-Real-Time-Traffic-Management-System/codes/videos/images_for_loop/")
    
    path = "C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/images_for_loop/"
    # path = "D:/Ultimate-Real-Time-Traffic-Management-System/codes/videos/images_for_loop/" #path to the folder where images are stored
    
    freq1 = vehicle_count.from_static_image(path  + arr[0]) #reading the first image in the folder
    # freq1 = vehicle_count.from_static_image("D:/Ultimate-Real-Time-Traffic-Management-System/codes/videos/testing.jpg")
    sum1 = freq1['car'] + freq1['motorbike'] + freq1['bus'] + freq1['truck'] #sum of all the vehicles in the first image
    miny1 = freq1['miny'] # minimum y value of the first image
    maxy1 = freq1['maxy'] # maximum y value of the first image
    VA1 = freq1['vehicle_area'] #vehicle area of the first image
    B1 = freq1['breadth'] #breadth of the first image
    road_length1 = freq1['height'] #road length of the first image
    density1 = float (VA1/ (B1 * road_length1)) * 100.0 #density of the first image

    freq2 = vehicle_count.from_static_image(path  + arr[1]) #reading the second image in the folder
    # freq2 = vehicle_count.from_static_image("D:/Ultimate-Real-Time-Traffic-Management-System/codes/videos/testing.jpg")
    sum2 = freq2['car'] + freq2['motorbike'] + freq2['bus'] + freq2['truck']#sum of all the vehicles in the second image
    miny2 = freq2['miny'] # minimum y value of the second image
    maxy2 = freq2['maxy'] # maximum y value of the second image
    VA2 = freq2['vehicle_area'] #vehicle area of the second image
    B2 = freq2['breadth'] #breadth of the second image
    road_length2 = freq2['height'] #road length of the second image
    density2 = float (VA2/ (B2 * road_length2)) * 100.0 #density of the second image

    freq3 = vehicle_count.from_static_image(path  + arr[2]) #reading the third image in the folder
    # freq3 = vehicle_count.from_static_image("D:/Ultimate-Real-Time-Traffic-Management-System/codes/videos/testing.jpg")
    sum3 = freq3['car'] + freq3['motorbike'] + freq3['bus'] + freq3['truck'] #sum of all the vehicles in the third image
    miny3 = freq3['miny'] # minimum y value of the third image
    maxy3 = freq3['maxy'] # maximum y value of the third image
    VA3 = freq3['vehicle_area'] #vehicle area of the third image
    B3 = freq3['breadth'] #breadth of the third image
    road_length3 = freq3['height'] #road length of the third image
    density3 = float (VA3/ (B3 * road_length3)) * 100.0 #density of the third image

    freq4 = vehicle_count.from_static_image(path  + arr[3]) #reading the fourth image in the folder
    # freq4 = vehicle_count.from_static_image("D:/Ultimate-Real-Time-Traffic-Management-System/codes/videos/testing.jpg")
    sum4 = freq4['car'] + freq4['motorbike'] + freq4['bus'] + freq4['truck'] #sum of all the vehicles in the fourth image
    miny4 = freq4['miny'] # minimum y value of the fourth image
    maxy4 = freq4['maxy'] # maximum y value of the fourth image
    VA4 = freq4['vehicle_area'] #vehicle area of the fourth image
    B4 = freq4['breadth'] #breadth of the fourth image
    road_length4 = freq4['height'] #road length of the fourth image
    density4 = float (VA4/ (B4 * road_length4)) * 100.0 #density of the fourth image
    
    one = arr[0] #first image in the folder
    two = arr[1] #second image in the folder
    three = arr[2] #third image in the folder
    four = arr[3] #fourth image in the folder
    arr.remove(one) #removing the first image from the folder
    arr.remove(two)  #removing the second image from the folder
    arr.remove(three) #removing the third image from the folder
    arr.remove(four) #removing the fourth image from the folder
    Breadth = [B1, B2, B3, B4] #list of breadth of the images
    freq = [freq1, freq2, freq3, freq4] #list of vehicle counts of the images
    road_length = [road_length1,road_length2, road_length3, road_length4] #list of road length of the images
    density = [density1, density2, density3, density4] #list of density of the images
    print(density) #printing the density of the images
    return density, Breadth, road_length,freq,arr #returning the density, breadth, road length and vehicle counts of the images


def yellow(G, R, s): #this function is used to find the yellow lane
    print("t4 yellow started") #printing the message
    Y = G #green lane becomes yellow for 10 sec and then it becomes green again
    if(s <= 15): #if the time is less than 15 sec
        time.sleep(5) #sleep for 5 sec
    else: #if the time is greater than 15 sec
        time.sleep(10)  #sleep for 10 sec
    R.append(Y) #now after 10 sec yellow is turned to red 
    print("t4 yellow ended") #printing the message
   
def green(G, s): #this function is used to find the green lane
    print("t1 green started") #printing the message
    G = G #green lane remains green for 10 sec
    time.sleep(s) #sleep for the time of the video
    print("t1 green ended") #printing the message

def Red(R, s): #this function is used to find the red lane
    print("t2 red started") #printing the message
    R = R #red lane remains red for 10 sec
    time.sleep(s) #sleep for the time of the video
    print("t2 red ended") #printing the message

def find_next_green_Lane(density5): #make sure this thread takes less than 10 sec so that we are ready with next green lane number before the yellow turns into red
    print("t5 greenlanefind started") #printing the message
    
    density, Breadth5, road_length5 , freq, arr = greatestLaneCount(density5['arr']) #finding the greatest lane count
    density5['density'] = density #density of the lane
    density5['Breadth'] = Breadth5 #breadth of the lane
    density5['road_length'] = road_length5 #road length of the lane
    density5['freq'] = freq #vehicle counts of the lane
    density5['arr'] = arr #images of the lane
    return density5  #returning the density, breadth, road length and vehicle counts of the lane
    
    

def setting(G,R,s, arr): #this function is used to find the green lane
    if(s <= 15): #if the time is less than 15 sec
        t1= threading.Thread(target=green, args= (G, math.ceil(s/2))) #thread for green lane
    else: #if the time is greater than 15 sec
        t1= threading.Thread(target=green, args= (G, s-10)) #thread for green lane
    t2= threading.Thread(target=Red, args= (R, s)) #thread for red lane
    t1.start() #starting the thread
    t2.start() #starting the thread
    t4 = threading.Thread(target=yellow, args = (G,R,s))  #starting yellow for 10sec
    density5={'arr' : arr} #creating a dictionary
    t5 = threading.Thread(target=lambda q, arg1: q.put(find_next_green_Lane(density5)), args=(que,density5))  #starting the thread for finding the next green lane
    t5.start() #starting the thread
    t5.join() #joining the thread
    print("t5 ended") #printing the message
    t1.join() #to make sure that t1 i.e green thread has completed
    t4.start() #starting the thread
    t2.join() #to make sure that t2 i.e red thread has completed
    t4.join() #to make sure that t4 i.e yellow thread has completed
    result = que.get()  #getting the result from the queue
    
    return result #returning the result


def newG(G): #this function is used to find the green lane
    Index = [0,0,0,0] #for row indexes of last occurences of 1,2,3,4
    one,two,three,four = True,True,True,True #for checking the occurence of 1,2,3,4
    time_count = [0,0,0,0] #for counting the time of 1,2,3,4
    df = pd.read_csv("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/static-data.csv",header=None)
    # df = pd.read_csv("D:/Ultimate-Real-Time-Traffic-Management-System/static-data.csv",header=None) #reading the static data
    df1 = pd.DataFrame(df,index=None)  #converting the dataframe to dataframe
    csvfile = df1.to_numpy().tolist()  #converting the dataframe to numpy array
    # print(csvfile) 
    j = len(csvfile)-1 #for the last row
    for a in csvfile[-1::-1]: #for the last row
        print(a, " a") #printing the last row
        if(a[0] == 1 and one is True and j>0): #if the first column is 1 and the one is true
            Index[0] = csvfile.index(a) #index of the row
            j=j-1 #decrementing the j
            one = False #one is false
        if(a[0] == 2 and two is True and j>0): #if the first column is 2 and the two is true
            Index[1] = csvfile.index(a) #index of the row
            j=j-1 #decrementing the j
            two = False #two is false
        if(a[0] == 3 and three is True and j>0): #if the first column is 3 and the three is true
            Index[2] = csvfile.index(a) #index of the row
            j=j-1 #decrementing the j
            three = False #three is false
        if(a[0] == 4 and four is True and j>0): #if the first column is 4 and the four is true
            Index[3] = csvfile.index(a) #index of the row
            j=j-1 #decrementing the j
            four = False #four is false
        if(j==0 or ((one is False) and (two is False) and (three is False) and (four is False))): #if j is 0 or all the lanes are false
            break #break the loop
                
    print(Index,"index check")  #printing the index
    consider = [0,1,2,3] #for considering the lanes
    rowlast = csvfile[-1] #for the last row
    consider.remove(rowlast[0]-1) #removing the lane which is not present
    for i in consider: #for considering the lanes
        print([x[2] for x in csvfile[Index[i]+1 : len(csvfile)] ]) #printing the row
        time_count[i]= sum([x[2] for x in csvfile[Index[i]+1 : len(csvfile)] ]) #sum of all the time_counts of the lanes
    maxcount = max(time_count) #max time_count of the lanes
    if(maxcount>=140): #if maxcount is greater than 140 then we have to consider all the lanes
        G = time_count.index(maxcount)+1 #lane number
        print(G, " G changed for 140") #lane number
    return G    
        
def Find_If_Any_Lane_140(density,Breadth, road_length,freq, arr , G, R): #this function is used to find the green lane
    with open('static-data.csv', 'r',newline="") as read_obj:  #if max density comes of same lane then don't consider that lane and check again for rest of the lanes
        print(" in case 1 int type G code") #printing the message
        csv_reader = csv.reader(read_obj) #reading the csv file
        row1 = list(csv_reader)[-1] #last row
        
        print("in") #printing the message
        if(G == int(row1[0])): #if the green lane is same as the last lane
            print("Same G as previous lane so ignoring this G and changing") #printing the message
            print(density) #printing the density
            density[G-1] = 0 #setting the density of the lane to 0
            print(density) #printing the density
            which_lane_to_choose(density,Breadth, road_length,freq, arr , G, R) #calling the function which_lane_to_choose
        G = newG(G) #calling the function newG
        
    return G #returning the green lane

#assuming side 1 has red ,side 2 has green, side 3 has red, side 4 has red as an initial case
   
def which_lane_to_choose(density,Breadth, road_length, freq, arr,G, R): #this function is used to find the green lane
    if(max(density) >= maxdensity): #case1 when max number of vehicles is greater than maxcount 
        print("In case 1") #printing the message
        G = density.index(max(density))+1 #give the lane number to green signal to turn that signal green   
        G = Find_If_Any_Lane_140(density,Breadth, road_length,freq, arr , G, R) #calling the function Find_If_Any_Lane_140
        AllLane2 = [1,2,3,4] #all the lanes
        AllLane2.remove(G) #removing the green lane
        R = AllLane2 #to turn all the other lanes red      
        print(G, " ", R) #printing the green lane and red lanes
        seconds = (road_length[G-1]/3.2) + 5 #calculating the time for green signal
        
        # save the data to a csv file
        with open("static-data.csv", 'a', newline="") as f1: #appending the data to the csv file
            cwriter = csv.writer(f1) #writing the data to the csv file
            cwriter.writerow([ G , R , seconds]) #writing the data to the csv file
        f1.close() #closing the csv file
        
        result = setting(G,R,seconds, arr) #calling the function setting
        density = result['density'] #density
        Breadth = result['Breadth'] #Breadth
        road_length = result['road_length'] #road_length
        freq = result['freq'] #freq
        arr = result['arr'] #arr
        which_lane_to_choose(density,Breadth, road_length,freq, arr , G, R) #calling the function which_lane_to_choose

    if(max(density) < 7.0): #clockwise case
        print("In case 2") #printing the message
        G = density.index(max(density))+1 #give the lane number to green signal to turn that signal green
        G = Find_If_Any_Lane_140(density,Breadth, road_length,freq, arr , G, R) #calling the function Find_If_Any_Lane_140
                
        AllLane2 = [1,2,3,4] #all the lanes
        AllLane2.remove(G) #removing the green lane
        R = AllLane2 #to turn all the other lanes red
        print(G, " ", R) #printing the green lane and red lanes
        seconds = 5 #calculating the time for green signal
         
        # save the data to a csv file
        with open("static-data.csv", 'a',newline="") as f1: #appending the data to the csv file
            cwriter = csv.writer(f1) #writing the data to the csv file
            cwriter.writerow([ G , R , int(math.ceil(seconds/2) + 5)]) #writing the data to the csv file
        f1.close() #closing the csv file
    
        
        result = setting(G,R,seconds, arr) #calling the function setting
        density = result['density'] #density
        Breadth = result['Breadth'] #Breadth
        road_length = result['road_length'] #road_length
        freq = result['freq'] #freq
        arr = result['arr'] #arr
        which_lane_to_choose(density, Breadth, road_length, freq, arr, G, R) #calling the function which_lane_to_choose

    elif(max(density) < maxdensity): #when all the lanes have count less than maxcount than less time will be given but the algorithm remains same
        print("In case 3") #printing the message
        G = density.index(max(density))+1 #give the lane number to green signal to turn that signal green
        
        G = Find_If_Any_Lane_140(density,Breadth, road_length,freq, arr , G, R) #calling the function Find_If_Any_Lane_140
        
        AllLane2 = [1,2,3,4] #all the lanes
        AllLane2.remove(G) #removing the green lane
        R = AllLane2 #to turn all the other lanes red
        print(G, " ", R) #printing the green lane and red lanes
        freq_required = freq[density.index(max(density))] #frequency required for the lane with max density
        if(Breadth[G-1] <=3.75): #if the breadth of the lane is less than 3.75
            lane = 1 #lane 1
    
        elif(Breadth[G-1] > 3.75 and Breadth[G-1] <=5.5): #if the breadth of the lane is greater than 3.75 and less than 5.5
            lane = 2 #lane 2
    
        elif(Breadth[G-1] > 5.5 and Breadth[G-1] <=7): #if the breadth of the lane is greater than 5.5 and less than 7
            lane = 2 #lane 2
    
        elif(Breadth[G-1] > 7 and Breadth[G-1] <=7.5): #if the breadth of the lane is greater than 7 and less than 7.5
            lane =2 #lane 2
        
        elif(Breadth[G-1] > 7.5 and Breadth[G-1] <=11.25): #if the breadth of the lane is greater than 7.5 and less than 11.25
            lane = 3 #lane 3
        
        elif(Breadth[G-1] > 11.25 and Breadth[G-1] <=15): #if the breadth of the lane is greater than 11.25 and less than 15
            lane = 4 #lane 4
        
        elif(Breadth[G-1] > 15 and Breadth[G-1] <=18.75): #if the breadth of the lane is greater than 15 and less than 18.75
            lane  =5 #lane 5
    
        elif(Breadth[G-1] > 18.75 and Breadth[G-1] <=22.5): #if the breadth of the lane is greater than 18.75 and less than 22.5
            lane = 6 #lane 6
        time1 = math.ceil((math.ceil(freq_required['car']/lane)*4.5+(freq_required['car']-(1*2)))/3.2) #calculating the time for green signal
        seconds = min(time1, 10) #calculating the time for green signal
        
        if(seconds <= 15): #if the time is less than 15
            with open("static-data.csv", 'a',newline="") as f1: #appending the data to the csv file
                cwriter = csv.writer(f1) #writing the data to the csv file
                cwriter.writerow([ G , R , int(math.ceil(seconds/2) + 5)])  #writing the data to the csv file
            f1.close() #closing the csv file
        else: #if the time is greater than 15
            # save the data to a csv file
            with open("static-data.csv", 'a',newline="") as f1: #appending the data to the csv file
                cwriter = csv.writer(f1) #writing the data to the csv file
                cwriter.writerow([ G , R , seconds]) #writing the data to the csv file
            f1.close() #closing the csv file
        
        result = setting(G,R,seconds, arr) #calling the function setting
        density = result['density'] #density
        Breadth = result['Breadth'] #Breadth
        road_length = result['road_length'] #road_length
        freq = result['freq'] #freq
        arr = result['arr'] #arr
        which_lane_to_choose(density, Breadth, road_length, freq, arr, G, R) #calling the function which_lane_to_choose
  
if __name__ == '__main__': #main function
    AllLane = [1,2,3,4]  #all the lanes
    maxdensity = 50.0      #threshold
    arr = os.listdir("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/images_for_loop/")
    # arr = os.listdir("D:/Ultimate-Real-Time-Traffic-Management-System/codes/videos/images_for_loop") #list of all the images
    density ,Breadth, road_length, freq, arr = greatestLaneCount(arr) #calling the function greatestLaneCount
    G = 1 #green lane
    R = [2,3,4] #red lanes
    Y = 0 #yellow lane
    which_lane_to_choose(density, Breadth, road_length, freq, arr , G, R) #calling the function which_lane_to_choose