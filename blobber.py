# blobber

from picamera2 import Picamera2, MappedArray
import cv2
import numpy as np
import time
import pprint
import inspect

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


def setup_camera():
    global picam2
    
    # create camera instance
    picam2 = Picamera2()

    picam2.configure(picam2.create_video_configuration())
    picam2.set_controls({"ExposureTime": 1000, "AnalogueGain": 1.0})

def process_frame():
    """Do a single frame, manually"""

    # these are out in the globalness
    global picam2, detector

    # grab a frame
    im = picam2.capture_array("main")

    # convert it into gray and save it
    gs = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    # cv2.imwrite("bw.png", gs)

    # Detect blobs.
    keypoints = detector.detect(im)
    for k in keypoints:
        pprint.pprint((k.pt, k.size))

    # Draw detected blobs as circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    # im_with_keypoints = cv2.drawKeypoints(im, keypoints, 
    #                                       np.array([]), 
    #                                       (255, 0, 0), 
    #                                       cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # cv2.imwrite("bleh.png", im_with_keypoints)


def track(request):
    """Tracker Callback"""
    global detector, times

    with MappedArray(request, "main") as m:
        keypoints = detector.detect(m.array)
        times = times + 1

        # for k in keypoints:
        #     pprint.pprint((k.pt, k.size))

def calibrate():
    """Determine the remapping"""
    return

def toMeatSpace(kp):
    """does the transformation from sensor blob space to earth"""
    return kp.pt


if __name__=="__main__":

    setup_camera()
    setup_blob()

    # set the callback
    picam2.pre_callback = track

    times = 0
    # start, give it a tick to wait
    picam2.start()

    # go
    time.sleep(3)
    print(times,times/3.0)
    picam2.stop()
    