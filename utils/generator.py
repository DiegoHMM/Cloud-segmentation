from sklearn import preprocessing
import os
import numpy as np
from osgeo import gdal, osr
import tensorflow as tf
import random

def data_gen(img_folder, mask_folder, batch_size,DIMENSION,BANDS):
    c = 0
    n = os.listdir(img_folder) #List of training images
    random.shuffle(n)
    while(True):
        img = np.zeros((batch_size, DIMENSION, DIMENSION, BANDS)).astype('float')
        mask = np.zeros((batch_size, DIMENSION, DIMENSION, 1)).astype('float')

        for i in range(c, c + batch_size): #initially from 0 to 16, c = 0. 
            train_img = gdal.Open(img_folder+'/'+n[i]).ReadAsArray()
            train_img = tf.convert_to_tensor(train_img.transpose((1,2,0)))
            img[i-c] = train_img #add to array - img[0], img[1], and so on.

            
            train_mask = gdal.Open(mask_folder+'/'+n[i]).ReadAsArray()
            train_mask = train_mask/1
            train_mask = resize_img(train_mask,DIMENSION,DIMENSION,1)
            train_mask = np.expand_dims(train_mask, axis=2)
            train_mask = tf.convert_to_tensor(train_mask)
            
            mask[i-c] = train_mask

        c += batch_size
        
        if(c + batch_size >= len(os.listdir(img_folder))):
            c=0
            random.shuffle(n)
                      # print "randomizing again"
        
        yield img, mask
        
