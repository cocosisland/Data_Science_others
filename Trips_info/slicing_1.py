import pandas as pd

from add_infos_2 import AddRoadinfos


class Slicing:
    
    def __init__(self, df, step):
        self.df = df
        self.step = step
        
        
    def resampling(self, df):        
        df = df.iloc[::self.step]
        #df.reset_index(drop=True, inplace=True)
        return df    
        
                        
    # df : ici le DF global, contenant l'ensemble des VehId et des Trips
    def slice_into_trips(self):
        
        self.df.drop(columns = ['Absolute Load[%]','Long Term Fuel Trim Bank 1[%]','Long Term Fuel Trim Bank 2[%]',\
                           'Short Term Fuel Trim Bank 1[%]','Short Term Fuel Trim Bank 2[%]','Fuel Rate[L/hr]',\
                               'Air Conditioning Power[kW]','Heater Power[Watts]','HV Battery Current[A]', 'HV Battery SOC[%]',\
                                   'HV Battery Voltage[V]','OAT[DegC]','Air Conditioning Power[Watts]'], inplace=True)    
    
        self.df.reset_index(drop=True, inplace=True)
        
        nb_vehic = self.df['VehId'].value_counts()
        print(f'Nombre de vehicules differents pour notre etude : {len(nb_vehic)}')
    
    
        # Separate each VehID data into different dataframes
        d_vehid = {}
        for i in self.df['VehId'].unique():
            d_vehid[i] = pd.DataFrame(self.df.loc[self.df['VehId'] == i])
            d_vehid[i].reset_index(drop=True, inplace=True)
            
        # Separate each Trip data into different dataframes - one VehId often has several Trips
        # It sometimes happen that different drivers share a same trip name. They need to be differenciated
        d_trip = {}
        for j in d_vehid:
            for k in self.df.loc[self.df['VehId']==j, 'Trip'].unique():
                tripname = str(j)+"_"+str(k)
                d_trip[tripname] = self.df.loc[(self.df['VehId'] == j) & (self.df['Trip'] == k)]
                d_trip[tripname].reset_index(drop=True, inplace=True)    
        
                # resample every 'step' lines
                df_trip_resampled = self.resampling(d_trip[tripname])
                
                               
                # call the fonctions that add wanted columns for each trip
                rd = AddRoadinfos(df_trip_resampled, tripname)
                rd.add_cols_address_roadtype()    # ------------------------------------------------------------- call 2
        
        
        # HERE WE HAVE A DICTIONARY HAVING : Keys are trip names, Values are their dataframe
