import threading
import vehicle_count
import time
import queue

que = queue.Queue()

def greatestLaneCount():
    freq1 = vehicle_count.from_static_image("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/example2.jpg")
    sum1 = freq1['car'] + freq1['motorbike'] + freq1['bus'] + freq1['truck']
    miny1 = freq1['miny']
    maxy1 = freq1['maxy']
    VA1 = freq1['vehicle_area']
    B1 = freq1['breadth']
    if(miny1 < 20):
        miny1=20
    height1 = maxy1 - miny1
    density1 = float (VA1/ (B1 * height1))

    freq2 = vehicle_count.from_static_image("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/traffic-1.jpg")
    sum2 = freq2['car'] + freq2['motorbike'] + freq2['bus'] + freq2['truck']
    miny2 = freq2['miny']
    maxy2 = freq2['maxy']
    VA2 = freq2['vehicle_area']
    B2 = freq2['breadth']
    if(miny2 < 20):
        miny2=20
    height2 = maxy2 - miny2
    density2 = float(VA2/ (B2 * height2))

    freq3 = vehicle_count.from_static_image("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/traffic-2.jpg")
    sum3 = freq3['car'] + freq3['motorbike'] + freq3['bus'] + freq3['truck']
    miny3 = freq3['miny']
    maxy3 = freq3['maxy']
    VA3 = freq3['vehicle_area']
    B3 = freq3['breadth']
    if(miny3 < 20):
        miny3=20
    height3 = maxy3 - miny3
    density3 = float(VA3/(B3 * height3))

    freq4 = vehicle_count.from_static_image("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/traffic-3.jpg")
    sum4 = freq4['car'] + freq4['motorbike'] + freq4['bus'] + freq4['truck']
    miny4 = freq4['miny']
    maxy4 = freq4['maxy']
    VA4 = freq4['vehicle_area']
    B4 = freq4['breadth']
    if(miny4 < 20):
        miny4=20
    height4 = maxy4 - miny4
    density4 = float( VA4 /(B4 * height4))
    
    

    density = [density1, density2, density3, density4]
    print(density)
    return density


def yellow(G, R):
    print("t4 yellow started")
    print("G",G)
    print("R",R)
    Y = G #green lane becomes yellow for 10 sec
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
    density5 = greatestLaneCount()
    return density5
    
    

def setting(G,R,s):
    t1= threading.Thread(target=green, args= (G, s-10))
    t2= threading.Thread(target=Red, args= (R, s))
    t1.start()
    t2.start()
    t4 = threading.Thread(target=yellow, args = (G,R))  #starting yellow for 10sec
    density5=[]
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


#assuming side 1 has red ,side 2 has green, side 3 has red, side 4 has red as an initial case
   
def which_lane_to_choose(density,G, R):
    if(max(density) >= maxdensity): #case1 when max number of vehicles is greater than maxcount 
        print("In case 1")
        G = density.index(max(density))+1 #give the lane number to green signal to turn that signal green
        AllLane2 = [1,2,3,4]
        AllLane2.remove(G)
        R = AllLane2 #to turn all the other lanes red
        seconds = 60
        density = setting(G,R,seconds)
        which_lane_to_choose(density , G, R)

    if(max(density) <= 15): #clockwise
        print("In case 2")
        G = G+1
        AllLane2 = [1,2,3,4]
        R = AllLane2.remove(G)
        seconds = 15
        density = setting(G,R,seconds)
        which_lane_to_choose(density, G, R)

    if(max(density) < density): #when all the lanes have count less than maxcount than less time will be given but the algorithm remains same
        print("In case 3")
        G = density.index(max(density))+1 #give the lane number to green signal to turn that signal green
        AllLane2 = [1,2,3,4]
        AllLane2.remove(G)
        R = AllLane2 #to turn all the other lanes red
        seconds = min(max(density), 29)
        density = setting(G,R,seconds)
        which_lane_to_choose(density, G, R)
  
if __name__ == '__main__':
    AllLane = [1,2,3,4]         
    maxdensity = 0.70      #threshold
    density = greatestLaneCount()
    print(density)
    G = 1
    R = [2,3,4]
    Y = 0
    print(G)
    print(R)
    which_lane_to_choose(density , G, R)
