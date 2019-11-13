import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.dates as md
import matplotlib.patches as mpatches

class Data:
    def __init__ (self,fname):
        self.fname = fname    
        self.df = pd.read_csv(self.fname)
        self.condition_start_end = []

    def time_to_index(self):
        """change time column into datetime index"""
        self.df.rename(columns={'Unnamed: 0' :'time'}, inplace=True)
        self.df.index = pd.to_datetime(self.df['time'])
        self.df.drop(['time'], axis=1, inplace=True)

    def basic_stat(self): #not finished
        """ return the sum of choices that did each bat into a new df """
        df_stat = self.df.copy().groupby('feeder').count()
        df_stat.drop(['signal'], axis=1, inplace=True)
        
        
    def bat_choices (self, bat, feeder):
        """ return a new df with one bat one feeder choices """
        pass
    def cond_times(self):
        """ return new df of start and end time of each condition"""
        df = self.df.copy()
        df_no_idx = df.reset_index()
        df_conds = pd.concat([df_no_idx['condition'], df_no_idx['condition'].shift()], axis=1)
        df_conds.columns = ['cond1', 'cond2']
        df_conds = df_conds.fillna(method='ffill')
        idx = df_conds[df_conds['cond1'] != df_conds['cond2']].index
        idx_list = list(idx)
        idx_list.remove(0)
        idx_list = [x-1 for x in idx_list]
        idx_list_max = idx_list + [df.index.shape[0]-1]
        idx_list_min = [0] + [x+1 for x in idx_list]
        df_min = df.iloc[idx_list_min]
        df_max = df.iloc[idx_list_max]
        self.condition_start_end = list(zip(df_min.index, df_max.index))
        
    def plot_cond (self): #not finished
        """ return a plot based on cond_times"""
        fig = plt.figure(figsize=(10,10))
        figtemp, ax = plt.subplots(1, 1)
        plt.style.use('seaborn')
        choices = plt.plot_date(df_bat1_choices['time'], df_bat1_choices2['better moving avg'], linestyle='solid')
        # choices = plt.plot_date(choices_df_num['time'], choices_df_num['moving avg'])

        plt.ylabel('2 = right feeder, 1 = left feeder')
        # Set time format and the interval of ticks (every 15 minutes)
        xformatter = md.DateFormatter('%H:%M')
        xlocator = md.MinuteLocator(interval = 60)
        # Set xtick labels to appear every 60 minutes
        ax.xaxis.set_major_locator(xlocator)
        ## Format xtick labels as HH:MM
        plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
        # rotate_labels...
        for label in ax.get_xticklabels():
            label.set_rotation(40)
            label.set_horizontalalignment('right')

        cond_dict = { 'unknown': 'y', 'R reward': 'g', 'L reward': 'r'}
        for min_time,max_time in condition_start_end:
            # min_time = pd.to_datetime(min_time)
            # max_time = pd.to_datetime(max_time)
            cond = df_min.loc[min_time]['condition']
            # print (cond, min_time, max_time)
            plt.axvspan(min_time,max_time, alpha=0.2, color=cond_dict[cond])
        # # act_label = ax.legend(['Right feeder activity'])
        # ax = plt.gca().add_artist(act_label)
        g_patch = mpatches.Patch(color='g', label='R reward')
        r_patch = mpatches.Patch(color='r', label='L reward')
        plt.legend(handles=[g_patch,r_patch], loc='upper left')
       



    
    def run(self):
        self.time_to_index()


if __name__ == "__main__":
    fname = '2019-11-07.csv'
    exp = Data(fname)
    print (exp.df.head())