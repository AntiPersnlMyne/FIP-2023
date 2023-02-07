#this code turns the motor in increments of 4 seconds.

from __future__ import print_function
import sys
import os
import time
from DFRobot_RaspberryPi_DC_Motor import DFRobot_DC_Motor_IIC as Board

import cv2

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
                    
                   
                    sys.path.append("../")



                    board = Board(1, 0x10)    # Select bus 1, set address to 0x10

                    def board_detect():
                      l = board.detecte()
                      print("Board list conform:")
                      print(l)

                    ''' print last operate status, users can use this variable to determine the result of a function call. '''
                    def print_board_status():
                      if board.last_operate_status == board.STA_OK:
                        print("board status: everything ok")
                      elif board.last_operate_status == board.STA_ERR:
                        print("board status: unexpected error")
                      elif board.last_operate_status == board.STA_ERR_DEVICE_NOT_DETECTED:
                        print("board status: device not detected")
                      elif board.last_operate_status == board.STA_ERR_PARAMETER:
                        print("board status: parameter error, last operate no effective")
                      elif board.last_operate_status == board.STA_ERR_SOFT_VERSION:
                        print("board status: unsupport board framware version")

                    if __name__ == "__main__":

                      board_detect()    # If you forget address you had set, use this to detected them, must have class instance

                      # Set board controler address, use it carefully, reboot module to make it effective
                      '''
                      board.set_addr(0x10)
                      if board.last_operate_status != board.STA_OK:
                        print("set board address faild")
                      else:
                        print("set board address success")
                      '''

                      while board.begin() != board.STA_OK:    # Board begin and check board status
                        print_board_status()
                        print("board begin faild")
                        time.sleep(2)
                      print("board begin success")

                      # board.set_encoder_enable(board.ALL)                 # Set selected DC motor encoder enable
                      board.set_encoder_disable(board.ALL)                  # Set selected DC motor encoder disable
                      board.set_encoder_reduction_ratio(board.ALL, 43)      # Set selected DC motor encoder reduction ratio, test motor reduction ratio is 43.8

                      board.set_moter_pwm_frequency(1000)   # Set DC motor pwm frequency to 1000HZ
                      x=0 
                      board.motor_movement([1], board.CCW, 50)    # DC motor 1 movement, orientation clockwise
                      time.sleep(4)
                      board.motor_stop(board.ALL)   #stop all DC motor
                      print_board_status()
                      time.sleep(4)
                      x+=1 
                      print(x)
                      board.motor_stop(board.ALL)



    return img,objectInfo


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)


    while True:
        success, img = cap.read()
        result, objectInfo = getObjects(img,0.45,0.2, objects=['person'])
        print(objectInfo)
        #cv2.imshow("Output",img)
        cv2.waitKey(1)
