import matplotlib.pylab as plt
import cv2
import numpy as np

def region_of_interest(img,vertices): 
    mask = np.zeros_like(img) 
    channel_count=img.shape[:2]         
    match_mask_color=  255   #(255,) * channel_count
    cv2.fillPoly(mask,vertices,match_mask_color)
    masked_image=cv2.bitwise_and(img,mask) 
    return masked_image

def draw_the_lines(img,lines): 
  imge=np.copy(img)     
  blank_image=np.zeros((imge.shape[0],imge.shape[1],3),dtype=np.uint8)
  for line in lines:  
    for x1,y1,x2,y2 in line:
      cv2.line(blank_image,(x1,y1),(x2,y2),(0,255,0),thickness=3)
      imge = cv2.addWeighted(imge,0.8,blank_image,1,0.0) 
  return imge


# Step1: Read the image and convert it to RGB format. Get its height and width and define a region of interest which is required for the Lane Detection.
image=cv2.imread("C:/Users/Deepak/Documents/GitHub/Ultimate-Real-Time-Traffic-Management-System/codes/videos/road1.jpg")
image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
cv2.imshow("image",image)
cv2.waitKey(0)
height=image.shape[0]
width=image.shape[1]
region_of_interest_coor=[(0,height),(0,400),(width/2,height/3),(width,height)]

# Step2: Convert the image to GRAY format and pass the image to Canny.
gray_image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
cv2.imshow("image",gray_image)
cv2.waitKey(0)
canny_image = cv2.Canny(gray_image,100,200)

# Step3: Now, mask the canny image by the region of interest defined earlier.
cropped=region_of_interest(canny_image,np.array([region_of_interest_coor],np.int32))

# Step4: Apply Probabilistic Hough Line Transform to the masked canny image.
lines = cv2.HoughLinesP(cropped,rho=1,theta=np.pi/120,threshold=120,lines=np.array([]),minLineLength=300,maxLineGap=50)

# Step5: Draw the lines by draw_the_lines() defined earlier, by using ‘lines’ returned by the HoughLinesP() and plot the resultant image.
image_with_lines = draw_the_lines(image,lines) 
cv2.imshow("image",image_with_lines)
cv2.waitKey(0)
