from osgeo import gdal, osr
import cv2
import numpy as np

def normalize_scene(RAW_SCENES_LIST)
    driver = gdal.GetDriverByName('GTiff')
    for scene_name in RAW_SCENES_LIST:
        scene = gdal.Open(SCENES_DIR+scene_name)
        driver.Register()
        raster_X_size = scene.RasterXSize
        raster_Y_size = scene.RasterYSize
        gt = scene.GetGeoTransform()
        proj = scene.GetProjection()
        scene = scene.ReadAsArray()

        max_pixel_value = scene.max()
        min_pixel_value = scene.min()
        #min_pixel_value = 0
        scene = cv2.normalize(scene, scene, 0, 1, cv2.NORM_MINMAX, cv2.CV_32F)
        # Create new tif
        driver = gdal.GetDriverByName('GTiff')
        tif_file = driver.Create(NORMALIZED_DIR+scene_name, 
                                 raster_X_size, 
                                 raster_Y_size, 
                                 BANDS, 
                                 gdal.GDT_Float32)
        # Set metadata
        tif_file.SetGeoTransform(gt)
        tif_file.SetProjection(proj)
        # write numpy as tif
        for i in range(BANDS):
            outBand = tif_file.GetRasterBand(i + 1)
            outBand.WriteArray(scene[i])
            outBand.SetNoDataValue(-9999)
    del scene