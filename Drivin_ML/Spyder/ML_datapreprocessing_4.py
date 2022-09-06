import pandas as pd
import numpy as np
import random
import gc
from sklearn.preprocessing import StandardScaler


class ML_Data_preprocessing:

    
    def __init__(self, df):
        self.df = df


    def clean_df(self):

        self.df.drop(columns=['Unnamed: 0', 'timestamp_arrondi', 'timestamp_x', 'timestamp_y', 'latitude', 'longitude',
                              'timestamp', 'max_allowed_speed'], inplace=True)
        # df1['ts'] = pd.to_datetime(df1['ts'], infer_datetime_format=True)   # pas vraiment utile ici, mais on convertit le timestamp "ts" en format datetime

        self.df.drop(columns=['ts'], inplace=True)
        # on interpole pour combler les NaN
        self.df['speed_gps'].interpolate(
            method='cubicspline', limit_direction='both', inplace=True)
        # 136 lignes où on a speed_gps <0 , on s'en débarasse
        self.df.drop(self.df[self.df['speed_gps'] < 0].index, inplace=True)

        return self.df


    '''
    En splittant le df en train-test-val sets après un data_generating, il est probable que l'on coupe un ou plusieurs trajets 
    en cours de route, et d'attribuer à la/les matrice(s) un label y à tort. 
    On split donc les sets avant le data_generating en sélectionnant randomly des file_id, les coupures seront donc faites 
    en fin de trajets, et on puis on fait le data_generating ensuite pour chacun des sets :
    '''

    # SPLITTING - faire listes de file_id qui iront dans train-test-val sets en les sélectionnant au hasard, mais en respectant
    # bien le ratio imposé :
        
    def split_dataset(self, train_ratio, val_ratio):

        # on créé une liste de file_id (i.e. chaque trajet a un nom, on fait une liste de ces noms)
        fileid_list = self.df['file_id'].unique().tolist()

        train_list0 = random.sample(fileid_list, int(train_ratio*len(fileid_list)))
        # l3 = [x for x in l1 if x not in l2]
        test_list = [x for x in fileid_list if x not in train_list0]
        val_list = random.sample(train_list0, int(val_ratio*len(train_list0)))
        train_list = [x for x in train_list0 if x not in val_list]

        return train_list, test_list, val_list    # -> train_list, test_list, val_list = split_dataset(.8, .3)



    def from_sets_to_df(self, train_list, test_list, val_list):

        # on définit les dataframes pour chaque set
        df_train = self.df.loc[self.df['file_id'].isin(train_list)]
        df_test = self.df.loc[self.df['file_id'].isin(test_list)]
        df_val = self.df.loc[self.df['file_id'].isin(val_list)]

        return df_train, df_test, df_val
        #df_train, df_test, df_val = mlp.from_sets_to_df(train_list, test_list, val_list)

    # StandardScaler - fit the scaler on training data only, then standardise both training and test sets with that scaler



    def scale_data(self, df_train, df_val, df_test):

        scaler = StandardScaler()
        for col in df_train:
            if col != 'label' and col != 'file_id':

                df_train.loc[:, col] = scaler.fit_transform(
                    df_train.loc[:, col].values.reshape(-1, 1))
                df_val.loc[:, col] = scaler.transform(
                    df_val.loc[:, col].values.reshape(-1, 1))
                df_test.loc[:, col] = scaler.transform(
                    df_test.loc[:, col].values.reshape(-1, 1))

        return df_train, df_val, df_test
        # -> df_train_scaled, df_val_scaled, df_test_scaled = scale_data(df_train, df_val, df_test)



    # Generate data to fit in LSTM model. One label on matrix of features
    def data_generating(self, past_history, future_target, step, df):
        
        (...)

        x = np.array(x)  # print(x.shape)   # (31466, 10, '')   # 31k lines, 10 features, '' last seconds
        y = np.array(y)  # print(y.shape)   # (31466, 3)   # '3' -> 3 labels

        return(x, y)

        # x_train, y_train = data_generating('', 0, 1, df_train_scaled)
        # x_test, y_test = 
        # x_val, y_val = 
