def center_around(pts, center):
    return [(pt[0] - center[0], pt[1] - center[1]) for pt in pts]


def dist(pt_a, pt_b):
    return ((pt_a[0] - pt_b[0]) ** 2 + (pt_a[1] - pt_b[1]) ** 2) ** 0.5
