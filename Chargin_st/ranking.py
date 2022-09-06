import plotly.express as px
# pour figure interactive sur le browser (Plotly) :
import plotly.io as pio
pio.renderers.default='browser'
# pour figure interactive sur le browser (Folium) :
import folium
import webbrowser
import numpy as np
import pandas as pd


class Ranking:
    
    def __init__(self, df):
        self._df = df    
    

    def ranking_freq(self):
        #print(self._df)
        #self._df = pd.read_csv("C:/.../belib_donnees_counts.csv")
        df_grouped = self._df.groupby([self._df['id_pdc'].str[:15], 'latitude', 'longitude'])['counts'].sum().sort_values(ascending=False).reset_index()
       
        #print(df_grouped[:30])   # DF
        #print(len(df_grouped))   # 412 ok (c bien le bon nombre de stations - note: 1 station possede plusieurs bornes)
        
        with open("C:/.../belib_ranking.csv", 'wb') as f:               
            df_grouped.to_csv(f, header=True, index=False)   
            
        return self._df
        

    def folium_map(self, df):
        
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        center_lat = df['latitude'].mean()
        center_long = df['longitude'].mean()
        
        paris = folium.Map(location=[center_lat, center_long], zoom_start=12, tiles="Stamen Terrain")
        
        for id_pdc in df['id_pdc']:
            df_per_id = df[df['id_pdc']==id_pdc]
        
            
            if df_per_id["counts"].values[0] <= 2:    
                folium.Circle(
                    location=[df_per_id['latitude'].values[0], df_per_id['longitude'].values[0]],
                    radius = float(df_per_id["counts"].values[0]),
                    color="black",
                    fill_color="black"
                ).add_to(paris)  
                
            if (df_per_id["counts"].values[0] > 2 and df_per_id["counts"].values[0] <= 8 ):    
                folium.Circle(
                    location=[df_per_id['latitude'].values[0], df_per_id['longitude'].values[0]],
                    radius = float(df_per_id["counts"].values[0]),
                    color="yellow",
                    fill_color="yellow"
                ).add_to(paris) 
                
            if df_per_id["counts"].values[0] > 8:    
                folium.Circle(
                    location=[df_per_id['latitude'].values[0], df_per_id['longitude'].values[0]],
                    radius = float(df_per_id["counts"].values[0]),
                    color="red",
                    fill_color="red"
                ).add_to(paris)         
            
        paris.save("paris.html")
        webbrowser.open("paris.html")


        
    # def plotly_map(self, df):
        
    #     # set up the chart from the df dataFrame
    #     fig = px.scatter_geo(df, 
    #                           # longitude is taken from the df_grouped["longitude"] columns and latitude from df_grouped["latitude"]
    #                           lon="longitude", 
    #                           lat="latitude", 
    #                           # choose the map chart's projection
    #                           projection="natural earth",
    #                           # columns which is in bold in the pop up
    #                           hover_name = "counts",
    #                           # format of the popup not to display these columns' data
    #                           hover_data = {"counts":False,
    #                                         "longitude": False,
    #                                         "latitude": False
    #                                           }
    #                           ) 
                
    #     # df = px.data.gapminder().query("year == 2007")
    #     # fig = px.scatter_geo(df, locations="iso_alpha",
    #     #                      size="pop", # size of markers, "pop" is one of the columns of gapminder
    #     #                      )
    #     fig.show()        