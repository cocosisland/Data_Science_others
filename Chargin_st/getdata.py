import pandas as pd
import requests
from time import localtime, strftime


class Get_data:
    
    iterations = 0    
    
    def __init__(self, nrows):
        self._mytime = strftime("%Y-%m-%d %H:%M:%S", localtime())
        # self._url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=belib-points-de-recharge-pour-vehicules-electriques-disponibilite-temps-reel&q=&rows="\
        #     + str(nrows) + "&sort=id_pdc&facet=statut_pdc&facet=last_updated&facet=arrondissement"
            
        self._url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=belib-points-de-recharge-pour-vehicules-electriques-disponibilite-temps-reel&q=&rows="\
            + str(nrows) + "&facet=statut_pdc&facet=last_updated&facet=arrondissement"



    def test_key_existence(self, rec, key, subkey):
        if subkey in rec[key]:
            #print(rec[key][subkey])
            return True
        #     if "adresse_station" in rec['fields']:                
        #         print(rec['fields']['adresse_station'])        



    def dataframe(self, data):
        
        records_list = ['record_date', 'record_ID']
        keys_list = ['adresse_station', 'arrondissement', 'url_description_pdc', 'statut_pdc', 'last_updated', 'id_pdc']#, 'coordonneesxy']        
        coord_list = ['latitude', 'longitude']
        df = pd.DataFrame(columns = records_list + keys_list + coord_list)

        for rec in data['records']:
       
            df.loc[len(df)] = [self._mytime, 
                rec['recordid'],
                rec['fields']['adresse_station'] if self.test_key_existence(rec, 'fields', 'adresse_station') else '',
                rec['fields']['arrondissement'] if self.test_key_existence(rec, 'fields', 'arrondissement') else '',
                rec['fields']['url_description_pdc'] if self.test_key_existence(rec, 'fields', 'url_description_pdc') else '',
                rec['fields']['statut_pdc'] if self.test_key_existence(rec, 'fields', 'statut_pdc') else '',
                rec['fields']['last_updated'] if self.test_key_existence(rec, 'fields', 'last_updated') else '',
                rec['fields']['id_pdc'] if self.test_key_existence(rec, 'fields', 'id_pdc') else '',
                #rec['fields']['coordonneesxy'] if self.test_key_existence(rec, 'fields', 'coordonneesxy') else '',
                rec['fields']['coordonneesxy'][0] if self.test_key_existence(rec, 'fields', 'coordonneesxy') else '',    
                rec['fields']['coordonneesxy'][1] if self.test_key_existence(rec, 'fields', 'coordonneesxy') else '']           
                                                      
        if int(data['nhits']) > 0:
            print("Nb de lignes recuperees: ", data['nhits'])
            print("- Mise en Dataframe -")    
            
        else:
            print("Aucune donnee a recuperer.")
                        
        return df
                        

            
    def scraper(self):
    
        response = requests.get(self._url)        
        if response.status_code != 200:
            print(self._mytime, " - Erreur recuperation des donnees.")
            return None
            
        else:
            data = response.json()  
            #data = json.loads(response.text)
            print(self._mytime, "- Donnees recuperees via API.")
            df = self.dataframe(data)
            Get_data.iterations += 1  
            
        return df          
          