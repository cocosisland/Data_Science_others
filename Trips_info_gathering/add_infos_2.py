import os 
import numpy as np
from geopy.geocoders import Nominatim
from geopy.point import Point         # for reverse geocoding
import pprint

from nlp_3 import NLP


# ici ca process 1 fichier (i.e. 1 trip)
class AddRoadinfos:

    
    def __init__(self, df, tripname):
        self.df = df
        self.tripname = tripname

    # we pass if the coordinates does not have the specific key (called from process_trips())
    def test_key_existence(self, rec, key, subkey):
        if subkey in rec[key]:
            #print(rec[key][subkey])
            return True 

                
    def add_cols_address_roadtype(self):             
           
        geolocator = Nominatim(user_agent='haha')
        
        # for each different trip we keep the coord every 12 sec

        s_lat = self.df['Latitude[deg]']   # latitude is a float
        s_lon = self.df['Longitude[deg]']  
        s_idx = self.df.index.to_series()
        print(f'Nb of lines of trip DF that has been resampled : {len(s_idx)}')
    
        global list_returned_roads_all
        list_returned_roads_all = []    
    
        # if key "road" is missing for one of the coordinates, pass to the next line
    
            (...)

                # save each trip into a .csv
                path = 'C:/.../'
                dirname = 'data_processed'
                self.df.to_csv(os.path.join(path+dirname, f"{self.tripname}.csv"))   # ----------------------- CSV per Trips
        
            else:
                pass  
            


class AddTripinfos:


    def __init__(self, df):
        self.df = df
        
       
    # INFORMATION BY TRIP 
    def trip_infos_calculus(self, step):
       
        list_single_trip_infos = []
        # VEHID AND TRIP NAMES
        vehid = self.df.loc[1, 'VehId']
        trip = self.df.loc[1, 'Trip']
        list_single_trip_infos.append(vehid)
        list_single_trip_infos.append(trip)
        
        
        # MEAN OF SPEEDS - km/h and m/sec
        speed_mean_H = ...
        list_single_trip_infos.append(speed_mean_H)  
        
        self.df['Vehicle Speed[m/s]'] = ...
        speed_mean_SEC = ...
        list_single_trip_infos.append(speed_mean_SEC)

        
        # TIMELENGTH    
        # to get the timelength of the trip, calculate : last timestamp - first timestamp
        self.df['Timestamp(s)'] = ...
        trip_timelength = ...
        list_single_trip_infos.append(round(trip_timelength))

        
        # MEAN OF ACCELERATIONS
        self.df['Accel'] =...
        accel_mean = ...
        list_single_trip_infos.append(accel_mean)

        
        # TIME SPENT PER ROADTYPE - ROUGH VERSION
        # roadtypes_counts = self.df['Road_type'].value_counts()
        # print(roadtypes_counts)
        # time_spent_each_roadtype = roadtypes_counts*step
        # print(dict(time_spent_each_roadtype))
            
        # TIME SPENT PER ROADTYPE - FINE VERSION
        self.df['Road_type'] = ...
        self.df["sum_bool"] = ...
        df_t = ...
                  
        df_t['Timespent_roadname'] = ...       
        self.df = ...

        # put into .csv to check if everything worked correctly            
        path = 'C:/.../'
        dirname = 'data_processed'
        self.df.to_csv(os.path.join(path+dirname, "tst.csv")) 
        
        grouped_0 = (self.df.groupby(['sum_bool'], as_index=False).agg(**{'Last roadtype':('Road_type', 'last'),
                                                                'Last timespent': ('Timespent_roadname', 'last')}))   

        grouped_1 = grouped_0.groupby('Last roadtype', as_index=False).agg({'Last timespent': sum}).round()
        dico_t_per_roadtype = dict(zip(grouped_1['Last roadtype'], grouped_1['Last timespent']))   # df.cols into a dico
        dico_t_per_roadtype_SORTED = sorted(dico_t_per_roadtype.items(), key=lambda x: x[1], reverse=True)  #sort dico values
        list_single_trip_infos.append(dico_t_per_roadtype_SORTED)

        
        # ALL THE INFOS ABOUT THE SINGLE TRIP GATHERED INTO A LIST AND DICTIONARY  
        descriptions = ['VehId', 'Trip', 'Mean speed (km/h)', 'Mean speed (m/sec)', 'Trip timelength (sec)', 'Mean accel (m2.s-2)', \
                        'Time per roadtype (sec)']
        dict_almost_clean = dict(zip(descriptions, list_single_trip_infos))
        dict_clean = pprint.PrettyPrinter(indent=4)
        dict_clean.pprint(dict_almost_clean)
                            
        return dict_almost_clean
        
        