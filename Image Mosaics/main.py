import mosaic_builder

if __name__== "__main__":
    path = [[]] * int(2)
    path[0] = "images"
    #path[1] = "towers"
    for i in range(2):
        mosaic_builder.construct_mosaic(path[i]+"/img1.jpg", path[i]+"/img2.jpg", mosaic_builder.CORRESPONDENCE_MANUAL, mosaic_builder.CALCULATE_H_RANSAC,10)
        mosaic_builder.construct_mosaic(path[i]+"/img1.jpg", path[i]+"/img2.jpg", mosaic_builder.CORRESPONDENCE_AUT0, mosaic_builder.CALCULATE_H_RANSAC, 100)
        mosaic_builder.construct_mosaic(path[i]+"/img1.jpg", path[i]+"/img2.jpg", mosaic_builder.CORRESPONDENCE_AUT0, mosaic_builder.CALCULATE_H_RANSAC, 1000)
        mosaic_builder.construct_mosaic(path[i]+"/img1.jpg", path[i]+"/img2.jpg", mosaic_builder.CORRESPONDENCE_AUT0, mosaic_builder.CALCULATE_H_RANSAC, 5000)
        mosaic_builder.construct_mosaic(path[i]+"/img1.jpg", path[i]+"/img2.jpg", mosaic_builder.CORRESPONDENCE_AUT0, mosaic_builder.CALCULATE_H_NORMALLY)

