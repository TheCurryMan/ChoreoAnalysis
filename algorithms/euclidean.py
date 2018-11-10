from algorithms.utils import center_around, dist


def similarity(pts1, pts2):
    centered1 = center_around(pts1, pts1[1])
    centered2 = center_around(pts2, pts2[1])
    del centered1[1]
    del centered2[1]
    h1 = ((centered1[10] - centered1[0]) + (
            centered1[13] - centered1[0])) / 2  # Averages distance from head to two feet
    h2 = ((centered2[10] - centered2[0]) + (centered2[13] - centered2[0])) / 2
    centered2 = [(pt[0], pt[1] * h1 / h2) for pt in centered2]
    return sum(dist(centered1[i], centered2[i]) for i in range(len(centered1)))
