import threading
import vehicle_count
import time
import queue

que = queue.Queue()

def greatestLaneCount():
    freq1 = vehicle_count.from_static_image("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/example2.jpg")
    sum1 = freq1['car'] + freq1['motorbike'] + freq1['bus'] + freq1['truck']

    freq2 = vehicle_count.from_static_image("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/traffic-1.jpg")
    sum2 = freq2['car'] + freq2['motorbike'] + freq2['bus'] + freq2['truck']

    freq3 = vehicle_count.from_static_image("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/traffic-2.jpg")
    sum3 = freq3['car'] + freq3['motorbike'] + freq3['bus'] + freq3['truck']

    freq4 = vehicle_count.from_static_image("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/traffic-3.jpg")
    sum4 = freq4['car'] + freq4['motorbike'] + freq4['bus'] + freq4['truck']

    sum = [sum1,sum2,sum3,sum4]
    print(sum)
    return sum


def yellow(G, R):
    print(G)
    print(R)
    Y = G #green lane becomes yellow for 10 sec
    time.sleep(10) 
    R.append(Y) #now after 10 sec yellow is turned to red 
   
def green(G, s):
    G = G
    time.sleep(s)

def Red(R, s):
    R = R
    time.sleep(s)

def find_next_green_Lane(sum1): #make sure this thread takes less than 10 sec so that we are ready with next green lane number before the yellow turns into red
    sum1 = greatestLaneCount()
    return sum1
    
    

def setting(G,R,s):
    t1= threading.Thread(target=green, args= (G, s-10))
    t2= threading.Thread(target=Red, args= (R, s))
    t1.start()
    t2.start()
    t4 = threading.Thread(target=yellow, args = (G,R))  #starting yellow for 10sec
    sum1=[]
    t5 = threading.Thread(target=lambda q, arg1: q.put(find_next_green_Lane(sum1)), args=(que,sum1)) 
    t5.start()
    t5.join()
    t1.join() #to make sure that t1 i.e green thread has completed
    t4.start()
    t2.join()
    t4.join()
    result = que.get() 
    return result


#assuming side 1 has red ,side 2 has green, side 3 has red, side 4 has red as an initial case
 
def which_lane_to_choose(su,G, R):
    print(su)
    if(max(su) >= maxcount): #case1 when max number of vehicles is greater than maxcount 
        G = su.index(max(su))+1 #give the lane number to green signal to turn that signal green
        AllLane2 = [1,2,3,4]
        AllLane2.remove(G)
        R = AllLane2 #to turn all the other lanes red
        seconds = 60
        su = setting(G,R,seconds)
        which_lane_to_choose(su , G, R)

    if(max(su) <= 15): #clockwise
        G = G+1
        AllLane2 = [1,2,3,4]
        R = AllLane2.remove(G)
        seconds = 15
        su = setting(G,R,seconds)
        which_lane_to_choose(su, G, R)

    if(max(su) < maxcount): #when all the lanes have count less than maxcount than less time will be given but the algorithm remains same
        G = su.index(max(su))+1 #give the lane number to green signal to turn that signal green
        AllLane2 = [1,2,3,4]
        AllLane2.remove(G)
        R = AllLane2 #to turn all the other lanes red
        seconds = min(max(su), 29)
        su = setting(G,R,seconds)
        which_lane_to_choose(su, G, R)
  
if __name__ == '__main__':
    AllLane = [1,2,3,4]         
    maxcount = 30         #threshold
    sum = greatestLaneCount()
    print(sum)
    G = 1
    R = [2,3,4]
    Y = 0
    print(G)
    print(R)
    which_lane_to_choose(sum , G, R)
