#!/usr/bin/python3
import time

import cv2
import numpy as np

from picamera2 import MappedArray, Picamera2, Preview
from picamera2.encoders import H264Encoder

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration())

colour = (0, 255, 0)
origin = (0, 30)
font = cv2.FONT_HERSHEY_SIMPLEX
scale = 1
thickness = 2

# morpho-kernel
kernel = np.ones((10, 10), np.uint8)


def apply_timestamp(request):
    timestamp = time.strftime("%Y-%m-%d %X")
    with MappedArray(request, "main") as m:
        cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)

def cluster(request):
    with MappedArray(request, "main") as m:
        gs=cv2.cvtColor(m.array, cv2.COLOR_BGR2GRAY)
        th,bob = cv2.threshold(gs, 128, 192, cv2.THRESH_OTSU)
        bob = cv2.erode(bob, kernel) 
        cv2.imwrite('opencv_th_otsu.jpg', bob)


def blob(request):
    with MappedArray(request, "main") as m:
        detector = cv2.SimpleBlobDetector()

        gs=cv2.cvtColor(m.array, cv2.COLOR_BGR2GRAY)
        th,bob = cv2.threshold(gs, 128, 192, cv2.THRESH_OTSU)
        bob = cv2.erode(bob, kernel) 

        # Detect blobs.
        keypoints = detector.detect(bob)
 
        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        im_with_keypoints = cv2.drawKeypoints(m.array, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
        # Show keypoints
        # cv2.imshow("Keypoints", im_with_keypoints)
        # cv2.waitKey(0)
        # time.sleep(1)
        cv2.imwrite('opencv_th_otsu.jpg', im_with_keypoints)
        

picam2.pre_callback = blob


picam2.set_controls({"ExposureTime": 1000, "AnalogueGain": 1.0})
picam2.start_preview(Preview.QT)
picam2.start()

time.sleep(3)
