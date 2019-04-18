import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import get_correspondences as corsp
import Homography
import RANSAC
import warping

CORRESPONDENCE_AUT0 = 0
CORRESPONDENCE_MANUAL = 1
CALCULATE_H_NORMALLY = 0
CALCULATE_H_RANSAC = 1

def construct_mosaic(path1, path2, correspondance_method, H_calculation_method, ransac_loops=100):
    image1 = cv.imread(path1)
    image2 = cv.imread(path2)

    image1_gray = cv.cvtColor(image1, cv.COLOR_RGB2GRAY)
    image2_gray = cv.cvtColor(image2, cv.COLOR_RGB2GRAY)
    path1=path1.split("/")
    #path2=path2.split("/")
    new_filename = path1[0]+ "/result_"

    corr_method_string = ""
    H_method_string = ""
    if (correspondance_method == CORRESPONDENCE_AUT0):
        p1, p2 = corsp.get_correspondance_auto(image1_gray, image2_gray)
        corr_method_string = "automatic correspondence"
    else:
        p1, p2 = corsp.get_correspondance_manually(image1, image2, 8)
        corr_method_string = "manual correspondence"

    new_filename = new_filename + "_" + corr_method_string

    if (H_calculation_method == CALCULATE_H_NORMALLY):

        H = Homography.calculate_h(p1[0:90], p2[0:90])
        H_method_string = "H calcualated without ransac"


    else:
        H, inliners = RANSAC.ransac(p1, p2, 5, ransac_loops)
        H_method_string = "H calcualated with ransac"
        new_filename = new_filename + "_" + H_method_string + "_" + "ransacloops=" + str(ransac_loops)

    new_filename = new_filename + "_" + H_method_string

    mosaic_image = warping.warp(image1, image2, H)

    # writes the output
    cv.imwrite(new_filename + ".jpg", mosaic_image)
    print("writing " + new_filename + " image is done")