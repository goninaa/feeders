import time
import numpy as np
import pandas as pd
import csv
from datetime import date
   

class Feeder:

    def __init__(self, fname):
        self.df = pd.DataFrame(columns=['time','signal','bat_id_1','bat1_loc','bat_id_2','bat2_loc','pump','condition'])
        self.disconnect = []
        # self.bat = False
        # self.cond = None
        self.fname = fname
        # self.bat_loc = "no_bat"
        self.bat_id_1 = None
        self.bat_id_2 = None
        self.loc_bat1 = "no_bat"
        self.loc_bat2 = "no_bat"
        self.activity = False

    def new_row(self):
        while True:
            # df = pd.DataFrame(columns=['time','signal','bat_id_1','bat1_loc','bat_id_2','bat2_loc','pump','condition'])
            new_row = pd.Series(data = {'time':pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'signal': 'play', 
                                                'bat_id_1': '', 'bat1_loc': '',
                                                'bat_id_2': '', 'bat2_loc': '', 'condition': 'cond'})
            new_row.name = 'new_row'
            # new_row = pd.DataFrame(data = {'time':pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'signal': 'play', 
            #                                     'bat_id_1': '', 'bat1_loc': '',
            #                                     'bat_id_2': '', 'bat2_loc': '', 'condition': 'cond'}, index = [pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')])

            # new_row.index = [pd.to_datetime(new_row['time'])]
            print (new_row)
            # self.df.index = pd.to_datetime(self.df['time'])
            # self.df = self.df.append(new_row, ignore_index = True) 
            index = pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')
            data = {'signal':'play'} 
            # self.df.append(pd.DataFrame(data, index=[self.df.index]))
            self.df = self.df.append(new_row, ignore_index = False)
            # self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'pump'] = 'pump'
            # self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = data
            self.df.index.drop_duplicates(keep='first')
            # self.df.index = pd.to_datetime(self.df['time'])
            self.df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
            # print (pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'))
            print (self.df)

# while True:
feeder = Feeder('fname')
feeder.new_row()