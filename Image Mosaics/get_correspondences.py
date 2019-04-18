import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
from numpy.linalg import inv
from scipy.interpolate import RectBivariateSpline as interpolate


from PIL import Image;

def get_correspondance_auto(image1_gray, image2_gray):
    "get coresspondance points between two given images by sift"
    orb = cv.ORB_create()
    kp1, des1 = orb.detectAndCompute(image1_gray, None)  # keypoints and descriptors of first image
    kp2, des2 = orb.detectAndCompute(image2_gray, None)

    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)  # creates a matcher

    # Match descriptors.
    matches = bf.match(des1, des2)  # matches the two descriptors
    matches = sorted(matches, key=lambda x: x.distance)  # sorts matches where best matcvhes come first

    p = []  # list of correspondance point in first image
    p_ = []  # list of correspondance point in second image

    for match in matches:  # loop on matches and fills p and p_
        index1 = match.queryIdx
        p.append((int(kp1[index1].pt[0]), int(kp1[index1].pt[1])))

        index2 = match.trainIdx
        p_.append((int(kp2[index2].pt[0]), int(kp2[index2].pt[1])))

    # matchImg = cv.drawMatches(image1_gray,kp1,image2_gray,kp2,matches[0:20],image2_gray) #draws the best 20 matches on the image and saves it as output image
    # cv.imwrite('Matches.png', matchImg)

    p = np.array(p)
    p_ = np.array(p_)
    return p, p_


def get_correspondance_manually(image1, image2, number_of_points):
    # Display images, select matching points
    fig = plt.figure()
    figA = fig.add_subplot(1, 2, 1)
    figB = fig.add_subplot(1, 2, 2)
    # Display the image
    # lower use to flip the image
    figA.imshow(image1)  # ,origin='lower')
    figB.imshow(image2)  # ,origin='lower')
    plt.axis('image')
    # n = number of points to read
    p1 = np.zeros([(number_of_points // 2), 2])
    p2 = np.zeros([number_of_points // 2, 2])
    pts = plt.ginput(n=number_of_points, timeout=0)
    p1_itr = 0
    p2_itr = 0
    for i in range(0, number_of_points):
        if (i % 2 == 0):
            p1[p1_itr] = pts[i]
            print("p1 of index ", p1_itr, " is ", pts[i])
            p1_itr += 1

        else:
            p2[p2_itr] = pts[i]
            print("p2 of index ", p2_itr, " is ", pts[i])
            p2_itr += 1
    return p1, p2