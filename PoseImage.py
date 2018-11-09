import cv2
import time
import numpy as np


protoFile = "pose/pose.prototxt"
weightsFile = "pose/pose.caffemodel"
nPoints = 15
POSE_PAIRS = [[0,1], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [1,14], [14,8], [8,9], [9,10], [14,11], [11,12], [12,13] ]


"""frame = cv2.imread('filename.jpg')
frame = cv2.resize(frame, (0, 0), fx=0.1, fy=0.1)
points = PoseImage.getPoints(frame)
"""
#returns 13 pairs in an array
def getPoints(frame):
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    threshold = 0.01

    net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

    t = time.time()
    # input image dimensions for the network
    inWidth = 368
    inHeight = 368
    inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight),
                              (0, 0, 0), swapRB=False, crop=False)

    net.setInput(inpBlob)

    output = net.forward()
    print("time taken by network : {:.3f}".format(time.time() - t))

    H = output.shape[2]
    W = output.shape[3]

    # Empty list to store the detected keypoints
    points = []
    ratios = []
    for i in range(nPoints):
        # confidence map of corresponding body's part.
        probMap = output[0, i, :, :]

        # Find global maxima of the probMap.
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
        
        # Scale the point to fit on the original image
        x = (frameWidth * point[0]) / W
        y = (frameHeight * point[1]) / H

        if prob > threshold : 
            # Add the point to the list if the probability is greater than the threshold
            points.append((int(x), int(y)))
            ratios.append([point[0]/W,point[1]/H])
        else :
            points.append(None)
    return points, ratios

