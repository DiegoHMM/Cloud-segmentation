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
    
    
def crop_scene(input_dir,output_dir,dimension):
    scenes_list = os.listdir(input_dir)
    for scene_name in scenes_list:
        scene = gdal.Open(input_dir+scene_name)
        gt = scene.GetGeoTransform()
        x_min = gt[0]
        y_max = gt[3]
        res = gt[1]
        num_img_x = scene.RasterXSize/dimension
        num_img_y = scene.RasterYSize/dimension
        x_len = res * scene.RasterXSize
        y_len = res * scene.RasterYSize
        x_size = x_len/num_img_x
        y_size = y_len/num_img_y

        x_steps = [x_min + x_size * i for i in range(int(num_img_x) + 1)]
        y_steps = [y_max - y_size * i for i in range(int(num_img_y) + 1)]
        index_img = 0
        for i in range(int(num_img_x)):
            for j in range(int(num_img_y)):
                x_min = x_steps[i]
                x_max = x_steps[i+1]
                y_max = y_steps[j]
                y_min = y_steps[j+1]
                index_img+=1
                scene_name = scene_name.replace('.tif','')
                gdal.Warp(output_dir + scene_name+ "_" + str(i)+ "_" +str(j)+'_'+str(index_img)+"_"+".tif", 
                      scene, 
                      outputBounds = (x_min,y_min,x_max, y_max), 
                      dstNodata = -9999)
def crop_mask(input_dir,output_dir,dimension):
    scenes_list = os.listdir(input_dir)
    for scene_name in scenes_list:
        scene = gdal.Open(input_dir+scene_name)
        gt = scene.GetGeoTransform()
        x_min = gt[0]
        y_max = gt[3]
        res = gt[1]
        num_img_x = scene.RasterXSize/dimension
        num_img_y = scene.RasterYSize/dimension
        x_len = res * scene.RasterXSize
        y_len = res * scene.RasterYSize
        x_size = x_len/num_img_x
        y_size = y_len/num_img_y

        x_steps = [x_min + x_size * i for i in range(int(num_img_x) + 1)]
        y_steps = [y_max - y_size * i for i in range(int(num_img_y) + 1)]
        index_img = 0
        for i in range(int(num_img_x)):
            for j in range(int(num_img_y)):
                x_min = x_steps[i]
                x_max = x_steps[i+1]
                y_max = y_steps[j]
                y_min = y_steps[j+1]
                index_img+=1
                gdal.Warp(output_dir + scene_name+ "_" + str(i)+ "_" +str(j)+'_'+str(index_img)+"_"+".tif", 
                      scene, 
                      outputBounds = (x_min,y_min,x_max, y_max), 
                      dstNodata = -9999)