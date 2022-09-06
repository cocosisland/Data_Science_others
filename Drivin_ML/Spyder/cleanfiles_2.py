import os 
import pandas as pd 
import glob


class Files_Processing:
           
    def __init__(self, bag_path):
        self.bag_path = bag_path
        

    # Select the features needed only
    def headers_list(self):
        
        headers_accel = ['timestamp', 'accel_x', ...]
        headers_gps = ['timestamp', 'speed_gps', 'latitude', 'longitude', ...]
        headers_streetmap = ['timestamp', 'max_allowed_speed', ...]  
        
        return headers_accel, headers_gps, headers_streetmap
    
    
    
    # Add the headers to the files and returns .csv + suppress unwanted columns    
    def add_headers(self, file):
        
        headers_accel, headers_gps, headers_streetmap = self.headers_list()
        
        if 'ACCEL' in file:
            df = pd.read_csv(file, delimiter=' ', header=None, usecols=range(10))
            df.columns = headers_accel
            df.reset_index(inplace=True)
            df.to_csv('accel.csv', index=None)
    
        elif 'GPS' in file:
            ...
            df.to_csv('gps.csv', index=None)
            
        elif 'OPENSTREETMAP' in file:
            ...
            df.to_csv('streetmap.csv', index=None)        
                    
        else:       
            print("Contains file that is neither ACCEL, GPS nor OPENSTREETMAP") 
            pass
             
    
    # Consider all the .txt files in the subfolder and add headers to each of them
    def returned_files_to_csv(self, camino):
        bag = glob.glob(camino+"/*.txt")      
        for file in bag:
            self.add_headers(file)
    

    
    def run_file_processing(self):
            
        os.chdir(self.bag_path)    # go to the right path
        #print("current directory: ", os.getcwd())
        
        for i in range(6):                  # loop through DriverX        
            os.chdir('Driver'+str(i+1))     # access the DriverX branch
            
            subdirs = [x[0] for x in os.walk(os.getcwd())]  # print only the subfolders of DriverX name and not their content
            for subdir in subdirs[1:]:                      # for each subfolder in DriverX
                os.chdir(subdir)
                camino = os.getcwd()
                self.returned_files_to_csv(camino)
                
            os.chdir(self.bag_path)
    
    
          