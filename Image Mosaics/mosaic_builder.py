import cv2 as cv
import get_correspondences as corsp
import Homography
import RANSAC
import warping

AUTO_CORRESPONDENCE = 0
MANUAL_CORRESPONDENCE = 1
NORMAL_H = 0
RANSAC_H = 1

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
    if (correspondance_method == AUTO_CORRESPONDENCE):
        p1, p2 = corsp.auto_correspondence(image1_gray, image2_gray)
        corr_method_string = "automatic correspondence"
    else:
        p1, p2 = corsp.manual_correspondence(image1, image2, 8)
        corr_method_string = "manual correspondence"

    new_filename = new_filename + "_" + corr_method_string

    if (H_calculation_method == NORMAL_H):

        H = Homography.calculate_homography(p1[0:90], p2[0:90])
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