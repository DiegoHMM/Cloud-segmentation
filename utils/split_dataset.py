import os
import random
import shutil

def move_files(source_dir,files_list,output_dir):
    for file_name in files_list:
        shutil.copy(os.path.join(source_dir, file_name), output_dir+file_name)
        
def split_dataset(SUBSCENES_DIR,SUBMASKS_DIR,TRAINING_DIR):
    #Split dataset files
    all_frames = os.listdir(SUBSCENES_DIR)
    random.seed(12)
    random.shuffle(all_frames)

    train_size = int(0.7 * len(all_frames))
    val_size = int(0.25 * len(all_frames))
    test_size = int(0.5 * len(all_frames))


    train_scene = all_frames[:train_size]
    val_scene = all_frames[train_size:train_size+val_size]
    test_scene = val_subscenes = all_frames[train_size+val_size:]

    # Generate corresponding mask lists for masks
    train_masks_list = [f for f in all_frames if f in train_scene]
    val_masks_list = [f for f in all_frames if f in val_scene]
    test_masks_list = [f for f in all_frames if f in test_scene]

    try:
        #Move files to correspondent directory
        move_files(SUBSCENES_DIR,train_scene,TRAINING_DIR+'train_frames/')
        move_files(SUBSCENES_DIR,val_scene,TRAINING_DIR+'val_frames/')
        move_files(SUBSCENES_DIR,test_scene,TRAINING_DIR+'test_frames/')


        move_files(SUBMASKS_DIR,train_masks_list,TRAINING_DIR+'train_masks/')
        move_files(SUBMASKS_DIR,val_masks_list,TRAINING_DIR+'val_masks/')
        move_files(SUBMASKS_DIR,test_masks_list,TRAINING_DIR+'test_masks/')
    except Exception as e:
        print(e)