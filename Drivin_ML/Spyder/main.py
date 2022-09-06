import numpy as np
import pandas as pd
import glob
import IPython.display as ipd   # beep

from dispatch_1 import Dispatch
from cleanfiles_2 import Files_Processing
from dataprocessing_3 import Data_Processing
from ML_datapreprocessing_4 import ML_Data_preprocessing
from modeltrain_5 import My_LSTM
from result_6 import Score


# FILL IN - define paths, raw data location, processed data destination, new folders creation
base_path = 'C:/...../'
mainfolder = 'mainfolder_name'
drivers_bag_dirname = 'dir_created/'
bag_path = base_path + mainfolder + drivers_bag_dirname
raw_data_location = base_path + 'raw_data_loc_name'
data_paths_list = [raw_data_location+'NORMAL', raw_data_location+'DROWSY', raw_data_location+'AGGRESSIVE']
data_path_for_ML = base_path+mainfolder+'data'



def data_read_df(data_path_for_ML):
    
    bag = glob.glob(data_path_for_ML + '/*.csv')        
    df_list = []
    np.random.shuffle(bag)
    for minifile in bag:
        df0 = pd.read_csv(minifile)
        df0.reset_index(drop=True, inplace=True)
        df_list.append(df0)
    df = pd.concat(df_list)
    df.reset_index(drop=True, inplace=True)
    return df



# STEP : RAW DATA CLEANING - GENERATE NEW FOLDERS CONTAINING CLEANED DATA
def main_cleaning():
  
    # Dispatch Drivers' data from original folders to DriverX folders located in drivers_bag_dirname (path)
    di = Dispatch()    
    di.create(base_path, mainfolder, drivers_bag_dirname)  
    di.dispatch_Drivers(base_path, data_paths_list, bag_path)
    print(f'Dispatching done - inside folder {mainfolder}{drivers_bag_dirname}.')     
       
    fpr = Files_Processing(bag_path)    
    fpr.run_file_processing()
    print('Processings related to files done.')
    
    dpr = Data_Processing(base_path, mainfolder, bag_path)
    dpr.run_data_processing()
    print('Processings related to data done.')
    
    print(f'Files located in {mainfolder}data/ will be used for Machine Learning.')
    


# STEP : DATA PREPROCESSING AND MACHINE LEARNING - LSTM MODEL
def main_learning(df):
    
    # Data preprocessing for the Learning
    mlpr = ML_Data_preprocessing(df)
    mlpr.clean_df()
    train_list, test_list, val_list  =  mlpr.split_dataset(...)   # split dataset into train/test/validation sets
    df_train, df_test, df_val  =  mlpr.from_sets_to_df(train_list, test_list, val_list)   # make sets into Dataframes
    df_train_scaled, df_val_scaled, df_test_scaled  =  mlpr.scale_data(df_train, df_val, df_test)  # rescale

    # Reshape input data for LSTM
    x_train, y_train  =  mlpr.data_generating(...)
    x_test, y_test  =  mlpr.data_generating(...)
    x_val, y_val  =  mlpr.data_generating(...)
    print(f'x_train : {x_train.shape}   \ny_train : {y_train.shape}')
    print(f'x_test : {x_test.shape}   \ny_test : {y_test.shape}')
    print(f'x_val : {x_val.shape}   \ny_val : {y_val.shape}')

    # Define the model
    lstm = My_LSTM(x_train, y_train, x_val, y_val, x_test, y_test)
    
    # RUN THE MODEL OR GRIDSEARCH
    print('START TRAINING THE MODEL ----------------------')
    Score, params, model, history  =  lstm.train_grid_search()
    ipd.Audio("https://www.soundjay.com/misc/sounds/censor-beep-3.mp3", rate=10000, autoplay=True)



# FINAL STEP : SCORING
def main_scoring() :
    
    sc = Scoring()
    model = sc.load_model()
    sc.read_test_dataset(model)



# Call the cleaning/learning/scoring steps - comment them out if you want to skip any step or go step by step 
if __name__ == "__main__":
    
    main_cleaning()

    df = data_read_df(data_path_for_ML)
    print(df)
    
    main_learning(df)
    
    main_scoring()