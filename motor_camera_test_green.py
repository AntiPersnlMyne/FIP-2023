#the window to show what the camera sees does not appear when running the code.

from __future__ import print_function
import sys
import os
import time
from DFRobot_RaspberryPi_DC_Motor import DFRobot_DC_Motor_IIC as Board

import cv2
board = Board(1, 0x10) 

#thres = 0.45 # Threshold to detect object

classNames = []
classFile = "/home/green/Desktop/MOTOR/Object_Detection_Files/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "/home/green/Desktop/MOTOR/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/green/Desktop/MOTOR/Object_Detection_Files/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    
    return img,objectInfo


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)


    while True:
        success, img = cap.read()
        result, objectInfo = getObjects(img,0.45,0.2, objects=['person'])
        #cv2.imshow("Output",img)
        print(objectInfo)
        if objectInfo != []:
            print(objectInfo)
            board.set_encoder_disable(board.ALL)                  # Set selected DC motor encoder disable
            board.set_encoder_reduction_ratio(board.ALL, 43)      # Set selected DC motor encoder reduction ratio, test motor reduction ratio is 43.8
            board.set_moter_pwm_frequency(1000)   # Set DC motor pwm frequency to 1000HZ
            board.motor_movement([1,2], board.CCW, 50)
            time.sleep(1)    # DC motor 1 movement, orientation clockwise
        board.motor_stop(board.ALL) #stop all DC motor     
       
