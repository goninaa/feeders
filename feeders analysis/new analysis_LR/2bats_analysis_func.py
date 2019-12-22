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
        self.df_score = pd.DataFrame()
        self.base = 0
        self.conds = [self.df['bat2_condition'].unique()]
        self.df_min = None
        self.df_stat = pd.DataFrame()

    def time_to_index(self):
        """change time column into datetime index"""
        self.df.rename(columns={'Unnamed: 0' :'time'}, inplace=True)
        self.df.index = pd.to_datetime(self.df['time'], dayfirst=True)
        self.df.drop(['time'], axis=1, inplace=True)

    def basic_stat(self): #not finished
        """ return the sum of choices that did each bat into a new df """
        # df_stat = self.df.copy().groupby('feeder').count()
        self.df_stat = self.df.copy().groupby('bat1_condition').count()
        self.df_stat.drop(['signal'], axis=1, inplace=True)
        
    def pump_score(self, fill_na = True):
        """ give score 1 to each right feeder choice, score (-1) to left feeder choice,
        score 0 when no choice been made (only if fillna = True). save this df into a csv file"""
        self.df_score = pd.DataFrame(self.df.copy())
        mapping_1 = {'no 1': -1, '1': -1}
        mapping_2 = {'no 2': 1, '2': 1}
        self.df_score.replace({'pump_1': mapping_1, 'pump_2': mapping_2}, inplace= True)
        self.df_score['pump_1'].fillna(0, inplace= True)
        self.df_score['pump_2'].fillna(0, inplace= True)
        self.df_score['sum_pump'] = self.df_score['pump_1']+self.df_score['pump_2']
        if fill_na == False: # when fill_na=False only results where bat chose will be taken into account
            self.df_score.sum_pump.replace(0, np.nan, inplace=True)
        self.df_score.to_csv(f"{self.fname}_score.csv")


    # def mean_pref(self, min = '10Min'): #not finished
    #     mean_pref = self.df_score.resample(min, self.base, label='right').mean()

    def fill_bat_id_gaps (self, gap_limit = 10):
        """ fills gaps in reading bat_ids, good when there is more than 2 bats
        and we need to know which one activiated the feeder"""
        self.df['bat1_id'].fillna (method= 'ffill', limit= gap_limit, inplace= True)
        self.df['bat2_id'].fillna (method= 'ffill', limit= gap_limit, inplace= True)
        self.df.to_csv(f'{fname}_fill_gaps.csv')

    def find_base(self):
        self.base = self.df.index[0].minute

    # def bat_choices (self, bat, feeder):
    #     """ return a new df with one bat one feeder choices """
    #     pass

    def cond_times(self):
        """ return new df of start and end time of each condition"""
        df = self.df.copy()
        df_no_idx = df.reset_index()
        df_conds = pd.concat([df_no_idx['bat2_condition'], df_no_idx['bat2_condition'].shift()], axis=1)
        df_conds.columns = ['cond1', 'cond2']
        df_conds = df_conds.fillna(method='ffill')
        idx = df_conds[df_conds['cond1'] != df_conds['cond2']].index
        idx_list = list(idx)
        idx_list.remove(0)
        idx_list = [x-1 for x in idx_list]
        idx_list_max = idx_list + [df.index.shape[0]-1]
        idx_list_min = [0] + [x+1 for x in idx_list]
        self.df_min = df.iloc[idx_list_min]
        df_max = df.iloc[idx_list_max]
        self.condition_start_end = list(zip(self.df_min.index, df_max.index))

    def plot_all_choices(self, name):
        """ """
        pd.plotting.register_matplotlib_converters(explicit=True)

        fig = plt.figure(figsize=(10,10))
        figtemp, ax = plt.subplots(1, 1)
        plt.style.use('seaborn')
        choices = plt.plot_date(self.df_score.index, self.df_score['sum_pump'], linestyle=':')
        plt.title (f'bats choices')
        plt.ylabel('1 = right feeder, (-1) = left feeder')
        # Set time format and the interval of ticks (every 15 minutes)
        xformatter = md.DateFormatter('%H:%M')
        xlocator = md.MinuteLocator(interval = 60)
        # Set xtick labels to appear every 60 minutes
        ax.xaxis.set_major_locator(xlocator)
        ## Format xtick labels as HH:MM
        plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
        # rotate_labels
        for label in ax.get_xticklabels():
            label.set_rotation(40)
            label.set_horizontalalignment('right')

        cond_dict = { 'unknown': 'y', 'R reward': 'g', 'L reward': 'r'}
        # cond_dict = { 'unknown': 'y', 'R reward': 'g', 'equal reward': 'r'}
        # cond_dict = { self.conds[2]: 'y', self.conds[0]: 'g', self.conds[1]: 'r'}
        for min_time,max_time in self.condition_start_end:
            cond = self.df_min.loc[min_time]['bat2_condition']
            plt.axvspan(min_time,max_time, alpha=0.2, color=cond_dict[cond])
        g_patch = mpatches.Patch(color='g', label='R reward')
        r_patch = mpatches.Patch(color='r', label='L reward')
        plt.legend(handles=[g_patch,r_patch], loc='upper right')
        figtemp.savefig(f'{fname}_choices_plot_{name}.png')

    def plot_pref (self, minutes = '10Min', name= 'choices_only'): 
        """ """
        df_mean_pref = self.df_score.resample(minutes, base = self.base, label='right').mean()
   
        pd.plotting.register_matplotlib_converters(explicit=True)

        fig = plt.figure(figsize=(10,10))
        figtemp, ax = plt.subplots(1, 1)
        plt.style.use('seaborn')
        choices = plt.plot_date(df_mean_pref.index, df_mean_pref['sum_pump'], linestyle=':')
        plt.title (f'mean ({minutes}) of choices')
        plt.ylabel('1 = right feeder, (-1) = left feeder')
        # Set time format and the interval of ticks (every 15 minutes)
        xformatter = md.DateFormatter('%H:%M')
        xlocator = md.MinuteLocator(interval = 60)
        # Set xtick labels to appear every 60 minutes
        ax.xaxis.set_major_locator(xlocator)
        ## Format xtick labels as HH:MM
        plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
        # rotate_labels
        for label in ax.get_xticklabels():
            label.set_rotation(40)
            label.set_horizontalalignment('right')

        cond_dict = { 'unknown': 'y', 'R reward': 'g', 'L reward': 'r'}
        # cond_dict = { 'unknown': 'y', 'R reward': 'g', 'equal reward': 'r'}
        # cond_dict = { self.conds[2]: 'y', self.conds[0]: 'g', self.conds[1]: 'r'}
        for min_time,max_time in self.condition_start_end:
            cond = self.df_min.loc[min_time]['bat2_condition']
            plt.axvspan(min_time,max_time, alpha=0.2, color=cond_dict[cond])
        g_patch = mpatches.Patch(color='g', label='R reward')
        r_patch = mpatches.Patch(color='r', label='L reward')
        plt.legend(handles=[g_patch,r_patch], loc='upper right')
        figtemp.savefig(f'{fname}_{minutes}_mean_plot_{name}.png')
       



    def run_fill_na(self):
        self.time_to_index()
        self.find_base()
        self.pump_score()
        # self.pump_score(fill_na=False)
        self.cond_times()
        self.plot_pref (minutes = '10Min', name = 'fill_na')
        self.plot_all_choices('fill_na')

    def run(self):
        self.time_to_index()
        self.find_base()
        # self.pump_score()
        self.pump_score(fill_na=False)
        self.cond_times()
        self.plot_pref (minutes = '10Min', name = 'choices_only')
        self.plot_all_choices('choices_only')


if __name__ == "__main__":

    # fname = '2019-11-15.csv'
    # fname = '2019-12-02_precent.csv'
    # fname = '2019-12-16_S_X.csv' #not working
    fname = '2019-12-20_S_dot_line_train.csv'


    exp = Data(fname)
    # exp.time_to_index()
    # exp.fill_bat_id_gaps()
    # exp.run_fill_na()
    exp.run()
    # exp.basic_stat()
    # print (exp.df_stat)
    # print (exp.df.head())
  