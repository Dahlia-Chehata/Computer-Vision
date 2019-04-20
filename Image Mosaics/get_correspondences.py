import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv


def auto_correspondence(image1,image2):

    ' get coresspondance points between two given images using (oriented BRIEF) keypoint detector and descriptor extractor'
    ' better than SIFT descriptors'

    orb = cv.ORB_create()
    keypoint1, descriptor1 = orb.detectAndCompute(image1, None)
    keypoint2, descriptor2 = orb.detectAndCompute(image2, None)

    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)  # creates a matcher

    # Match descriptors.
    matches = bf.match(descriptor1, descriptor2)  # matches the two descriptors
    matches = sorted(matches, key=lambda x: x.distance)  # sort matches where best matches come first

    points1 = []  # list of correspondence points in first image
    points2 = []  # list of correspondence points in second image

    # loop on matches and fills  points1  and points2
    for match in matches:
        index1 = match.queryIdx
        points1 .append((int(keypoint1[index1].pt[0]), int(keypoint1[index1].pt[1])))
        index2 = match.trainIdx
        points2.append((int(keypoint2[index2].pt[0]), int(keypoint2[index2].pt[1])))

    points1 = np.array(points1)
    points2 = np.array(points2)
    return points1, points2


def manual_correspondence(image1, image2, number_of_points):
    " Display images and select matching points "
    fig = plt.figure()
    fig1 = fig.add_subplot(1, 2, 1)
    fig2 = fig.add_subplot(1, 2, 2)

    # Display the image
    # to flip the image : #, origin='lower'
    fig1.imshow(image1)
    fig2.imshow(image2)
    plt.axis('image')

    p1 = np.zeros([(number_of_points // 2), 2])
    p2 = np.zeros([number_of_points // 2, 2])
    pts = plt.ginput(n=number_of_points, timeout=0)
    p1_itr = 0
    p2_itr = 0
    for i in range(0, number_of_points):
        if i % 2 == 0:
            p1[p1_itr] = pts[i]
            print("p1 of index ", p1_itr, " is ", pts[i])
            p1_itr += 1

        else:
            p2[p2_itr] = pts[i]
            print("p2 of index ", p2_itr, " is ", pts[i])
            p2_itr += 1
    return p1, p2