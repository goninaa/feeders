import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.dates as md
import matplotlib.patches as mpatches
import os
from datetime import datetime



class OneNight:
    def __init__ (self,fname,subj):
        self.fname = fname    
        self.df = pd.read_csv(self.fname)
        self.condition_start_end = []
        self.df_score = pd.DataFrame()
        self.base = 0
        self.conds = [self.df['bat2_condition'].unique()]
        self.df_min = None
        self.df_stat = pd.DataFrame()
        self.bats_stat_df = pd.DataFrame(columns=['bat_id','pump_1_reward','pump_1_no_reward',
                                        'pump_2_reward','pump_2_no_reward', 'pump_1_sum', 'pump_2_sum',
                                        'pumps_sum'])
        self.df_filled = pd.DataFrame()
        self.stay_prob_df = pd.DataFrame()
        self.stay_num_df = None
        self.proba_df = None
        self.df_events = pd.DataFrame()
        self.df_min_ev = None
        self.subj = subj
        self.date = None
        self.env = None

    def find_date(self):
        self.date= self.df['Unnamed: 0'][0].split('-')
        self.date= f'{self.date[0]}{self.date[1]}{self.date[2]}'

    def time_to_index(self):
        """change time column into datetime index
            input: self.df, output:self.df """
        self.df.rename(columns={'Unnamed: 0' :'time'}, inplace=True)
        self.df.index = pd.to_datetime(self.df['time'], dayfirst=True)
        self.df.drop(['time'], axis=1, inplace=True)

    def fill_bat_id_gaps (self, gap_limit = 10):
        """ fills gaps in reading bat_ids, good when there is more than 2 bats
        and we need to know which one activiated the feeder
            input: self.df, output: self.df_filled"""
        self.df_filled = self.df.copy()
        self.df_filled['bat1_id'].fillna (method= 'ffill', limit= gap_limit, inplace= True)
        self.df_filled['bat2_id'].fillna (method= 'ffill', limit= gap_limit, inplace= True)
        # self.df_filled.to_csv(f'{fname}_fill_gaps.csv')

    def fill_bat_loc_gaps (self, gap_limit = 10):
        """ fills gaps in reading bat_locs, after fill_bat_id_gaps"""
        self.df_filled['bat1_loc'].fillna (method= 'ffill', limit= gap_limit, inplace= True)
        self.df_filled['bat2_loc'].fillna (method= 'ffill', limit= gap_limit, inplace= True)
        # self.df_filled.to_csv(f'{fname}_fill_gaps.csv')

    def fill_pumps_gaps (self, gap_limit = 2):
        """ fills gaps """
        self.df_filled['pump_1'].fillna (method= 'bfill', limit= gap_limit, inplace= True)
        self.df_filled['pump_2'].fillna (method= 'bfill', limit= gap_limit, inplace= True)
        # self.df_filled.to_csv(f'{fname}_fill_gaps.csv')

    def fill_cond_gaps (self, gap_limit = 2):
        """ fills conditions gaps """
        self.df_filled['bat1_condition'].fillna (method= 'ffill', limit= gap_limit, inplace= True)
        self.df_filled['bat2_condition'].fillna (method= 'ffill', limit= gap_limit, inplace= True)
        # self.df_filled.to_csv(f'{fname}_fill_gaps.csv')

    def map_feeders(self):
        """replace feeder number with its location (left or right)
            input: self.df_filled, output: self.df_filled"""
        map_1 = {101: 'Right',102: 'Left',103: 'Left',104: 'Right'}
        self.df_filled.replace({'bat1_loc': map_1, 'bat2_loc': map_1}, inplace=True)

    def start_event (self, bat): #still in progress
        """ return new df of the feeder first landed in each event start
            input: self.df_filled, 
            output: self.df_min_ev, self.event_start_end"""
        if bat==1:
            bat_loc = 'bat1_loc'
        elif bat==2:
            bat_loc = 'bat2_loc'
        try:
            df = self.df_filled.copy()
            df_no_idx = df.reset_index()
            df_feeder = pd.concat([df_no_idx[bat_loc], df_no_idx[bat_loc].shift()], axis=1)
            df_feeder.columns = ['loc1', 'loc2']
            # df_feeder = df_feeder.fillna(method='ffill')
            idx = df_feeder[df_feeder['loc1'] != df_feeder['loc2']].index
            idx_list = list(idx)
            idx_list.remove(0)
            idx_list = [x-1 for x in idx_list]
            idx_list_max = idx_list + [df.index.shape[0]-1]
            idx_list_min = [0] + [x+1 for x in idx_list]
            self.df_min_ev = df.iloc[idx_list_min]
            self.df_min_ev.dropna(subset=[bat_loc], inplace=True) #need to check
            df_max = df.iloc[idx_list_max]
            self.event_start_end = list(zip(self.df_min_ev.index, df_max.index))
            # self.df_events = df
        except NameError as e:
            print (e, 'bat can be 1 or 2')
        
    def find_env (self):
        env = self.fname.split('_')[-1]
        env = env.split('.')[0]
       
        if env == 'slow':
            self.env=1
        elif env == 'fast':
            self.env=2
        else:
            raise ValueError ('env is nither slow or fast')

    def mark_reward (self,bat): #not working yet
        """ mark all often and rare rewards, bat can be 1 or 2
            input: self.df_min_ev, output: self.df_min_ev('all_events_marked.csv')"""
        if bat==1:
            bat_loc = 'bat1_loc'
        elif bat==2:
            bat_loc = 'bat2_loc'
        try:
            self.df_min_ev['output'] = np.where( 
                                    ( (self.df_min_ev['pump_1'] == '1')&
                                    (self.df_min_ev[bat_loc]=='Right'))|
                                    ((self.df_min_ev['pump_2'] == '2')&
                                    (self.df_min_ev[bat_loc]=='Left'))
                                    , 'reward', 'no reward')
        except NameError as e:
            print (e, 'bat can be 1 or 2')
        root = f'/Users/gonina/Dropbox/feeders_exp/analysis/bats_events_to_analyze/subj_{self.subj}_bat'
        if not os.path.exists(root):
            os.makedirs(root)
        self.df_min_ev.to_csv(f'{root}/{self.date}_{self.env}_all_events_marked.csv')


    def run_landings_chunks (self,bat):
        """count landing chunks as events on each feeder"""
        self.find_date()
        self.find_env()
        print (self.env)
        self.time_to_index()
        self.fill_bat_id_gaps()
        self.fill_bat_loc_gaps()
        self.fill_cond_gaps()
        self.fill_pumps_gaps()
        self.map_feeders()
        self.start_event(bat)
        self.mark_reward(bat)

if __name__ == "__main__":
    
    path = '/Users/gonina/Dropbox/feeders_exp/analysis/one_bat_to_analyze'
    fname = f'{path}/1Shraga/2020-03-18-08_B_Shin_slow.csv' 
    exp = OneNight(fname=fname, subj=1)
    exp.run_landings_chunks(bat=1)