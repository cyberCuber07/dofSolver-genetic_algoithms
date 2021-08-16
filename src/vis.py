import numpy as np
from numpy import sin, cos
from parms import *
from arm import Arm
import cv2
from utils import get_points, mod_target
from icecream import ic
import matplotlib.pyplot as plt


class Vis:
    def __init__(self, angs):
        self.angs = angs
        self.links = LINKS
        self.target = mod_target(TARGET)
        self.ss = SS

    def vis2D(self):

        points = np.zeros((len(self.angs) + 1, 2))
        cnt = 0
        for (l, ang) in zip(self.links, self.angs):
            points[cnt + 1, 0] = points[cnt, 0] + l * np.cos(ang)
            points[cnt + 1, 1] = points[cnt, 1] + l * np.sin(ang)
            cnt += 1

        ax = plt.axes()

        for idx in range(points.shape[0] - 1):
            ax.arrow(points[idx, 0],
                     points[idx, 1],
                     points[idx + 1, 0] - points[idx, 0],
                     points[idx + 1, 1] - points[idx, 1],
                     head_width=0.5,
                     head_length=0.7)
            plt.scatter(points[idx, 0], points[idx, 1])
            plt.scatter(points[idx + 1, 0], points[idx + 1, 1])

        plt.show()
