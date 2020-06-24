import pandas as pd
import numpy as np
import attr
from attr.validators import instance_of
import datetime
import time
import os

class AllNights:
    def __init__ (self,nights_list,subj,env):
        self.fname_list = nights_list
        self.df_list = []
        self.df_nights= pd.DataFrame()
        self.subj = subj
        self.env = env

 
           
    def fname_to_df (self):
        """ create list of df's from files names """
        for fname in self.fname_list:
            df = pd.read_csv(fname)
            self.df_list.append(df)            

    def merge_nights(self) -> None:
        """Merges all data frames in the list into one data frame"""
        basic_df = self.df_list.pop(0)
        self.trial_num(basic_df)
        for df in self.df_list:
            self.trial_num(df)
            basic_df = pd.concat([basic_df, df],ignore_index=True)
        self.df_nights = basic_df
        self.df_nights.sort_values(by ='time', inplace=True)


    def format_df (self):
        """format the merged df
        convert each df to the wanted format and save to csv """
        self.night_num()
        choice = {'Right':1,'Left':2}
        reward = {'reward':1, 'no reward':0}
        corr_side = {'R reward':1, 'L reward':2} #notice this oppsite to what nitzan did
        # print (self.df_nights.loc[self.df_nights.columns.str.endswith('_loc')])#need to fix
        if self.df_nights['bat1_loc'][0]=='Right' or self.df_nights['bat1_loc'][0]=='Left':
            self.df_nights.rename(columns={'bat1_loc':'ch', 'output':'rw', 'bat2_condition':'corr_side'}, inplace=True) #need to fix bat loc?
        elif self.df_nights['bat2_loc'][0]=='Right' or self.df_nights['bat2_loc'][0]=='Left':
            self.df_nights.rename(columns={'bat1_loc':'ch', 'bat2_loc':'ch', 'output':'rw', 'bat2_condition':'corr_side'}, inplace=True)
        self.df_nights.replace({'ch': choice, 'rw':reward, 'corr_side':corr_side}, inplace=True)
        self.df_nights['subj'] = self.subj
        self.df_nights['env'] = self.env
        self.df_nights = self.df_nights[['subj','env','night','trial','epoch','time0','time1','ch','rw','corr_side']]
        self.df_nights.rename(columns={'time1':'time'},inplace=True)
        self.save_csv()

    def save_csv (self):
        root = f'/Users/gonina/Dropbox/feeders_exp/analysis/4nights_files'
        if not os.path.exists(root):
            os.makedirs(root)
        self.df_nights.to_csv(f"{root}/subj_{self.subj}_4nights.csv")
        
    
    def night_num (self):
        """create column with night number"""
        nights = self.df_nights['time0'].unique()
        nights = sorted(nights)
        num = range(1,len(nights)+1)
        nights_dict = dict(zip(nights,num))
        print (nights_dict)
        self.df_nights['night']= self.df_nights['time0']
        self.df_nights.replace({'night': nights_dict}, inplace= True)

    def trial_num (self,df):
        """ add trail number """
        df.reset_index(drop=True, inplace=True)
        df['trial'] = df.index+1
        
    def calc_time (self):
        """ calculate the time from the start of each night """
        for df in self.df_list:
            df['time'] = pd.to_datetime(df['time'],dayfirst= True)
            df['epoch'] = df['time'].astype('int64')
            df['time0'] = df['epoch'][0]
            df['time1'] = pd.to_timedelta(df['epoch']-df['time0'])
       
       

    def run (self):
        """ main pipeline"""
        self.fname_to_df() 
        self.calc_time() 
        self.merge_nights() 
        self.format_df() 
       





if __name__ == "__main__":
    
    nights = ['/Users/gonina/Dropbox/feeders_exp/feeders_figures/2020/Tzadi_slow/Tzadi_1.4.20/all_events/Tzadi_010420_all_events_marked.csv','/Users/gonina/Dropbox/feeders_exp/feeders_figures/2020/Tzadi_slow/Tzadi_31.3.20/all_events/all_events_marked.csv']
    tzadi_nights = AllNights(nights_list=nights, subj=1, env=1)
    # print (Tzadi_nights.nights_list)
    tzadi_nights.run()
    print (tzadi_nights.df_nights)
    # print (tzadi_nights.df_nights[tzadi_nights.df_nights['night']==1])
    # print (tzadi_nights.df_nights.sort_values(by ='time'))
    # print (tzadi_nights.df_nights.sort_values(by ='time')['time'][0])
 
   
    # tzadi_nights.df_nights.to_csv(f"test2306.csv")
    
    # print (datetime.datetime(2020,4,1,0,2).strftime('%s'))
   