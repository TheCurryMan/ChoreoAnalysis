import numpy as np

from algorithms.utils import center_around


def similarity(p1, p2):
    """
    For each position vector v1 and v2, finds the perpendicular component of v2 w.r.t. v1 and takes the ratio of the
    length of this perpendicular component to the ratio of v2.
    :param p1: Set of points describing model, where p1[1] is the 'central' vector
    :param p2: Set of points describing model, where p2[1] is the 'central' vector
    """
    m1 = center_around(p1, p1[1])
    m2 = center_around(p2, p2[1])
    del m1[1]
    del m2[1]
    ratios = []
    for i in range(len(m1)):
        a1 = np.array(m1[i])
        a2 = np.array(m2[i])
        perp = a2 - a2.dot(a1) / (np.linalg.norm(a1) ** 2) * a1
        ratio = np.linalg.norm(perp) / np.linalg.norm(a2)
        ratios.append(ratio)
    return sum(ratios) / len(ratios)
