from keras.callbacks import ModelCheckpoint
from keras.callbacks import CSVLogger
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam


def config_hyper_parameters(weights_path, monitor, mode, min_delta, patience):
    checkpoint = ModelCheckpoint(weights_path, monitor='f1', 
                             verbose=1, save_best_only=True, mode='max')

    csv_logger = CSVLogger('D:/cbers_data/DataSetModelo/log.out', append=True, separator=';')

    earlystopping = EarlyStopping(monitor = 'f1', verbose = 1,
                                  min_delta = 0.01, patience = 5, mode = 'max')

    
    return [checkpoint, csv_logger, earlystopping]