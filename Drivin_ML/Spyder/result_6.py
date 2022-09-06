from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.layers import Dense
import numpy
import pandas as pd
import os
import tensorflow as tf
from numpy import loadtxt
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import numpy as np
import tensorflow as tf
import tensorflow_addons as tfa
from tensorflow.keras.metrics import Recall, AUC, Precision
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from keras.regularizers import l2
from tensorflow.keras import backend as K, callbacks
from collections import Counter
import heapq

from ML_datapreprocessing_4 import ML_Data_preprocessing
from model_5 import My_LSTM


class Score:

    @staticmethod
    def load_model():
                
        #model = load_model("model.h5", custom_objects={'binary_focal_loss_fixed': focal_loss})   # if need to train, optimize further
        model = load_model("model.h5", compile=False)   # if it's just for model inference, as it is here
                
        # summarize model
        model.summary()
        
        return model
    

    @staticmethod
    def binary_focal_loss(gamma=2., alpha=.25):
        pass


    @staticmethod
    def metrics_call_from_another_class(My_LSTM):
        pass


    @staticmethod
    def optimization(learning_rate):    
        pass        
        

    # evaluate loaded model on test data (fichier/trajet pris au pif du dataset_bag sur lequel on n'a pas machine learningué)
    @staticmethod
    def read_test_dataset(model):
        pass
        
        
    @staticmethod
    def fonction_decision_deux(array_predicted_labels):
        
        #(...)
        
        if percentage_safe >= '...':
            print('\nThis driving is considered safe.')
        else:
            print('This driving is considered careless and dangerous.')
        
                        
    @staticmethod
    def fonction_decision_trois(array_predicted_labels, percentage_diff=False):
        counts_drowsy = []       # label 0
        counts_safe = []         # label 1
        counts_aggressive = []   # label 2

        for i in array_predicted_labels:
            if i == 0:
                counts_drowsy.append(i)
            elif i == 1:
                counts_safe.append(i)
            elif i == 2:
                counts_aggressive.append(i)
            else:
                print("Errors : unknown label met.")
        
        tot_nb_labels = len(array_predicted_labels)
        nb_drowsy_labels = len(counts_drowsy)
        nb_safe_labels = len(counts_safe)        
        nb_aggressive_labels = len(counts_aggressive)
        
        percentage_drowsy = nb_drowsy_labels/tot_nb_labels*100
        percentage_safe = nb_safe_labels/tot_nb_labels*100
        percentage_aggressive = nb_aggressive_labels/tot_nb_labels*100
        print('\n--- Trois modalités : Drowsy / Safe / Aggressive')
        print(f'Safe labels : {percentage_safe} %\nDrowsy labels : {percentage_drowsy} %\nAggressive labels : {percentage_aggressive} %')
        
        list_percentages = [percentage_drowsy, percentage_safe, percentage_aggressive]
        two_largest = heapq.nlargest(2, list_percentages)   # retrieves the 1st and 2nd largest percentages in list
        
        
        safe = [1]
        dangerous = [0, 1]        
        
        if two_largest[0] - two_largest[1] >= percentage_diff:
            if two_largest[0] == list_percentages[0]:
                print('This driving is considered Drowsy.')
            elif two_largest[0] == list_percentages[1]:
                print('This driving is considered Safe.')
            elif two_largest[0] == list_percentages[2]:
                print('This driving is considered Aggressive.')
                        
        elif two_largest[0] - two_largest[1] < percentage_diff:  
            if (two_largest[0] and two_largest[1]) in dangerous:
                print('This driving is considered careless and dangerous.')
            else:
                print('Cant tell if dangerous or safe :( ')

        
 