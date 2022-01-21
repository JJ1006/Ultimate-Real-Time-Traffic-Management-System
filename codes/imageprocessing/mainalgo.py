import threading
import vehicle_count
import time

def greatestLaneCount():
    freq1 = vehicle_count.from_static_image("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/example2.jpg")
    sum1 = freq1['Car'] + freq1['motorbike'] + freq1['bus'] + freq1['truck']

    freq2 = vehicle_count.from_static_image("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/example2.jpg")
    sum2 = freq2['Car'] + freq2['motorbike'] + freq2['bus'] + freq2['truck']

    freq3 = vehicle_count.from_static_image("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/example2.jpg")
    sum3 = freq3['Car'] + freq3['motorbike'] + freq3['bus'] + freq3['truck']

    freq4 = vehicle_count.from_static_image("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/example2.jpg")
    sum4 = freq4['Car'] + freq4['motorbike'] + freq4['bus'] + freq4['truck']

    sum = [sum1,sum2,sum3,sum4]
    return sum


def yellow(G, R):
    Y = G #green lane becomes yellow for 10 sec
    threading.Thread.sleep(10000) 
    R.append(Y) #now after 10 sec yellow is turned to red 
   
def green(G, s):
    G = G
    threading.Thread.sleep(s)

def Red(R, s):
    R = R
    threading.Thread.sleep(s)

def find_next_green_Lane(sum1): #make sure this thread takes less than 10 sec so that we are ready with next green lane number before the yellow turns into red
    sum1 = greatestLaneCount()
    
    

def setting(G,R,s):
    t_end = time.time() + s-10 #saving 10seconds for yellow warning period
    t1= threading.Thread(target=green, args= (G, t_end))
    t2= threading.Thread(target=Red, args= (R, t_end +10))
    t1.start()
    t2.start()
    t_end_yellow = time.time() + 10
    t4 = threading.Thread(target=yellow, args = (G,R))  #starting yellow for 10sec
    sum1 = []   #to get the list from find_next_green_Lane thread
    t5 = threading.Thread(target=find_next_green_Lane, args = (sum1,)) 
    t1.join() #to make sure that t1 i.e green thread has completed
    t4.start()
    t5.start()  
    return sum1


#assuming side 1 has red ,side 2 has green, side 3 has red, side 4 has red as an initial case
 
def which_lane_to_choose(sum):
    if(max(sum) >= maxcount): #case1 when max number of vehicles is greater than maxcount 
        G = sum.index(max(sum))+1 #give the lane number to green signal to turn that signal green
        AllLane2 = AllLane[:]
        AllLane2.remove(G)
        R = AllLane2 #to turn all the other lanes red
        seconds = 60
        sum = setting(G,R,seconds)
        which_lane_to_choose(sum)

    if(max(sum) <= 15): #clockwise
        G = G+1
        AllLane2 = AllLane[:]
        R = AllLane2.remove(G)
        seconds = 15
        sum = setting(G,R,seconds)
        which_lane_to_choose(sum)

    if(max(sum) < maxcount): #when all the lanes have count less than maxcount than less time will be given but the algorithm remains same
        G = sum.index(max(sum))+1 #give the lane number to green signal to turn that signal green
        AllLane2 = AllLane[:]
        AllLane2.remove(G)
        R = AllLane2 #to turn all the other lanes red
        seconds = min(max(sum), 29)
        sum = setting(G,R,seconds)
        which_lane_to_choose(sum)
  
if __name__ == '__main__':
    global AllLane
    AllLane = [1,2,3,4]         
    global maxcount 
    maxcount = 30         #threshold
    sum = greatestLaneCount()
    #assumption
    global G, R, Y
    G = 1
    R = [2,3,4]
    Y = 0
    which_lane_to_choose(sum)