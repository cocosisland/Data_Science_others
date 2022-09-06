import numpy as np
import tensorflow as tf
import tensorflow_addons as tfa
from tensorflow.keras.metrics import Recall, AUC, Precision
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from keras.regularizers import l2
from tensorflow.keras import backend as K, callbacks

# the input to every LSTM layer must be 3D (input_shape=), we can give a tuple


class My_LSTM:
    
    def __init__(self, x_train, y_train, x_val, y_val, x_test, y_test):
        self.x_train = x_train
        self.y_train = y_train
        self.x_val = x_val
        self.y_val = y_val
        self.x_test = x_test
        self.y_test = y_test
        
    
     
    def binary_focal_loss(self, gamma=2., alpha=.25):
        pass  


     
    def data_preparation(self, x_train, y_train, x_val, y_val, BUFFER_SIZE, BATCH_SIZE):
        pass
        
        
    def optimization(self, learning_rate):    
        pass       
        
        
    def LSTM_block2(self):
        
        model = Sequential()
        pass 



    def model_configs(self):
        pass



    def model_train(self, train_data_single, val_data_single, config, eval_interval=200):  # eval_interval is the nb of batches i.e. steps for 1 epoch
        
        epochs, batches, lr_adam = config
        
        model = self.LSTM_block2()
        
        optimizer = self.optimization(learning_rate=lr_adam)
        
        # METRICS
        focal1 = self.binary_focal_loss(gamma=2., alpha=.25)       
        recall = tf.keras.metrics.Recall()        
        f1 = tfa.metrics.F1Score(num_classes=3, threshold=0.5)

        
        # EARLY STOPPING
        # This callback will stop the training when there is no improvement in the val_f1_score for 20 consecutive epochs
        callback = callbacks.EarlyStopping(patience=100, verbose=2, restore_best_weights=True)
           
        
        # MODEL COMPILE
        model.compile(optimizer=optimizer, loss=focal1, metrics=[recall, f1])
        
    
        # MODEL FIT
        one_step_history = model.fit(train_data_single, epochs=epochs,
                                                    steps_per_epoch=eval_interval,
                                                    callbacks=[callback],
                                                    validation_data=val_data_single,
                                                    validation_steps=200)
        
        #print(one_step_history.history.keys())  
        # print-> dict_keys(['loss', 'recall', 'f1_score', 'val_loss', 'val_recall', 'val_f1_score'])
        
        # RESULTS FOR ONE STEP :
        try :
            list_val_recall = one_step_history.history['val_recall']
            step_val_recall = np.mean(list_val_recall[-3:])
            
            list_val_f1 = one_step_history.history['val_f1_score']
            step_val_f1 = np.mean(list_val_f1[-3:])
                  
        except : 
            best_loss = 1
        
        #saved_model=load_model('best_model.h5')
        
        return(model, one_step_history, step_val_recall, step_val_f1)



    def train_grid_search(self):
        
        (...)
            
            # DATA PREPARATION
            train_data_single, val_data_single  =  self.data_preparation(...)
            
            # TRAIN THE MODEL
            model, history, step_val_recall, step_val_f1  =  self.model_train(...)
            
    
            # EVALUATE THE MODEL on the test data
            print("Evaluate on test data")
            scores = model.evaluate(...)
            print("test loss, test acc:", scores)
            

            # SAVE MODEL and architecture to single file
            model.save("model.h5")
            print("Saved model to disk")            
            
            (...)
            
        print(f'Best Recall on Validation : {hist_val_recall}')
        print(f'Best F1-Score on Validation : {hist_val_f1}')
        print(f'Best parameters [batches, epochs, regularization, learning-rate] : {best_params}')
        
        return(hist_val_recall, best_params, best_model, history_best)
