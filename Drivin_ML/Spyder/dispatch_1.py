import os 
from distutils.dir_util import copy_tree


class Dispatch:
    
    def __init__(self):
        print("--- Start dispatching Drivers' data from original folders to DriverX folders located in bag_location (path) ---")
        
    
    def create_dir(self, path, dirname):
        if not os.path.exists(dirname):
            os.mkdir(path + dirname)    
    

    def create(self, base_path, mainfolder, drivers_dirname): 
        self.create_dir(base_path, mainfolder)    
        drivers_path = base_path + mainfolder
        self.create_dir(drivers_path, drivers_dirname)
    
    
    def dispatch_Drivers(self, base_path, data_paths_list, bag_path):    
        for path in data_paths_list:
            for sub in os.listdir(path):    
                for i in range(6):
                    if "D"+str(i+1) in sub:
                        source = path+"/"+sub
                        path_newfo = os.path.join(bag_path, 'Driver'+str(i+1))
                        
                        if not os.path.exists(path_newfo):
                            os.mkdir(path_newfo)
                        
                        if not os.path.exists(os.path.join(path_newfo, sub)):
                            os.mkdir(os.path.join(path_newfo, sub))
    
                        copy_tree(source, os.path.join(path_newfo, sub))



   