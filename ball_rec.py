# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 12:26:57 2020

@author: Anna Galsanova
"""

import cv2
import numpy as np

def set_upper(x):
    global colorUpper
    colorUpper[0] = x

def set_lower(x):
    global colorLower
    colorLower[0] = x
    
def draw(cnts, frame):
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        (curr_x, curr_y), radii = cv2.minEnclosingCircle(c)
        if radii > 10:
            cv2.circle(frame, (int(curr_x), int(curr_y)), int(radii), (2, 255, 255), 2)
    
def get_cnts(hsv, colorLower, colorUpper):
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)
    
    cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return cnts

def get_coords(cnts):
    cur_x = 0
    cur_y = 0
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((cur_x, cur_y), radius) = cv2.minEnclosingCircle(c)
    return cur_x
    
cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
# cv2.namedWindow("Mask", cv2.WINDOW_KEEPRATIO)

# cv2.createTrackbar("U", 'Mask', 0, 255, set_upper)
# cv2.createTrackbar("L", 'Mask', 0, 255, set_lower)

# colorLower = np.array([0, 100, 100], dtype = "uint8")
# colorUpper = np.array([255, 255, 255], dtype = "uint8")

while cam.isOpened():
    ret, frame = cam.read()
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    #it barely works for blue, yellow and green balls
    
    cnts_blue = get_cnts(hsv, np.array([95,100,100]), np.array([110,255,255]))
    draw(cnts_blue, frame)
    
    cnts_yellow = get_cnts(hsv, np.array([13,100,100]), np.array([30,255,255]))
    draw(cnts_yellow, frame)
    
    cnts_green = get_cnts(hsv, np.array([64,100,100]), np.array([86,255,255]))
    draw(cnts_green, frame)
    
    #it can work better but I don't know how
    
    if (get_coords(cnts_blue) > get_coords(cnts_yellow)):
        if (get_coords(cnts_yellow) > get_coords(cnts_green)):
            cv2.putText(frame, "blue, yellow, green", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
        else:
            cv2.putText(frame, "blue, green, yellow", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
    
    elif (get_coords(cnts_yellow) > get_coords(cnts_blue)):
        if (get_coords(cnts_blue) > get_coords(cnts_green)):
            cv2.putText(frame, "yellow, blue, green", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
        else:
            cv2.putText(frame, "yellow, green, blue", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
            
    elif (get_coords(cnts_green) > get_coords(cnts_blue)):
        if (get_coords(cnts_blue) > get_coords(cnts_yellow)):
            cv2.putText(frame, "green, blue, yellow", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
        else:
            cv2.putText(frame, "green, yellow, blue", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
    
    # cv2.putText(frame, f"{get_coords(cnts_blue)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
    
    # cv2.imshow("Mask", mask)
    cv2.imshow("Camera", frame)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()