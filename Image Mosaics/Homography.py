import numpy as np
import cv2 as cv


def auto_calculate_homography(points1, points2):
    h, status = cv.findHomography(points1, points2)
    return h


def calculate_homography(points1, points2):
    """
     takes a pair of points list , calculates the Homography matrix, returns 3x3 matrix"
     points1 is array of correspondence points  ≥ 4 of image 1
     points2 is array of correspondence points  ≥ 4 of image 2
    """

    B = points2
    A = np.zeros([2 * points1.shape[0], 8])  # construct A from input points
    for i in range(points1.shape[0]):  # constructs A from given points of image 1
        A[i * 2] = points1[i, 0], points1[i, 1], 1, 0, 0, 0, -points1[i, 0] * points2[i, 0], \
                   -points1[i, 1] * points2[i, 0]

        A[i * 2 + 1] = 0, 0, 0, points1[i, 0], points1[i, 1], 1, -points1[i, 0] * points2[i, 1], \
                       -points1[i, 1] * points2[i, 1]

    B = B.flatten().reshape(-1, 1)  # flatten and reshape to be one column for dimension suitability

    H = np.linalg.lstsq(A, B, rcond=None)[0]  # returns H

    H = np.append(H, 1)  # puts 1 at the end of H

    H = np.reshape(H, [3, 3])  # return H as matrix of shape 3x3
    return H


def inverse_transform(h, point):
    "for a point in second image gets its correspondence in first image"

    inverse_point = np.dot(np.linalg.inv(h), point);  # matrix multiplication with the inverse of H
    inverse_point[0] /= inverse_point[2]  # divides by weight
    inverse_point[1] /= inverse_point[2]
    return inverse_point[0:2]


def transform(h, point):
    "for a point in first image gets its correspondence in second image "
    corr_point = np.dot(h, point);
    corr_point[0] /= corr_point[2];
    corr_point[1] /= corr_point[2]
    return corr_point[0:2]


def convert_to_non_homogenous(points):
    "converts homogoneous representation of a point to a non-homo representation"

    points[:, 0] /= points[:, 2]
    points[:, 1] /= points[:, 2]

    return points[:, 0:2]
