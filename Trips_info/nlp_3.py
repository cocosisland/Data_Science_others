import ---
import os


class NLP:
    
    def __init__(self, text_address):
        
        self.text_address = text_address



    def extract_road_from_address(self, model_str):
        
        nlp = ...
            (...)
        return road_str
    
    
    
    def get_roadtype_from_NLP(self):   # called from app_infos.py
                
        roadtype_str = self.extract_road_from_address("model")

        return roadtype_str
    
