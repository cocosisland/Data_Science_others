import os 
import pandas as pd
pd.set_option("display.max_columns", None)
import numpy as np
import glob
import sys
print('geopandas' in sys.modules)
import shutil

from slicing_1 import Slicing
from addinfos_2 import AddTripinfos

    
# collect the files in the folder and make a unique dataframe
def files_into_dataframe(bag, files_nb=False):
    
    df_list = []
    #for file in bag[:files_nb]:
    for file in bag:
        df0 = pd.read_csv(file, sep=',')
        df0.reset_index(drop=True, inplace=True)
        df_list.append(df0)
        df = pd.concat(df_list)
        df.reset_index(drop=True, inplace=True)   
        
    return df

    
# create folder in given path where we will stock processed files
def create_dir(path, dirname):
    if os.path.exists(path + dirname):
        shutil.rmtree(path + dirname)
    os.mkdir(path + dirname) 
        
    #if not os.path.exists(dirname):   # +sur pour eviter override du dossier
        #os.mkdir(path + dirname) 
            
            

if __name__ == "__main__":
       
    single_raw_file = True    # set to True or False at will whether we wanna consider aaalll the raw files or not
    
    global step    # resampling : keep data every X step 
    step = 2
    
    if single_raw_file:
                        
        # ***** PROCESS ONE SPECIFIC RAW FILE THAT CONTAINS SEVERAL VEHICLE ID AND TRIP ID AND CREATE ONE FILE PER TRIP *****
        
        file = 'C:/.../171129_week.csv'
        df = pd.read_csv(file)
        
        # # create empty folder in specific path where we can put processed files inside it
        path = 'C:/...'
        dirname = 'data_processed'
        create_dir(path, dirname)         
        
        # STEP 1 : call all the functions to create .csv file for each trip
        sc = Slicing(df, step)
        sc.slice_into_trips()    # ------------------------------------------------------------------------------ call 1   
        
        
        # ***** PROCESS EACH FILE THAT HAS BEEN PREVIOUSLY CUT INTO INDIVIDUAL TRIP *****
          
        path_to_data = 'C:/...'              
        bag = glob.glob(path_to_data + '*.csv')
        list_dictionaries = []
        for file in bag:            
            df1 = pd.read_csv(file, sep=',')

            # STEP 2 : call all the functions to calculate for each file : trip timelength, mean speed, mean accel
            # further later : trip length in km, time spent for each roadtype
            # and make a unique .csv gathering all the infos of the trips, one trip per line
            tp = AddTripinfos(df1)
            dico_infos_singletrip = tp.trip_infos_calculus(step)    # ------------------------------------------- call 3
            list_dictionaries.append(dico_infos_singletrip)
        list_dictionaries.reverse()    # reorganize saving order of VehIds
        df_FINAL = pd.DataFrame(list_dictionaries)
        print(df_FINAL)
        path = 'C:/.../'
        dirname = 'data_FINAL'
        create_dir(path, dirname)
        df_FINAL.to_csv(os.path.join(path+dirname, "trips_information.csv"))
                  

    
    # TODO - TO TAKE INTO ACCOUNT ALL THE RAW FILES    
    else:
        
        bag = glob.glob('C:/.../*.csv')
    
        df = files_into_dataframe(bag, 3)
    
        # https://stackoverflow.com/questions/57507832/unable-to-allocate-array-with-shape-and-data-type
        
 

    