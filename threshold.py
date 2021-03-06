from collections import deque
import cv2
import numpy as np
import RangeConfig

cam_index=int(raw_input("Enter Camera Index : "))
cap = cv2.VideoCapture(cam_index)

def persist_values(x):
    config.set_low_range(h1, s1, v1)
    config.set_high_range(h2, s2, v2)

config = RangeConfig.RangeConfig("./config.ini")
h1 = config.lowRange[0]
s1 = config.lowRange[1]
v1 = config.lowRange[2]

h2 = config.highRange[0]
s2 = config.highRange[1]
v2 = config.highRange[2]

cv2.namedWindow('image',flags=cv2.WINDOW_NORMAL)
# create trackbars for color change
cv2.createTrackbar('h1','image', h1, 255, persist_values)
cv2.createTrackbar('s1','image', s1, 255, persist_values)
cv2.createTrackbar('v1','image', v1, 255, persist_values)

cv2.createTrackbar('h2','image', h2, 255, persist_values)
cv2.createTrackbar('s2','image', s2, 255, persist_values)
cv2.createTrackbar('v2','image', v2, 255, persist_values)

pts = deque(maxlen=64)

while(1):
  _, frame = cap.read()
  frame=cv2.resize(frame,(300,280))
  frame=cv2.medianBlur(frame, 5)
  # Convert BGR to HSV
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  h1 = cv2.getTrackbarPos('h1','image')
  s1 = cv2.getTrackbarPos('s1','image')
  v1 = cv2.getTrackbarPos('v1','image')

  h2 = cv2.getTrackbarPos('h2','image')
  s2 = cv2.getTrackbarPos('s2','image')
  v2 = cv2.getTrackbarPos('v2','image')

  lower= np.array([h1,s1,v1])
  upper = np.array([h2,s2,v2])
  # Threshold the HSV image to get only blue colors
  mask = cv2.inRange(hsv, lower, upper)
  cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
  center = None

  # only proceed if at least one contour was found
  if len(cnts) > 0:
    # find the largest contour in the mask, then use
    # it to compute the minimum enclosing circle and
    # centroid
    c = max(cnts, key=cv2.contourArea)
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    if M["m00"] != 0:
      center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

      # only proceed if the radius meets a minimum size
      if radius > 10:
      #  # draw the circle and centroid on the frame,
      #  # then update the list of tracked points
      #  cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)
      # update the points queue
      pts.appendleft(center)


  cv2.imshow('frame',frame)
  cv2.imshow('thresh',mask)

  k = cv2.waitKey(5) & 0xFF
  if k == 27:
    break

cv2.destroyAllWindows()
