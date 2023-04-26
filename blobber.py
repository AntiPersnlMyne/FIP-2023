#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# blobber.py - finds robot blobs
#
# flip & aidan
# spring 2023
#
# Based on FIP2022 code by Mason and Karla
# 

import socketserver
import threading
import time

import cv2
import time
import numpy as np
import random


from picamera2 import Picamera2, MappedArray

# debuggery
import pprint
import inspect

# comms
from base64 import encode


# remapper

class Calibration():
    """Arena calibration, p = pixels, m = meat space"""
    p1 = (0,0)
    p2 = (0,0)
    p3 = (0,0)

    m1 = (0,0)
    m2 = (0,0)
    m3 = (0,0)

    def __init__(self, p1, p2, p3, m1, m2, m3) -> None:
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self.m1 = m1
        self.m2 = m2
        self.m3 = m3

        # pass

    def set(self, p1, p2, p3, m1, m2, m3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self.m1 = m1
        self.m2 = m2
        self.m3 = m3

    def transform(self, p):
        """Transform from pixels to meat space"""
        # TODO
        return p
    
    def inverse(self, m):
        """Transform from meat space to pixels"""
        # TODO
        return m   
    

## Robot state

class Robot():
    """Robot state"""
    bx = 0.0
    by = 0.0
    lastx = 0.0
    lasty = 0.0

    def __init__(self, x, y) -> None:
        self.bx = x
        self.by = y
        #pass

    def get(self):
        return self.bx, self.by

    def set(self, x, y):
        # memories
        self.lastx = self.bx
        self.lasty = self.by

        #current
        self.bx = x
        self.by = y
    
    def delta(self):
        return self.bx - self.lastx, self.by - self.lasty


class RobotThread(threading.Thread):
    """Robot detection thread"""

    def __init__(self):
        threading.Thread.__init__(self)
        #initialize camera
        print("Robot Thread initialized")

    def findRobot(self):
        #find x y of robots
        global rOtto, rManuel
        
        #curx, cury = rOtto.get()
        #print(curx, cury)
        #rOtto.set(curx+(0.1*(random.random()-0.5)), cury+(0.1*(random.random()-0.5)))

    
    def run(self):
        #calls find ball over and over
        print("Robot thread go")
        while True:
            self.findRobot()
  

# blobber
def setup_blob():
    """Setup SimpleBlobDetector parameters."""
    
    global detector

    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 200
    params.maxThreshold = 255

    # find bright
    params.filterByColor = True
    params.blobColor = 255

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 10
    params.maxArea = 500

    # Filter by Circularity
    params.filterByCircularity = False
    # params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = False
    # params.minConvexity = 0.87

    # Filter by Inertia
    params.filterByInertia = False
    # params.minInertiaRatio = 0.01

    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector.create(params)


def track(request):
    """Tracker Callback"""
    global detector, rOtto
    
    with MappedArray(request, "main") as m:
        keypoints = detector.detect(m.array)

        for k in keypoints:
            # pprint.pprint((k.pt, k.size))
            rOtto.set(k.pt[0],k.pt[1])


def setup_camera():
    """Setup the camera."""

    global picam2
    
    # create camera instance
    picam2 = Picamera2()

    video_config = picam2.create_video_configuration(main={"size": (1280, 720), "format": "RGB888"},
                                                     lores={"size": (640, 480), "format": "YUV420"})


    picam2.configure(video_config)
    picam2.set_controls({"ExposureTime": 1000, "AnalogueGain": 1.0})

    # set the callback
    picam2.pre_callback = track

    # start, give it a tick to wait
    picam2.start_preview()
    picam2.start()





class MyTCPHandler(socketserver.BaseRequestHandler):
    """from the socketserver docs"""
    def handle(self):
        
        global server
        global rOtto

        while True:
            # self.request is the TCP socket connected to the client
            self.data = self.request.recv(1024).strip()
            # print("{} wrote:".format(self.client_address[0]))
            # print(self.data)
            if self.data == b'getloc':
                posx, posy = rOtto.get()
                message = bytes('%.3f' % posx+','+ '%.3f' % posy,'UTF-8')
                self.request.sendall(message)
                # print("sent",message)
            elif self.data == b'done' or self.data == b'':
                self.request.sendall(b"quitting")
                # print("quitting")
                server.shutdown()
            else:
                # print("unknown message")
                pass

        # encoding example    
        # thesx=str(ppp[0])+','+str(ppp[1])
        # self.request.sendall(bytearray(thesx.encode()))
        # #time.sleep(.1)
        # fieldnames = [ 'X', 'Y' ]      

if __name__=="__main__":

    # global robots
    rOtto = Robot(300.0*random.random(), 200.0*random.random())
    rManuel = Robot(300.0*random.random(), 200.0*random.random())
    
    # calibration
    # pixel space (right now in col,row space) then meat space (in cm right now)        
    cal = Calibration((0.0, 480.0), (640.0, 480.0), (0.0, 0.0),
                      (0.0, 0.0), (300.0, 0.0), (0.0, 200.0))
    
    # tracker
    setup_blob()
    setup_camera()

    # robotThread = RobotThread()
    # robotThread.start()

    HOST, PORT = "192.168.0.10", 9998
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

    # call server.shutdown() to stop the server

    picam2.stop()
    