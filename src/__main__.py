from ga import GA
from vis import Vis
from arm import Arm
from icecream import ic
from time import time


def main():
    arm = Arm()
    ga = GA(arm)
    angs, curr = ga.run()
    return angs, curr


if __name__ == "__main__":
    # ===========================================================\
    import numpy as np
    x = np.array([[0, 0],
                  [10, 110],
                  [110, 110],
                  [110, 10],
                  [110, 110]])
    from utils import check_self_cross
    # ic(check_self_cross(x))
    # ===========================================================
    best = 10 ** 2
    iter = 0
    while best > 1.5:
        iter += 1
        start_time = time()
        angs, curr = main()
        ic("time it took: {:.2f}".format(time() - start_time))
        if curr < best:
            best = curr
        ic("iter {}: {:.2f}\n".format(iter, curr))
    ic("Best result: {:.2f}".format(best))
    vis = Vis(angs)
    vis.vis2D()
