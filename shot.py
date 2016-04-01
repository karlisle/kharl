#!/usr/bin/python
##############################
# Author: HackerAzteca       #
# Licence: Creative Common   #
# Web: hackerazteca.org      #
# Share&Help                 #
##############################
import numpy as np
import argparse
import imutils
import glob
import cv2

class Vision:
    def __init__(self):
        print("Hola mundo")
        pass

    def getFrame(self):
        print("\n\t**** Bienvenido al detector de piel **** \n ")
        print("\tIniciado dispositivo de captura.....")

        devcap = cv2.VideoCapture(0)

        while True:
            (grabbed, frame) = devcap.read()

            self.preProsses(frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
                pass
        devcap.release()
        pass




    def preProsses(self, frame):

        resized = imutils.resize(frame, width=300)
        ratio = frame.shape[0] / float(resized.shape[0])
        print(ratio)

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurresd = cv2.GaussianBlur(gray_frame, (5,5), 0)
        #bilateral = cv2.bilateralFilter(gray_frame, 9, 90, 90)
        thresh = cv2.threshold(blurresd, 70, 255, cv2.THRESH_BINARY)[1]
        #canny  = cv2.Canny(blurresd, 50, 200)

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]



        for c in cnts:

            M = cv2.moments(c)
            print(M)
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)
            shape = self.detector(c)

            c = ratio

            cv2.drawContours(frame, c[0], -1, (0, 255, 0), 2)
            cv2.putText(frame, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.imshow("Frame", frame)
            pass

        cv2.imshow("Frame", thresh)


        pass



    def detector(self,c):
        #--Initialize the shape name and approximate the contour
        shape = "Unknow"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 *peri, True)

        #-- if the shape es a triangle, i will have three vertices
        if len(approx == 3):
            shape = "Triangle"
            pass
        elif len(approx == 4):
            # compute the bounding box of the contour and use the
            # baounding box to copute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "Square" if ar >= 0.95 and ar <= 1.95 else "rectangle"
            pass
        elif len(approx == 5):
            shape = "Pentangon"
            pass
        else:
            shape = "circle"
            pass
        return  shape
        pass


App = Vision()
App.getFrame()


















