import os
from osgeo import gdal, osr

def create_training_folders(TRAINING_PATH):
    # Creating folders
    try:
        folders = ['train_frames', 'train_masks', 'val_frames', 'val_masks', 'test_frames', 'test_masks']
        for folder in folders:
            os.makedirs(TRAINING_PATH + folder)
    except:
        pass
    
# CLIP ALL THE BANDS INTO ONE FILE
def clip_image(input_path, output_path,image_name):
    red = gdal.Open(input_path + image_name + '_BAND13_GRID_SURFACE.tif')
    green = gdal.Open(input_path + image_name + '_BAND14_GRID_SURFACE.tif')
    blue = gdal.Open(input_path + image_name + '_BAND15_GRID_SURFACE.tif')
    nir = gdal.Open(input_path + image_name + '_BAND16_GRID_SURFACE.tif')
    #Create the .vrt from RGBN
    array = [red, green, blue,nir]#adicionar o nir
    #array = [red, green, nir]#adicionar o blue
    opt = gdal.BuildVRTOptions(srcNodata=-9999, VRTNodata=-9999,separate=True,resampleAlg='nearest')
    print(VRT_DATA_DIR + image_name +'.vrt')
    vrt_clip = gdal.BuildVRT(VRT_DATA_DIR + image_name +'.vrt', array, options=opt)
    #Translate the .vrt to .tif
    trans_opt = gdal.TranslateOptions(format="tif", outputType=gdal.gdalconst.GDT_Unknown, 
                                  bandList=[1,2,3],width=0, height=0, widthPct=0.0, 
                                  heightPct=0.0, xRes=0.0, yRes=0.0,noData=-9999)
    #Clip da imagem
    gdal.Translate(output_path + image_name +'_rgbn.tif', vrt_clip)
    #Apaga o vrt
    #os.remove(VRT_DATA_DIR + image_name +'.vrt') 
    return True
    