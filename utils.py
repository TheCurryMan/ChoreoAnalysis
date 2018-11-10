import cv2

from constants import NET, N_POINTS, THRESHOLD


def get_points(frame, in_width, in_height):
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]
    NET.setInput(cv2.dnn.blobFromImage(frame, 1.0 / 255, (in_width, in_height), (0, 0, 0), swapRB=False, crop=False))
    output = NET.forward()
    height = output.shape[2]
    width = output.shape[3]
    points = []
    ratios = []
    for i in range(N_POINTS):
        prob_map = output[0, i, :, :]
        min_val, prob, min_loc, point = cv2.minMaxLoc(prob_map)
        if prob > THRESHOLD:
            x = (frame_width * point[0]) / width
            y = (frame_height * point[1]) / height
            points.append((int(x), int(y)))
            ratios.append((point[0] / width, point[1] / height))
        else:
            points.append(None)
    return [points, ratios]

