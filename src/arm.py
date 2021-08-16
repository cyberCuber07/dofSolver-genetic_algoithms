import numpy as np
from numpy import sin, cos
from parms import *
from icecream import ic


class Arm:
    def __init__(self):
        self.links = LINKS
        self.ang_limits = ANG_LIMITS
        self.target = TARGET
        self.n_sets = N_SETS
        self.n = N
        self.ang_z = self.cal_ang_z()
        self.bound = BOUND
        self.ss = SS

    def cal_ang_z(self):
        """
        method to calculate the angle on OZ axis
        ** default angle is 0 --- through the OX axis (axis of robots movement)
        """
        c = np.linalg.norm(self.target)
        _sin = self.target[1] / c
        _cos = self.target[0] / c
        return np.arctan2(_sin, _cos)

    def init_pos(self):
        angs = np.zeros((self.n_sets, self.n))
        for iter in range(self.n_sets):
            for idx, ang in enumerate(self.ang_limits):
                ang_tmp = np.random.uniform(low=ang[0], high=ang[1], size=(1,1))
                angs[iter, idx] = ang_tmp
        return np.array(angs)

    def Rx(self, ang):
        R = [[1, 0, 0],
             [0, cos(ang), -sin(ang)],
             [0, sin(ang), cos(ang)]]
        return np.array(R)

    def Ry(self, ang):
        R = [[cos(ang), 0, sin(ang)],
             [0, 1, 0],
             [-sin(ang), 0, cos(ang)]]
        return np.array(R)

    def Rz(self, ang):
        R = [[cos(ang), -sin(ang), 0],
             [sin(ang), cos(ang), 0],
             [0, 0, 1]]
        return np.array(R)

    def count_pos(self, one_set):
        """before using: configure to correct cord sys"""
        pos = np.zeros((3, 1))
        ang_z = self.ang_z
        ang_tmp = 0
        R10 = self.Rz(ang_z)
        points = [[0, 0, 0]]
        for (l, ang, _s) in zip(self.links, one_set, self.ss):
            ang_tmp += ang * _s
            # R10 = np.matmul(R10, self.Ry(ang_tmp))
            R10 = np.matmul(self.Rz(ang_z), self.Ry(ang_tmp))
            link = np.array([l, 0, 0]).reshape((3, 1))
            pos += np.matmul(R10, link)
            points.append(list([i[0] for i in pos]))
        return pos.reshape((3,)), np.array(points)

    def fitness(self, angs):
        tmp = np.zeros((self.n_sets, 3))
        for idx, _angs in enumerate(angs):
            tmp_val, _ = self.count_pos(_angs)
            tmp[idx] = tmp_val
        return np.array([np.linalg.norm(np.array([i, j, k]) - self.target) for (i, j, k) in tmp])

    def ex_dis(self, angs, type_name="max"):
        """
        fitness method to check maximum / minimum accesible distance
        """
        check_type = {"max": -1, "min": 1}
        one = check_type[type_name]
        tmp = np.zeros((self.n_sets, 3))
        for idx, _angs in enumerate(angs):
            tmp[idx] = self.count_pos(_angs)
        return np.array([one * np.linalg.norm(np.array([i, j, k])) for (i, j, k) in tmp])
