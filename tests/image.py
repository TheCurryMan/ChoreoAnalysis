import cv2
import numpy as np

from constants import POSE_PAIRS
from utils import get_points

frame = cv2.imread("res/img/single.jpeg")
pts = get_points(frame, 368, 368)[0]
frame_copy = np.copy(frame)
for i in range(len(pts)):
    x, y = pts[i]
    cv2.circle(frame_copy, (int(x), int(y)), 8, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
    cv2.putText(frame_copy, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                lineType=cv2.LINE_AA)

for (a, b) in POSE_PAIRS:
    if pts[a] and pts[b]:
        cv2.line(frame_copy, pts[a], pts[b], (0, 255, 255), 3, lineType=cv2.LINE_AA)
        cv2.circle(frame_copy, pts[a], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
        cv2.circle(frame_copy, pts[b], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
cv2.imshow('Key points', frame_copy)
cv2.waitKey(0)
