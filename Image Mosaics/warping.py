import numpy as np
import Homography


def warp(source_image, dest_image, h):
    "aligns the two images"
    source_height = source_image.shape[0]
    source_width = source_image.shape[1]
    # array containing corner points of source image
    source_edges = np.array([[0, 0], [source_width - 1, 0], [0, source_height - 1], [source_width - 1, source_height - 1]])
    # pad 1 to make it homogoneous representation
    source_edges = np.pad(source_edges, (0, 1), 'constant',constant_values=1)
    # remove a redundant row from padding
    source_edges = source_edges[:-1]
    # get the points corresponding to edges in non-homogeneous form each row is a point and each column is x or y
    corr_source_edges = Homography.convert_to_non_homogenous(np.dot(h,source_edges.T).T)


    # get the corresponding positions of the corner points
    max_mapped_i, max_mapped_j = int(np.ndarray.max(corr_source_edges[:, 1], axis=0)), int(
        np.ndarray.max(corr_source_edges[:, 0], axis=0))
    min_mapped_i, min_mapped_j = int(np.ndarray.min(corr_source_edges[:, 1], axis=0)), int(
        np.ndarray.min(corr_source_edges[:, 0], axis=0))

    # gets the size of source image after warping
    mapped_source_height = max_mapped_i - min_mapped_i + 1
    mapped_source_width = max_mapped_j - min_mapped_j + 1

    # determines the shift that happens to the second image
    shiftHeight = -min_mapped_i
    shiftWidth = - min_mapped_j

    # new image containing the first image after warping
    mapped_source_image = np.zeros((mapped_source_height, mapped_source_width, 3), dtype=np.uint8);

    # forward warping
    for i in range(0, source_height):
        for j in range(0, source_width):
            mapped_position = Homography.transform(h, np.array([j, i, 1]))
            mapped_j = int(mapped_position[0])
            mapped_i = int(mapped_position[1])

            mapped_source_image[mapped_i + shiftHeight][mapped_j + shiftWidth] = source_image[i][j];

    # save forward warped image
    # the resulting image contains holes
    ###cv.imwrite("with holes.png",mapped_source_image)
    # inverse warping to remove holes
    for i in range(0, mapped_source_height):
        for j in range(0, mapped_source_width):
            # check if pixel is black
            if (int(mapped_source_image[i][j][0]) == 0 and int(mapped_source_image[i][j][1]) == 0 and int(
                    mapped_source_image[i][j][2]) == 0):

                inverse_mapped_position = Homography.inverse_transform(h, np.array([j - shiftWidth, i - shiftHeight, 1]))
                inverse_mapped_i = inverse_mapped_position[1]
                inverse_mapped_j = inverse_mapped_position[0]
                if inverse_mapped_i <= source_height - 1 and inverse_mapped_i >= 0 and inverse_mapped_j <= source_width - 1 and inverse_mapped_j >= 0:
                    # interpolate
                    low_i = int(inverse_mapped_i);
                    low_j = int(inverse_mapped_j);
                    idistance = inverse_mapped_i - low_i;
                    jdistace = inverse_mapped_j - low_j;

                    # interpolation for each channel
                    mapped_source_image[i][j][0] = (1 - idistance) * (1 - jdistace) * source_image[low_i][low_j][0] + (
                                1 - idistance) * (jdistace) * source_image[low_i][low_j + 1][0] + (idistance) * (
                                                               1 - jdistace) * source_image[low_i + 1][low_j][0] + (
                                                       idistance) * (jdistace) * source_image[low_i + 1][low_j + 1][0]
                    mapped_source_image[i][j][1] = (1 - idistance) * (1 - jdistace) * source_image[low_i][low_j][1] + (
                                1 - idistance) * (jdistace) * source_image[low_i][low_j + 1][1] + (idistance) * (
                                                               1 - jdistace) * source_image[low_i + 1][low_j][1] + (
                                                       idistance) * (jdistace) * source_image[low_i + 1][low_j + 1][1]
                    mapped_source_image[i][j][2] = (1 - idistance) * (1 - jdistace) * source_image[low_i][low_j][2] + (
                                1 - idistance) * (jdistace) * source_image[low_i][low_j + 1][2] + (idistance) * (
                                                               1 - jdistace) * source_image[low_i + 1][low_j][2] + (
                                                       idistance) * (jdistace) * source_image[low_i + 1][low_j + 1][2]

    # writes image after inverse warping
    ###cv.imwrite("without holes.png",mapped_source_image)

    dest_image_height = dest_image.shape[0]
    dest_image_width = dest_image.shape[1]

    # get dimensions for the new image
    mosaic_image_height = max(mapped_source_height, dest_image_height + shiftHeight)
    mosaic_image_width = max(mapped_source_width, dest_image_width + shiftWidth)

    mosaic_image = np.zeros((mosaic_image_height, mosaic_image_width, 3), dtype=np.uint8);

    # put the second image in the mosaic image
    for i in range(0, dest_image_height):
        for j in range(0, dest_image_width):
            mosaic_image[i + shiftHeight][j + shiftWidth] = dest_image[i][j]

    # puts the first image in mosaic image
    for i in range(0, mapped_source_image.shape[0]):
        for j in range(0, mapped_source_image.shape[1]):
            if not (int(mapped_source_image[i][j][0]) == 0 and int(mapped_source_image[i][j][1]) == 0 and int(
                    mapped_source_image[i][j][2]) == 0):
                mosaic_image[i][j] = mapped_source_image[i][j]

    return mosaic_image
