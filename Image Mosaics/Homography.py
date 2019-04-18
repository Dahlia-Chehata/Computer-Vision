import numpy as np

def calculate_h(p, p_):
    "takes setof points p and their corresponting points p_ , calculates the Homography matrix, returns 3x3 matrix"
    # p is array of correspondance points of image 1, p_ is same for image 2
    B = p_
    A = np.zeros([2 * p.shape[0], 8])  # construct A from input points
    for i in range(p.shape[0]):  # constructs A from given points of image 1
        A[i * 2] = p[i, 0], p[i, 1], 1, 0, 0, 0, -p[i, 0] * p_[i, 0], -p[i, 1] * p_[i, 0]
        A[i * 2 + 1] = 0, 0, 0, p[i, 0], p[i, 1], 1, -p[i, 0] * p_[i, 1], -p[i, 1] * p_[i, 1]

    B = B.flatten().reshape(-1, 1)  # flatten and reshape to be one column for dimension suitability

    H = np.linalg.lstsq(A, B, rcond=None)[0]  # returns H

    H = np.append(H, 1)  # puts 1 at the end of H

    H = np.reshape(H, [3, 3])  # return H as matrix of shape 3x3
    return H


def InvTransform(h, point):
    "for a point in second image gets its correspondance in first image"

    inverse_point = np.dot(np.linalg.inv(h), point);  # matrix multiplication with the inverse of H
    inverse_point[0] /= inverse_point[2]  # divides by weight
    inverse_point[1] /= inverse_point[2]
    return inverse_point[0:2]


def transform(h, point):
    "for a point in first image gets its correspondance in second image "
    corr_point = np.dot(h, point);
    corr_point[0] /= corr_point[2];
    corr_point[1] /= corr_point[2]
    return corr_point[0:2]


def from_homo(points):
    "converts homogoneous representation of a point a non-homo representation"

    points[:, 0] /= points[:, 2]
    points[:, 1] /= points[:, 2]

    return points[:, 0:2]