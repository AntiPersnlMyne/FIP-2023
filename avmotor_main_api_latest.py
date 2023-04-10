#!/usr/bin/env python3
"""
The code is edited from docs (https://docs.luxonis.com/projects/api/en/latest/samples/Yolo/tiny_yolo/)
We add parsing from JSON files that contain configuration
"""

from pathlib import Path
import sys
import cv2
import depthai as dai
import numpy as np
import time
import argparse
import json
import blobconverter
import random
from DFRobot_RaspberryPi_DC_Motor import DFRobot_DC_Motor_IIC as Board


board = Board(1, 0x10)    # Select bus 1, set address toboard = Board(1, 0x10)    # Select bus 1, set address to 0x10 0x10

board.set_encoder_enable(board.ALL)                 # Set selected DC motor encoder enable
  # board.set_encoder_disable(board.ALL)              # Set selected DC motor encoder disable
board.set_encoder_reduction_ratio(board.ALL, 43)    # Set selected DC motor encoder reduction ratio, test motor reduction ratio is 43.8

board.set_moter_pwm_frequency(1000)   # Set DC motor pwm frequency to 1000HZ

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", help="/home/whitewalter/depthai-python/examples/gen2-yolo/exp-device-decoding/model/best55_openvino_2021.4_6shave.blob",
                    default='/home/whitewalter/depthai-python/examples/gen2-yolo/exp-device-decoding/model/best55_openvino_2022.1_6shave.blob', type=str)
parser.add_argument("-c", "--config", help="/home/whitewalter/depthai-python/examples/gen2-yolo/exp-device-decoding/model/best55.json",
                    default='/home/whitewalter/depthai-python/examples/gen2-yolo/exp-device-decoding/model/best55.json', type=str)
args = parser.parse_args()

# parse config
configPath = Path(args.config)
if not configPath.exists():
    raise ValueError("Path {} does not exist!".format(configPath))

with configPath.open() as f:
    config = json.load(f)
nnConfig = config.get("nn_config", {})

# parse input shape
if "input_size" in nnConfig:
    W, H = tuple(map(int, nnConfig.get("input_size").split('x')))

# extract metadata
metadata = nnConfig.get("NN_specific_metadata", {})
classes = metadata.get("classes", {})
coordinates = metadata.get("coordinates", {})
anchors = metadata.get("anchors", {})
anchorMasks = metadata.get("anchor_masks", {})
iouThreshold = metadata.get("iou_threshold", {})
confidenceThreshold = metadata.get("confidence_threshold", {})

print(metadata)

# parse labels
nnMappings = config.get("mappings", {})
labels = nnMappings.get("labels", {})

# get model path
nnPath = args.model
if not Path(nnPath).exists():
    print("No blob found at {}. Looking into DepthAI model zoo.".format(nnPath))
    nnPath = str(blobconverter.from_zoo(args.model, shaves = 6, zoo_type = "depthai", use_cache=True))
# sync outputs
syncNN = True

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
camRgb = pipeline.create(dai.node.ColorCamera)
detectionNetwork = pipeline.create(dai.node.YoloDetectionNetwork)
xoutRgb = pipeline.create(dai.node.XLinkOut)
nnOut = pipeline.create(dai.node.XLinkOut)

xoutRgb.setStreamName("rgb")
nnOut.setStreamName("nn")

# Properties
camRgb.setPreviewSize(W, H)

camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setInterleaved(False)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
camRgb.setFps(60)
camRgb.initialControl.setManualFocus(120) # 0..255
#camRgb.initialControl.setExposureTime(100) # 0..255


# Network specific settings
detectionNetwork.setConfidenceThreshold(confidenceThreshold)
detectionNetwork.setNumClasses(classes)
detectionNetwork.setCoordinateSize(coordinates)
detectionNetwork.setAnchors(anchors)
detectionNetwork.setAnchorMasks(anchorMasks)
detectionNetwork.setIouThreshold(iouThreshold)
detectionNetwork.setBlobPath(nnPath)
detectionNetwork.setNumInferenceThreads(2)
detectionNetwork.input.setBlocking(False)

# Linking
camRgb.preview.link(detectionNetwork.input)
detectionNetwork.passthrough.link(xoutRgb.input)
detectionNetwork.out.link(nnOut.input)

def drivingNoise():
    randChngInDir = random.randint(0, 180)
    return randChngInDir


# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    # Output queues will be used to get the rgb frames and nn data from the outputs defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
    qDet = device.getOutputQueue(name="nn", maxSize=4, blocking=False)

    frame = None
    detections = []
    startTime = time.monotonic()
    counter = 0
    color2 = (255, 255, 255)

    # these are the states
    lDuty = 0
    rDuty = 0
    lDirection = board.CW
    rDirection = board.CW

    lPresence = False
    rPresence = False

    imLost = True
    lastSeenR = False
    lastSeenL = False
    
    wallAvoid = False
    obstAvoid = False

    rDetectedobs = False
    lDetectedobs = False

    rPresentobs = False
    lPresentobs = False

    search = True
    # @@@ @@@ @@@ @@@ @@@
     

    lostTime = time.monotonic()

    # nn data, being the bounding box locations, are in <0..1> range - they need to be normalized with frame width/height
    def frameNorm(frame, bbox):
        normVals = np.full(len(bbox), frame.shape[0])
        normVals[::2] = frame.shape[1]
        return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)

    def displayFrame(name, frame, detections):
        global lDuty, rDuty, lDirection, rDirection, lPresence, rPresence, imLost, lostTime, lastSeenR, lastSeenL, rDetectedobs, lDetectedobs, rPresentobs, lPresentobs, search 
        color = (255, 0, 0)            
        rDetected = False
        lDetected = False
        rDetectedobs = False
        lDetectedobs = False

        for detection in detections:
            bbox = frameNorm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
            cv2.putText(frame, labels[detection.label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.putText(frame, f"{int(detection.confidence * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)

            #declare a variable for motors
            xMidPos = ((bbox[2]+bbox[0])/2)
            yLowPos = (bbox[3])

            #/ Declaring what Booleans/States per Object /
            if (((labels[detection.label]) == ("Class_1"))): #Class 1 = ENEMY
                search = False
                if xMidPos >= 80: #finds center point of x position of bounding box, determines which side of frame it is on
                                  #If ENEMY found in right_vf
                    rDetected = True
                    lastSeenR = True
                    lastSeenL = False
                    #print('lastsceneR')
                if xMidPos <= 176: #finds center point of x position of bounding box, determines which side of frame it is on
                                   #If ENEMY found in right_vf
                    lDetected = True
                    lastSeenL = True
                    lastSeenR = False
                    #print('lastsceneL')
           
            if (((labels[detection.label]) == ("Class_2"))): #Class 2 = WALL
                
                if yLowPos >= 120: #finds center point of x position of bounding box, determines which side of frame it is o
                        print('wall! on right')
                        lDetected = False
                        rDetected = False
                        lastSeenR = True
                        lastSeenL = False
                        rDetectedobs = True
                        search = False
                        board.motor_movement([board.M1], board.CW, 40)
                        board.motor_movement([board.M2], board.CCW, 40)
                        time.sleep (.1)
                        #board.motor_movement([board.M1], board.CW, 30)
                        #board.motor_movement([board.M2], board.CW, 35)
                        #time.sleep (1)""" 

            if (((labels[detection.label]) == ("Class_0"))): #Class 1 = OBSTACLE
 
                if yLowPos >= 200: #finds center point of x position of bounding box, determines which side of frame it is on
                    if xMidPos >= 128: 
                        print('obstacle! on RIGHT')
                        lDetected = False
                        rDetected = False
                        rDetectedobs = True
                        rPresentobs = True
                        search = False
                        #board.motor_movement([board.M1], board.CW, 30)
                        #board.motor_movement([board.M2], board.CW, 35)
                        #time.sleep (.5)
                    if xMidPos < 128: 
                        print('obstacle! on LEFT')
                        lDetected = False
                        rDetected = False
                        lDetectedobs = True
                        lPresentobs = True
                        search = False
                        #board.motor_movement([board.M1], board.CW, 35)
                        #board.motor_movement([board.M2], board.CW, 30)
                        #time.sleep (.1)

            #\ Declaring Booleans \
            #         rDetectedOb = True
            #     if xMidPos < 220: #finds center point of x position of bounding box, determines which side of frame it is on
            #         lDetectedOb = True


        if lDetected or rDetected: #(Is there anything in a visual field) - Did I lose it?
            imLost = False
            search = False
            print ("I can see")
            # check each visual field
            if lDetected:
                if not lPresence:
                    rDuty = 90
                    rDirection = board.CW
                    lPresence = True
                    
            else:
                rDuty = 0
                lPresence = False

            if rDetected:
                if not rPresence:
                    lDuty = 90
                    lDirection = board.CW
                    rPresence = True
            else:
                lDuty = 0
                rPresence = False
        elif not imLost:
            imLost = True
            lostTime = time.monotonic()


        if lDetectedobs or rDetectedobs:
            imLost = False
            
            
            if lDetectedobs:
                if  lPresentobs:
                    rDuty = 50
                    rDirection = board.CCW
                    lDuty = 50
                    lDirection = board.CW
            else: 
                search = True
            if rDetectedobs: 
                if  rPresentobs:
                    lDuty = 50
                    lDirection = board.CCW
                    rDuty = 50
                    rDuty = board.CW 
            else: 
                search = True

        if search:
            rDuty = 40
            lDuty = 40
            lDirection = board.CW
            rDirection = board.CW
            print("searching")
            
        if imLost and lastSeenR and time.monotonic() - lostTime > 2: #Wandering: Last seen right
            if time.monotonic() - lostTime < 3:
                print ('Imlost')
                rDuty = 40
                lDuty = 50
                lDirection = board.CCW
                rDirection = board.CW
            else:
                search = True

        if imLost and lastSeenL and time.monotonic() - lostTime > 2: #Wandering: Last seen left
            if time.monotonic() - lostTime < 3:                       #If lost for >5 seconds,
                print ('Imlost')
                rDuty = 40
                lDuty = 50
                lDirection = board.CCW
                rDirection = board.CW
            else:                                                     #
                search = True
                   
        # carry out our behavior
        board.motor_movement([board.M2], lDirection, lDuty)
        board.motor_movement([board.M1], rDirection, rDuty)
        # Show the frame
        cv2.imshow(name, frame)

    while True:
        inRgb = qRgb.get()
        inDet = qDet.get()

        if inRgb is not None:
            frame = inRgb.getCvFrame()
            cv2.putText(frame, "NN fps: {:.2f}".format(counter / (time.monotonic() - startTime)),
                        (2, frame.shape[0] - 4), cv2.FONT_HERSHEY_TRIPLEX, 0.4, color2)

        if inDet is not None: 
            detections = inDet.detections
            counter += 1

        if frame is not None: # Run main Function
            displayFrame("rgb", frame, detections)

        if cv2.waitKey(1) == ord('q'): # Exit key 'q'
            board.motor_movement([board.M1], rDirection, 0)
            board.motor_movement([board.M2], lDirection, 0)
            break