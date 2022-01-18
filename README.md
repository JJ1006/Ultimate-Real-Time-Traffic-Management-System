#Ultimate-Real-Time-Traffic-Management-System
Research on Traffic Management System on real time basis.

<h1> References </h1>
<h3> https://www.analyticsvidhya.com/blog/2020/04/vehicle-detection-opencv-python/ </h3>
<h3> https://rsdharra.com/blog/lesson/26.html from where cars.mp4 and cars.xml copied </h3>
<h3> https://www.cityofirvine.org/signal-operations-maintenance/traffic-signal-synchronization </h3>
<h3> https://gadgetstouse.com/blog/2021/10/17/types-of-traffic-cameras-e-challan-in-india/ </h3>
<h3> https://timesofindia.indiatimes.com/city/chandigarh/smart-cameras-to-manage-traffic-enforce-rules/articleshow/81130901.cms </h3>


<h1> To do </h1>
<p> 1. Image processing in opencv and count the vehicles </p>
<p> 2. Understand all the four lanes and built a program that can easily let all the vehicles on more crowded side to release first</p>
<p> 3. Cameras available on the traffic signal and the range of the such cameras to set the threshold of maximum cars. </p>
<p> 4. Study the average length of cars to understand how much range of camera we need to have threshold number of cars in the single line i.e camera range ~ directly proportional to length of cars. </p>
<p> 5. Calculate the breadth of road to set the threshold value </p>

<h1> IMPS </h1>
<p>1. We need to install cameras on the sides of road to get a clear image of vechiles on road and to be able to identify vehicles distinctly to get an accurate count of vehicles on the road.</p>
<p><span>2. Algorithm for RGY :
  add one switch loop here for different breadths of road to have different threshold values for each kind of roads.
  <h2>i)check all cases</h2>
  <span>a)if(no. of vehicles > 15(threshold):
       for 30 sec:
          green light = on
  b)check again 
    if same lane in a) then repeat+1 a) untill repeat <2  <h1> [issue here is if the signal is green then vehciles must be moving in that region than image of what time will be considered as all the vehicles must be moving in that lane .. so how to consider or count the vehicles in that lane]</h1>
    if repeat >3 break and consider other three sides for a)
  c)give priority to the first lane having more than threshold count of vehicles and allot the green light to lanes in this priority
  </span>
    
  <h2>ii)if any side has been opened uptill</h2>
   <span>a)if any side not opened for 100 seconds then open it for( max(no. of vehicles,30sec) seconds) means maximum of the two in the brackets would be chosen , this would save the time if no. of vehciles is less than 30. [assuming one vehicle takes 1 sec to cross the crossing].
   </span>
  <h2>iii)if number of vehicles <15 (threshold) on everyside than clockwise green on each side for 30sec green .
</span>
</p>

