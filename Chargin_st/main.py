#import configparser
import time
from threading import Timer
from getdata import Get_data
from status import Status
from ranking import Ranking
    

def start_and_update():

    try:
        gd = Get_data(nrows=2500)    # nrows -> nb max de lignes à scraper (le dataset en a moins)
        df = gd.scraper()
        print(df.isnull().sum())
        print(f'Scraping\'s {Get_data.iterations}-th iteration done.')
    except:
        print("Probleme lors de la collecte des donnees.")

    
    if Get_data.iterations == 1:
        df['counts'] = 0
        with open("C:/.../belib_donnees_counts.csv", 'wb') as f:
            df.to_csv(f, header=True, index=False)  
            
    #time.sleep(3)
        
    
    try:
        sc = Status(df)
        df_with_counts = sc.status_counter()
        print(f'Succes processus comptage des bornes pour la {Get_data.iterations}-th iteration.')
        print('- Mise en CSV du Dataframe avec les counts -')
        print('---------- FIN PROCESS DE L\'ITERATION ----------\n\n\n')
    except:
        print("Probleme lors du comptage des frequences d'\'utilisation des bornes.")

    
    rk = Ranking(df_with_counts)
    df_rk = rk.ranking_freq()
    rk.folium_map(df_rk)
        
    #print(df_with_counts)  # counts:int64
    set_timer()
            
            

# timer pour permettre de scraper automatiquement toutes les X secondes (durationinsec)    
def set_timer():    
    Timer(durationinsec, start_and_update).start()



def main():    
    start_and_update()

        

if __name__ == "__main__":

    global durationinsec 
    durationinsec = 5

    main()
    
    