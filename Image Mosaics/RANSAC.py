import numpy as np
import math
import random
import Homography

def ransac_error(single_p, single_p_, h):
    "calcualtes difference between the calculated point and the given point"
    point = np.array([single_p[0], single_p[1], 1])
    calculated_point_ = np.dot(h, point.reshape(-1, 1))
    calculated_point_ /= calculated_point_[2]

    error = calculated_point_[0:2] - single_p_.reshape(-1, 1)  # difference

    error = np.square(error)  # squared

    error = np.sum(error)  # sum of dimensions

    return math.sqrt(error)


def ransac(p, p_, threshold, iterations):
    "takes coreespondance points and for each 4 random pairs it calculates h and counts inliners from a given threshold and keeps the best h"
    max_inliners = 0
    best_h = None

    for i in range(iterations):
        inliners = 0
        randp = np.zeros([4, 2])
        randp_ = np.zeros([4, 2])
        H = None
        for j in range(4):
            random_index = random.randrange(0, p.shape[0], 1)  # picks random points from the given set

            randp[j] = p[random_index]
            randp_[j] = p_[random_index]

        H = Homography.calculate_h(randp, randp_)  # calculates h from the 4 random points

        for j in range(p.shape[0]):
            error = ransac_error(p[j], p_[j], H)

            if (error < threshold):
                inliners += 1

        if (inliners > max_inliners):
            max_inliners = inliners
            best_h = H
            # return the H and the number of inliners for H
    return best_h, max_inliners