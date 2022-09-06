import pandas as pd


class Status:
    
    def __init__(self, df):
        self._df = df
        

    def status_counter(self):
               
        try:           
            df_old = pd.read_csv("C:/.../belib_donnees_counts.csv")
            bool_update = True

        except:              
            bool_update = False
            
        # #print(('nb points de charges : ', df['id_pdc'].nunique()))    # pas de doublon dans le dataset -> OK
      
        
        if bool_update == False:               
            for i in range(len(self._df)):
                if self._df.loc[i, 'statut_pdc'] == 'Occupé (en charge)':
                    self._df.loc[i, 'counts'] = 1
                else:
                    self._df.loc[i, 'counts'] = 0
                    

                #else:
                 #   pass
                #     print(df_old.loc[df_old['id_pdc']==id_pdc, 'counts'] + 1)
                #     self._df.loc[i, 'counts'] = df_old.loc[df_old['id_pdc']==id_pdc, 'counts'] + 1
                # else:
                #     self._df.loc[i, 'counts'] = df_old.loc[df_old['id_pdc']==id_pdc, 'counts']                   
                    
                
        else:                
            for i in df_old['id_pdc'].values:
                                
        #         print(df_old.loc[df_old['statut_pdc'] == 'Occupé (en charge)', 'id_pdc'])
                
                bool_id_new = (self._df['id_pdc'] == i)
                bool_id_old = (df_old['id_pdc'] == i)

                if self._df.loc[bool_id_new, 'statut_pdc'].values[0] == 'Occupé (en charge)':
                    self._df.loc[bool_id_new, 'counts'] = df_old.loc[bool_id_old, 'counts'] + 1
                    
                else:
                    self._df.loc[bool_id_new, 'counts'] = df_old.loc[bool_id_old, 'counts']
                
                #print(len(df_old.loc[df_old['statut_pdc'] == 'Occupé (en charge)', 'id_pdc']))
                      

        with open("C:/.../belib_donnees_counts.csv", 'wb') as f:                          
            self._df.to_csv(f, header=True, index=False)

                
        return self._df