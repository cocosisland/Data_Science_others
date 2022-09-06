import os 
import pandas as pd 
import numpy as np
import glob
from functools import reduce
import datetime
import re



class Data_Processing:
           
    def __init__(self, base_path, mainfolder, bag_path):
        self.base_path = base_path
        self.mainfolder = mainfolder
        self.bag_path = bag_path



    # en fonction du fichier, ne sélectionne que les colonnes à garder au moment de la lecture (gain de mémoire etc)
    def keep_only_these_columns(self, filename):
        
        list_cols_keep = []
        if 'accel' in filename:
            #list_cols_keep = ['timestamp', 'accel_x', 'accel_y', 'accel_z']
            list_cols_keep = ['timestamp', 'accel_x_kf', 'accel_y_kf', 'accel_z_kf', 'roll', 'pitch', 'yaw']
                              
        if 'gps' in filename:
            list_cols_keep = ['timestamp', 'speed_gps', 'latitude', 'longitude']
            
        if 'streetmap' in filename:
            list_cols_keep = ['timestamp', 'max_allowed_speed', 'roadtype']
            
        return list_cols_keep
    

    
    def arrondir(self, filename):
        list_cols_keep = self.keep_only_these_columns(filename)
        df = pd.read_csv(filename, usecols=list_cols_keep)
        #df.reset_index(drop=True, inplace=True)
        df['timestamp_arrondi'] = np.floor(df['timestamp'])   # arrondi entier inférieur
        return df



    def run_data_processing(self):
        
        for i in range(6):
            # three_files contiendra des listes [accel,gps,streetmap] pour chaque trajet (subdir) du Driver
            three_files = {}
            os.chdir(self.bag_path + 'Driver'+str(i+1))
            subdirs = [x[0] for x in os.walk(os.getcwd())]  # print only the subfolders of DriverX name and not their content
            for subdir in subdirs[1:]:    # for each subfolder in DriverX
                os.chdir(subdir)
                bag = glob.glob('*.csv')
                bag = [b for b in bag if any(substr in b for substr in ['accel', 'gps', 'streetmap'])]
                for i, file in zip(list(range(3)), bag):
                    three_files[i] = self.arrondir(file)    
                    # pour avoir au final -> {[accel,gps,streetmap], [accel,gps,streetmap], [accel,gps,streetmap], ...}
    
                # dataframes de accel, gps et streetmap pour le trajet (subdir) en question
                df0 = three_files[0]
                df1 = three_files[1]
                df2 = three_files[2]
        
                # faire un merge des 3 dataframes selon leur colonne 'timestamp_arrondi' qu'ils ont en commun
                #df_list0 = [df0, df1, df2]
                df0_moy_timearrondis = df0.groupby('timestamp_arrondi').mean()
                df1_moy_timearrondis = df1.groupby('timestamp_arrondi').mean()
                df2_moy_timearrondis = df2.groupby('timestamp_arrondi').mean()
                df_list = [df0_moy_timearrondis, df1_moy_timearrondis, df2_moy_timearrondis]    
                df_merged = reduce(lambda left, right: pd.merge(left, right, on=['timestamp_arrondi'], how='outer'), df_list)
                df_merged = df_merged.reset_index(level=0)
            
                # créer nouvelle colonne contenant les labels
                basename = os.path.basename(subdir)
                if 'DROW' in basename:
                    df_merged['label'] = 0
                    
                if 'NORM' in basename:
                    df_merged['label'] = 1
                    
                if 'AGG' in basename:
                    df_merged['label'] = 2
                
                # find in filename consecutive numbers of minimum length=5 (ex° filename 20151110175712-16km-D1-NORMAL1-SECONDARY)
                # and make it as values of new column 'file_id'
                df_merged['file_id'] = re.findall("[0-9]{5,}", basename)[0]   #re.findall returns a list, thats why need the [0]
                       
                # créer nouvelle colonne avec timestamps sous format datetime (initialisé avec .min ? / à partir de 2020 ?)
                col_length = len(df_merged['label'])
                df_merged['ts'] = [datetime.datetime.now() + datetime.timedelta(seconds=1*x) for x in range(col_length)]
                
                # créer .csv pour chaque trajet   
                outdir_last = self.base_path + self.mainfolder + 'data/'
                
                if not os.path.exists(outdir_last):
                    os.mkdir(outdir_last)
                
                df_merged.to_csv(f"{basename}.csv")
                df_merged.to_csv(os.path.join(outdir_last, f"{basename}.csv"))
            os.chdir(self.bag_path) 
            
            
           