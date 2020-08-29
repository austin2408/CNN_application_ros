#! /usr/bin/env python

import rospy
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import tkinter as tk

#img = cv2.imread('/home/austin/trailnet-testing-Pytorch/2020_summer/src/deep_learning/data/Lane_data/train_data/S/S_degree_30_0236.jpg',1)
i = 0
s = None
img = cv2.imread('/home/austin/trailnet-testing-Pytorch/duckiefloat_line_follow/src/data/float_1/119.jpg')
root = tk.Tk()
s1 = tk.Scale(root, from_=0, to=255, orient="horizontal")
#s1.pack()
s2 = tk.Scale(root, from_=0, to=255, orient="horizontal")
#s2.pack()
s3 = tk.Scale(root, from_=0, to=255, orient="horizontal")
#s3.pack()
#img = cv2.imread('/home/austin/trailnet-testing-Pytorch/2020_summer/src/deep_learning/data/Lane_data/train_data/R/R_degree_30_0275.jpg',1)
while True:
    #img = cv2.imread('/home/austin/data/float_1/'+str(i)+'.jpg')
    #----------hsv_trans----------------------#
    s1.pack()
    s2.pack()
    s3.pack()
    Img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #----------detect blue line------------#
    low_red = np.array([0, 0, 0])
    up_red = np.array([s1.get(), s2.get(), s3.get()])
    Img = cv2.inRange(Img, low_red, up_red)
    Img = 255 -Img
    
    #----------optimi----------------#
    kernel = np.ones((3,3), np.uint8)
    Img = cv2.erode(Img, kernel)
    Img = cv2.dilate(Img,kernel)

    #----------find_contour-------------#
    contours, hierarchy = cv2.findContours(Img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea,reverse=True)


    #----------place box----------------------------#
    blackbox = cv2.minAreaRect(contours[0])
    (x_min, y_min), (w_min, h_min), angle = blackbox #x,y:center local w,h:weight height
    if abs((w_min)-(h_min)) < 100:
        blackbox = cv2.minAreaRect(contours[1])
        (x_min, y_min), (w_min, h_min), angle = blackbox
    box = cv2.boxPoints(blackbox)
    box = np.int0(box)
    (x1,y1), (x2,y2), (x3,y3), (x4,y4) = box
    cv2.drawContours(Img,[box],0,(125, 0, 0),3)
    d = x1 - x2
    if w_min > h_min:
        if abs(d) < 10:
            a = 0
            s = 'S'
        else:
            a = abs(angle)
            s = 'L'
    if w_min < h_min:
        if abs(d) < 10:
            a = 0
            s = 'S'
        else:
            a = abs(angle) + 90
            s = 'R'
    #print(x_min)
    #print(angle)
    print(str(x1)+'_'+str(y1))
    print(str(x2)+'_'+str(y2))
    #print(str(x3)+'_'+str(y3))
    #print(str(x4)+'_'+str(y4))
    print(s)

    #----------show--------#
    cv2.imshow('Img',Img)
    #cv2.imwrite('/home/austin/data/angle/'+s+'_'+str(a)+'_'+str(i)+'.jpg', img)
    #cv2.imwrite('/home/austin/data/center/'+str(x_min - 340)+'_'+str(i)+'.jpg', img)
    i += 1
    root.mainloop()
    #time.sleep(1)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cv2.destroyAllWindows()