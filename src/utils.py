import numpy as np
from numpy import sin, cos
from icecream import ic
from parms import SS


n = 10 ** 2


def get_points(angs, links, ang_z):
    points = np.zeros((angs.shape[0] + 1, 3))
    idx = 0
    for (l, ang, _s) in zip(links, angs, SS):
        points[idx + 1, 2] += ang * _s
        points[idx + 1, 0] += points[idx, 0] + l * cos(points[idx + 1, 2])
        points[idx + 1, 1] += points[idx, 1] + l * sin(points[idx + 1, 2])
        idx += 1
    points = points[:, :2]
    return points


# ========================================================================
# methods to check if in correct bounds
def check_self_cross(points):
    from copy import deepcopy
    from icecream import ic
    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    # line_intersection method should return None if lines staring from one point
    def line_intersection(line1, line2):
        # ic(line1, line2)
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])
        div = det(xdiff, ydiff)
        if div == 0: return None
        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div

        # print(det(d, xdiff) / div, det(d, ydiff) / div)
        def check_val(linex):
            for i in range(2):
                if linex[0][i] > linex[1][i]:
                    tmp_val = linex[0][i]
                    linex[0][i] = linex[1][i]
                    linex[1][i] = tmp_val
            return linex

        line1 = check_val(deepcopy(line1))
        line2 = check_val(deepcopy(line2))
        # print(line1, line2, x, y)
        if line1[0][0] <= x <= line1[1][0] and line1[0][1] <= y <= line1[1][1] and \
                line2[0][0] <= x <= line2[1][0] and line2[0][1] <= y <= line2[1][1]:
            return x, y
        else:
            return None

    # ********************************************************************************
    # consider modifying the code --- not to use IF statement !!!!
    # ********************************************************************************
    for i in range(points.shape[0] - 1):
        for j in range(points.shape[0] - 1):
            if j != i:
                line1 = [points[i + k] for k in range(2)]
                line2 = [points[j + k] for k in range(2)]
                if line_intersection(line1, line2) is not None:
                    return True
    return False


def check_bound_cross(points, bound):
    def check_line(p1, p2, el_num=10):
        line = np.linspace(p1, p2, el_num)
        for point in line:
            cnt = 0
            for idx, one in enumerate(point):
                # checks if point's (one) coordinate is not in the BOX --- robot's bounds
                if not (bound[idx, 0] < one < bound[idx, 1]):
                    cnt += 1
                if cnt == 3:
                    return True
        return False

    for i in range(points.shape[0] - 1):
        if check_line(points[i], points[i + 1]):
            return True
    return False


def check_valid(angs, target, links, bound, ang_z):
    """
    later change the method
    """
    cnt = 0
    for _angs in angs:
        points = get_points(_angs, links, ang_z)
        cnt += 1
        # if cnt == n - 52:
        #     ic(points)
        if len(target) == 3:
            target = [np.sqrt(target[0] ** 2 + target[1] ** 2), target[2]]
        if check_self_cross(points):
            return True
        if check_bound_cross(points, bound):
            return True
    return False
# ========================================================================


def mod_target(target):
    return np.array([np.linalg.norm([i for i in target[:2]]), target[2]])
