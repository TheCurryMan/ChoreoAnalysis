from math import degrees, atan2

import numpy as np

from utils import get_points


def abs_angle(pts, a):
    return (360 + degrees(atan2(-1 * (pts[a[1]][1] - pts[a[0]][1]), pts[a[1]][0] - pts[a[0]][0]))) % 360


def rel_angle(points, arr):
    p0 = points[arr[0]]
    p1 = points[arr[1]]
    p2 = points[arr[2]]
    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p1)
    angle = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
    return np.degrees(angle)


def get_diffs(mod_frame, inp_frame):
    model_points, ratios_m = get_points(mod_frame, 368, 368)
    input_points, ratios_i = get_points(inp_frame, 368, 368)

    right_arm = [[2, 3], [3, 4], [2, 4], [2, 3, 4]]
    left_arm = [[5, 6], [6, 7], [5, 7], [5, 6, 7]]
    right_leg = [[8, 9], [9, 10], [8, 10], [8, 9, 10]]
    left_leg = [[11, 12], [12, 13], [11, 13], [11, 12, 13]]
    funcs = [abs_angle, abs_angle, abs_angle, rel_angle]
    limbs = [right_arm, left_arm, right_leg, left_leg]
    limb_diffs = []
    limb_diff = []
    weights = [.5, .5, .75, .25]
    for limb in limbs:
        input_angles = []
        model_angles = []
        for i in range(len(limb)):
            model_angles.append(funcs[i](model_points, limb[i]))
            input_angles.append(funcs[i](input_points, limb[i]))
        diffs = []
        total_diff = 0
        for i in range(len(model_angles)):
            di = abs(model_angles[i] - input_angles[i])
            diffs.append(min([di, 360 - di]))
            total_diff += diffs[i] / 360.0 * weights[i]
        total_diff /= len(diffs)
        limb_diffs.append(diffs)
        limb_diff.append(total_diff)
    return limb_diff, model_points, input_points, ratios_i, ratios_m


def diff_to_error(diff):
    if diff > 0.12:
        return 3
    elif diff > 0.06:
        return 2
    else:
        return 1
