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

import sys

from picamera2 import Picamera2, MappedArray

# debuggery
from pprint import pprint
import inspect

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
    params.filterByArea = False
    params.minArea = 3
    params.maxArea = 100

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

ddt = 0

def track(request):
    """Tracker Callback"""
    global detector, rOtto, rManuel
    global ddt, dtx

    t0 = time.time()

    with MappedArray(request, "lores") as m:

        k = detector.detect(m.array)

        if len(k) > 0:
            # pprint(k[0].pt)

            # if k[0].size > k[1].size:
            rOtto.set(k[0].pt[0],k[0].pt[1])
            #     rManuel.set(k[1].pt[0],k[1].pt[1])
            # else:
            #     rManuel.set(k[0].pt[0],k[0].pt[1])
            #     rOtto.set(k[1].pt[0],k[1].pt[1])              

    # dt = time.time() - t0
    # ddt = (ddt + dt) / 2.0
    # print(1/ddt)

        


def setup_camera():
    """Setup the camera."""

    global picam2

    tuning = Picamera2.load_tuning_file("imx519.json")

    #algo = Picamera2.find_tuning_algo(tuning, "rpi.agc")
    #algo["exposure_modes"]["normal"] = {"shutter": [100, 66666], "gain": [1.0, 8.0]}
    
    #picam2 = Picamera2(tuning=tuning)

    # create camera instance
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(main={"size": (2328,1748), "format": "RGB888"},
                                                     lores={"size": (640,480), "format": "YUV420"})

    # video_config = picam2.create_video_configuration(main={"size": (1280,720), "format": "RGB888"})

    picam2.configure(video_config)
    picam2.set_controls({"AnalogueGain": 10.0})

    # set the callback
    picam2.pre_callback = track

    # start, give it a tick to wait
    # picam2.start_preview()
    picam2.start()




class MyTCPHandler(socketserver.BaseRequestHandler):
    """from the socketserver docs"""
    def handle(self):
        
        global server
        global rOtto, rManuel

        while True:
            # self.request is the TCP socket connected to the client
            self.data = self.request.recv(1024).strip()
            # print("{} wrote:".format(self.client_address[0]))
            print(self.data)

            if self.data == b'getotto':
                posx, posy = rOtto.get()
            elif self.data == b'getmanuel':
                posx, posy = rManuel.get()
            elif self.data == b'getdotto':
                posx, posy = rOtto.delta()
            elif self.data == b'getdmanuel':
                posx, posy = rManuel.delta()
            
            elif self.data == b'done' or self.data == b'':
                self.request.sendall(b"quitting")
                # print("quitting")
                picam2.stop()
                sys.exit()
                server.shutdown()
            else:
                # print("unknown message")
                return

            message = bytes('%.3f' % posx+','+ '%.3f' % posy,'UTF-8')
            self.request.sendall(message)
            # print("sent",message)
   

if __name__=="__main__":

    # global robots
    rOtto = Robot(0., 0.)
    rManuel = Robot(0., 0.)
    
    # calibration
    # pixel space (right now in col,row space) then meat space (in cm right now)        
    # cal = Calibration((0.0, 480.0), (640.0, 480.0), (0.0, 0.0),
    #                   (0.0, 0.0), (300.0, 0.0), (0.0, 200.0))
    
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

    