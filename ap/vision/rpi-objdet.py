#!/usr/bin/env python3

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from cv2 import dnn
import numpy as np

# camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
#camera.vflip = True
rawCapture = PiRGBArray(camera, size=camera.resolution)
time.sleep(0.1)


inWidth = 300
inHeight = 300
inScaleFactor =  0.007843
meanVal = (127.5, 127.5, 127.5)
prototxt = "models/deploy.prototxt"
caffemodel = "models/mobilenet_ssd.caffemodel"

classNames = { 0: 'background',
    1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
    5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
    10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
    14: 'motorbike', 15: 'person', 16: 'pottedplant',
    17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor' }


def postProc(detection, frame, classNames):
    cols = 300
    rows = 300
    class_id    = int(detection[1])
    confidence  =     detection[2]
    if (confidence < 0.25):
        return
    xLeftBottom = int(detection[3] * cols)
    yLeftBottom = int(detection[4] * rows)
    xRightTop   = int(detection[5] * cols)
    yRightTop   = int(detection[6] * rows)
    #print(confidence, classNames[class_id], xLeftBottom, yLeftBottom, xRightTop, yRightTop)
    # Factor for scale to original size of frame
    heightFactor = frame.shape[0]/rows
    widthFactor = frame.shape[1]/cols
    # Scale object detection to frame
    xLeftBottom = int(widthFactor * xLeftBottom)
    yLeftBottom = int(heightFactor * yLeftBottom)
    xRightTop   = int(widthFactor * xRightTop)
    yRightTop   = int(heightFactor * yRightTop)
    #print(confidence, classNames[class_id], xLeftBottom, yLeftBottom, xRightTop, yRightTop)
    # Draw location of object  
    cv2.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop), (0, 255, 0))
    # Draw label and confidence of prediction in frame resized
    if class_id in classNames:
        label = classNames[class_id] + ": " + str(confidence)
        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        yLeftBottom = max(yLeftBottom, labelSize[1])
        cv2.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]),
                             (xLeftBottom + labelSize[0], yLeftBottom + baseLine),
                             (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, label, (xLeftBottom, yLeftBottom),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
        #print(label) #print class and confidence
                
net = dnn.readNetFromCaffe(prototxt, caffemodel)

frame_count = 0
start = time.time()
for framePi in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = framePi.array
        frame_resized = cv2.resize( frame,(300,300))

        blob = dnn.blobFromImage( frame_resized, inScaleFactor, (inWidth, inHeight), meanVal, False)
        net.setInput(blob)
        detections = net.forward()

        for detection in detections[0,0,:,:]:
                #postProc(detection, frame, classNames)
                class_id    = int(detection[1])
                class_name = classNames[class_id]
                confidence = detection[2]
                if (confidence >= 0.25):
                    print(class_name + ' ' + str(confidence))
        
        #cv2.imshow("Frame", frame)
        frame_count = frame_count + 1
        end = time.time()
        #print( frame_count / (end - start) )
        key = cv2.waitKey(1) & 0xFF

        rawCapture.truncate(0)

        if key == ord("q"):
                        break

