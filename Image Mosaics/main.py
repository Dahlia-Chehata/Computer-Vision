import mosaic_builder

if __name__== "__main__":
    path = [[]] * int(2)
   # path[0] = "images"
    path[0] = "towers"
    for i in range(1):
         mosaic_builder.construct_mosaic(path[i]+"/img1.jpg", path[i]+"/img2.jpg", mosaic_builder.MANUAL_CORRESPONDENCE, mosaic_builder.RANSAC_H,10)
        # mosaic_builder.construct_mosaic(path[i]+"/img1.jpg", path[i]+"/img2.jpg", mosaic_builder.AUTO_CORRESPONDENCE, mosaic_builder.RANSAC_H, 100)
        # mosaic_builder.construct_mosaic(path[i]+"/img1.jpg", path[i]+"/img2.jpg", mosaic_builder.AUTO_CORRESPONDENCE, mosaic_builder.RANSAC_H, 1000)
        # mosaic_builder.construct_mosaic(path[i]+"/img1.jpg", path[i]+"/img2.jpg", mosaic_builder.AUTO_CORRESPONDENCE, mosaic_builder.RANSAC_H, 5000)
        # mosaic_builder.construct_mosaic(path[i]+"/img1.jpg", path[i]+"/img2.jpg", mosaic_builder.AUTO_CORRESPONDENCE, mosaic_builder.NORMAL_H)

