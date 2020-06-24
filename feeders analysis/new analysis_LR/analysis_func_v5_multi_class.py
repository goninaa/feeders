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
        self.bats_stat_df = pd.DataFrame(columns=['bat_id','pump_1_reward','pump_1_no_reward',
                                        'pump_2_reward','pump_2_no_reward', 'pump_1_sum', 'pump_2_sum',
                                        'pumps_sum'])
        self.df_filled = pd.DataFrame()
        self.stay_prob_df = pd.DataFrame()
        self.stay_num_df = None
        self.proba_df = None
        self.df_events = pd.DataFrame()
        self.df_min_ev = None

    def time_to_index(self):
        """change time column into datetime index
            input: self.df, output:self.df """
        self.df.rename(columns={'Unnamed: 0' :'time'}, inplace=True)
        self.df.index = pd.to_datetime(self.df['time'], dayfirst=True)
        self.df.drop(['time'], axis=1, inplace=True)

    def remove_duplicated(self): #not in use
        """remove duplicated timestamps while keeping last value"""
        bool_series = self.df['Unnamed: 0'].duplicated(keep = 'last')
        self.df = self.df[~bool_series] 

    def basic_stat(self): #not finished
        """ return the sum of choices that did each bat into a new df """
        # df_stat = self.df.copy().groupby('feeder').count()
        self.df_stat = self.df.copy().groupby('bat1_condition').count()
        self.df_stat.drop(['signal', 'bat1_id', 'bat1_loc', 'bat2_id', 'bat2_loc', 'bat2_condition'], axis=1, inplace=True)
        print (self.df_stat)

    def bats_stat(self): # not finished
        """ statistics for each bat"""
        # finding all unique tags:
        tags = self.df_filled['bat1_id'].unique().tolist()
        tags.extend(self.df_filled['bat2_id'].unique().tolist())
        tags = list(set(tags))
        tags = [x for x in tags if str(x) != 'nan']
        # print (tags)
        for tag in tags:
            tag_count = self.df_filled[self.df_filled['bat1_id']==tag].count(axis=0)
            print (tag)
            # print(tag_count['bat1_id'])
            try:
                if tag_count['bat1_id'] == 0: #checks if tag is in bat1_id, if not than it in bat2_id
                    tag_count = self.df_filled[self.df_filled['bat2_id']==tag].count(axis=0)
                    # print (tag_count)
                    reward_count_1 = self.df_filled.groupby(['bat2_id','pump_1'])
                    reward_count_2 = self.df_filled.groupby(['bat2_id','pump_2'])
                else:
                    reward_count_1 = self.df_filled.groupby(['bat1_id','pump_1'])
                    reward_count_2 = self.df_filled.groupby(['bat1_id','pump_2'])
                
                # print (reward_count_1.get_group((tag,'1')).count())
                # print (reward_count_1.get_group((tag,'1')).count()['pump_1'])
                tag_dict = {'bat_id': tag, 
                            'pump_1_reward': reward_count_1.get_group((tag,'1')).count()['pump_1'],
                            'pump_1_no_reward': reward_count_1.get_group((tag,'no 1')).count()['pump_1'],
                            'pump_2_reward': reward_count_2.get_group((tag,'2')).count()['pump_2'], 
                            'pump_2_no_reward': reward_count_2.get_group((tag,'no 2')).count()['pump_2'], 
                            'pump_1_sum': tag_count['pump_1'], 'pump_2_sum': tag_count['pump_2'], 
                            'pumps_sum': (tag_count['pump_1']+tag_count['pump_2'])}
            except:
                print ('stat_problem')
        
            self.bats_stat_df = self.bats_stat_df.append(tag_dict, ignore_index=True)

            # self.bats_stat_df = pd.MultiIndex.from_frame(self.bats_stat_df, names = ['bat_id','pump_1_reward','pump_1_no_reward',
            #                             'pump_2_reward','pump_2_no_reward', 'pump_1_sum', 'pump_2_sum',
            #                             'pumps_sum'])
        print (self.bats_stat_df)
        self.bats_stat_df.to_csv(f"{self.fname}_bats_stat.csv")
        
    def pump_score(self, fill_na = True): 
        """ give score 1 to each left feeder choice, score (-1) to right feeder choice,
        score 0 when no choice been made (only if fillna = True). save this df into a csv file"""
        # self.df_score = self.df.copy() 
        mapping_1 = {'no 1': -1, '1': -1}
        mapping_2 = {'no 2': 1, '2': 1}
        self.df_score['pump_1'].fillna(0, inplace= True) #right feeder
        self.df_score['pump_2'].fillna(0, inplace= True)
        self.df_score =  self.df_score.astype({'pump_1': 'object', 'pump_2': 'object'})
        self.df_score.replace({'pump_1': mapping_1, 'pump_2': mapping_2}, inplace= True)
        self.df_score =  self.df_score.astype({'pump_1': 'int', 'pump_2': 'int'})
        self.df_score['sum_pump'] = self.df_score['pump_1']+self.df_score['pump_2']
        if fill_na == False: # when fill_na=False only results where bat chose will be taken into account
            self.df_score.sum_pump.replace(0, np.nan, inplace=True)
                
        map_1 = {-1: 'Right',1: 'Left'}
        self.df_score.replace({'sum_pump': map_1}, inplace=True)
       
        self.df_score.to_csv(f"{self.fname}_score.csv")

    def match (self,bat): # need to fix
        """ add a column with y/n if value was as expected or not. later used for plotting"""
        # self.df_score = pd.DataFrame(self.df.copy())
        self.df_score = pd.DataFrame(self.df_filled.copy())
        if bat==1:
            bat_loc='bat1_loc'
        elif bat==2:
            bat_loc='bat2_loc'

        # self.df_score['match'] = np.where( 
        #                         ( (self.df_score['pump_1'] == '1') & (self.df_score['bat2_condition'] == 'L reward' ) ) 
        #                         | ( (self.df_score['pump_1'] == 'no 1') & (self.df_score['bat2_condition'] == 'R reward' ) )
        #                         | ( (self.df_score['pump_2'] == '2') & (self.df_score['bat2_condition'] == 'R reward' ))
        #                         | ( (self.df_score['pump_2'] == 'no 2') & (self.df_score['bat2_condition'] == 'L reward' ))
        #                         , 's', 'x')
        # self.df_score['match'] = np.where( 
        #                             ( (self.df_score['pump_1'] == '1')&
        #                             (self.df_score['bat2_loc']==104))|
        #                             ((self.df_score['pump_2'] == '2')&
        #                             (self.df_score['bat2_loc']==103))
        #                             , 'reward', 'none')
                                     #need to fix here- that only -1 or -2 will be 'no reward'
        # find all choices (only when pump gave "reward" or "no reward"):
        self.df_score['match'] = np.where( 
                                    ( ((self.df_score['pump_1'] == '1')|(self.df_score['pump_1'] == 'no 1'))&
                                    (self.df_score[bat_loc]=='Right'))|
                                    (((self.df_score['pump_2'] == '2')|(self.df_score['pump_2'] == 'no 2'))&
                                    (self.df_score[bat_loc]=='Left'))
                                    , 'choice', 0) 
        # leave only reward and no rewards (drop 0)
        self.df_score = self.df_score[self.df_score.match == 'choice']
        self.df_score['match'] = np.where( 
                                    ( (self.df_score['pump_1'] == '1')&
                                    (self.df_score[bat_loc]=='Right'))|
                                    ((self.df_score['pump_2'] == '2')&
                                    (self.df_score[bat_loc]=='Left'))
                                    , 'reward', 'no reward')



        # print (self.df_score[self.df_score['match'] == 'y'])
        # self.df.rename(columns={'Unnamed: 0' :'time'}, inplace=True)
        self.df_score.to_csv(f"{self.fname}_score.csv")

    def stay_prob (self):
        """ """
        ## prepare df:
        self.stay_prob_df = self.df.copy()
        mapping_1 = {'no 1': -1}
        mapping_2 = {'no 2': -2}
        self.stay_prob_df['pump_1'].fillna(0, inplace= True)
        self.stay_prob_df['pump_2'].fillna(0, inplace= True)
        self.stay_prob_df = self.stay_prob_df.astype({'pump_1': 'object', 'pump_2': 'object'})
        self.stay_prob_df.replace({'pump_1': mapping_1, 'pump_2': mapping_2}, inplace= True)
        self.stay_prob_df = self.stay_prob_df.astype({'pump_1': 'int', 'pump_2': 'int'})
        self.stay_prob_df['sum_pump'] = self.stay_prob_df['pump_1']+self.stay_prob_df['pump_2']
        self.stay_prob_df['sum_pump'].replace(0, np.nan, inplace = True)
        # self.stay_prob_df.sum_pump.replace(0, np.nan, inplace=True)
        self.stay_prob_df.dropna(subset=['sum_pump'],inplace = True)
        self.stay_prob_df['pre_choice'] = self.stay_prob_df['sum_pump'].shift(1)
        self.stay_prob_df['choice'] = self.stay_prob_df['sum_pump']
        map_choice = {-1:1,-2:2}
        self.stay_prob_df.replace({'choice': map_choice}, inplace= True)
        self.stay_prob_df.to_csv('stay_prob_df.csv') #for debugging

    def stay_prob_events (self, bat=2):
        """ """
        # still missing a way to calculate one bat when there are two bats
        ## prepare df:
        if bat==1:
            bat_loc='bat1_loc'
        elif bat==2:
            bat_loc='bat2_loc'
        self.stay_prob_ev = self.df_min_ev.copy()
        mapping_1 = {'no 1': -1}
        mapping_2 = {'no 2': -2}
        self.stay_prob_ev['pump_1'].fillna(0, inplace= True)
        self.stay_prob_ev['pump_2'].fillna(0, inplace= True)
        self.stay_prob_ev = self.stay_prob_ev.astype({'pump_1': 'object', 'pump_2': 'object'})
        self.stay_prob_ev.replace({'pump_1': mapping_1, 'pump_2': mapping_2}, inplace= True)
        self.stay_prob_ev = self.stay_prob_ev.astype({'pump_1': 'int', 'pump_2': 'int'})
        self.stay_prob_ev['num_output'] = self.stay_prob_ev['pump_1']+self.stay_prob_ev['pump_2']
        self.stay_prob_ev['pre_choice'] = self.stay_prob_ev['num_output'].shift(1)
        self.stay_prob_ev['choice'] = self.stay_prob_ev[bat_loc]
        map_choice = {'Right':1,'Left':2}
        self.stay_prob_ev.replace({'choice': map_choice}, inplace= True)
        self.stay_prob_ev.to_csv('stay_prob_ev1.csv') #for debugging


    def stay_change_to_df(self,cond, events=False): #new version
        """ create stay-change number (for specefic condition) df based on stay_prob func"""
        if events==True:
            df1 = self.stay_prob_ev[self.stay_prob_ev['bat2_condition']== cond].copy()
        elif events==False:
            df1= self.stay_prob_df[self.stay_prob_df['bat2_condition']== cond].copy() #need to fix
        # df1 = self.stay_prob_ev.copy()
        # print (df1)
        #create masks for pump_1
        reward_1_stay = (df1['pre_choice']==1) & (df1['choice']==1)
        reward_1_change = (df1['pre_choice']==1) & (df1['choice']==2)
        unreward_1_stay = ((df1['pre_choice']==-1)|(df1['pre_choice']==0)) & (df1['choice']==1)
        unreward_1_change = ((df1['pre_choice']==-1)|(df1['pre_choice']==0)) & (df1['choice']==2)
        #create masks for pump_2
        reward_2_stay = (df1['pre_choice']==2) & (df1['choice']==2)
        reward_2_change = (df1['pre_choice']==2) & (df1['choice']==1)
        unreward_2_stay = ((df1['pre_choice']==-2)|(df1['pre_choice']==0)) & (df1['choice']==2)
        unreward_2_change = ((df1['pre_choice']==-2)|(df1['pre_choice']==0)) & (df1['choice']==1)
        #create dict 
        reward = {'stay_1':df1[reward_1_stay].choice.count(), 'change_1':df1[reward_1_change].choice.count(),
                  'stay_2':df1[reward_2_stay].choice.count(), 'change_2':df1[reward_2_change].choice.count()}
        unreward = {'stay_1':df1[unreward_1_stay].choice.count(), 'change_1':df1[unreward_1_change].choice.count(),
                    'stay_2':df1[unreward_2_stay].choice.count(), 'change_2':df1[unreward_2_change].choice.count()}
        proba_dict = {'reward' :reward,'unreward':unreward}
       
        self.stay_num_df = pd.DataFrame(proba_dict)

    def stay_prob_to_df(self, cond):
        """ create stay-change probability df based on...1=right, 2=left"""
        self.proba_df = self.stay_num_df.copy().T
        print (cond)
        print (self.proba_df)
        if cond== 'R reward':
            self.proba_df['80% reward'] = self.proba_df['stay_1']/(self.proba_df['stay_1']+self.proba_df['change_1'])
            self.proba_df['20% reward'] = self.proba_df['stay_2']/(self.proba_df['stay_2']+self.proba_df['change_2'])
        elif cond== 'L reward':
            self.proba_df['20% reward'] = self.proba_df['stay_1']/(self.proba_df['stay_1']+self.proba_df['change_1'])
            self.proba_df['80% reward'] = self.proba_df['stay_2']/(self.proba_df['stay_2']+self.proba_df['change_2'])
            self.proba_df.drop(['stay_1','change_1','stay_2','change_2'], axis=1, inplace=True)
        else:
            raise ValueError('cond must be "R reward" or "L reward"')
        print (self.proba_df)
        self.proba_df=self.proba_df[['80% reward','20% reward']] #keeps the same colmuns order
  

    def plot_prob(self,cond):
        colors = {'b','r'}
        ax = self.proba_df.plot.bar(color=colors)
        ax.set_title('Stay Probability')
        L=plt.legend()
        # print ( L.get_texts()[0])
        L.get_texts()[0].set_text('80% reward')
        L.get_texts()[1].set_text('20% reward')
        ax.set_ylabel('Stay probability')
        fig = ax.get_figure()
        fig.savefig(f'{fname}_stay_prob.png')
        fig.savefig(f'{fname}_stay_prob.svg')
     
    def run_prob_ev(self,cond='L reward',bat=2):
        """stay-probability plot by events """
        self.stay_prob_events(bat=bat)
        self.stay_change_to_df(cond=cond, events=True)
        self.stay_prob_to_df(cond)
        self.plot_prob(cond)


    def run_prob(self,cond):
        """stay-probability plot by choices """
        self.stay_prob()
        self.stay_change_to_df(cond, events=False)
        self.stay_prob_to_df(cond)
        self.plot_prob(cond)

    def feeders_time_plot(self, x_time, y, marker, title):
        fig = plt.figure(figsize=(30,30))
        figtemp, ax = plt.subplots(1, 1)
        # x_time = pd.to_datetime(x_time,dayfirst=True)
        x = x_time
        # y = self.df_min_ev[bat_loc]
        sns.set()
        sns_fig = sns.scatterplot( x=x,y=y,
                        hue=marker, style = marker, 
                        data=self.df_min_ev, markers= True)
        xformatter = md.DateFormatter('%H:%M')
        xlocator = md.MinuteLocator(interval = 60)
        ax.xaxis.set_major_locator(xlocator)
        plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
        for label in ax.get_xticklabels():
            label.set_rotation(40)
            label.set_horizontalalignment('right')
        sns_fig.set_xlabel('Time', fontweight='bold')
        sns_fig.set_ylabel('Feeder')
        sns_fig.set_title(title)
        # cond_dict = { 'unknown': 'y', 'R reward': 'g', 'L reward': 'r', 'equal reward': 'c'}
        # for min_time,max_time in self.condition_start_end:
        #     cond = self.df_min.loc[min_time]['bat2_condition']
        #     plt.axvspan(min_time,max_time, alpha=0.2, color=cond_dict[cond])
        # g_patch = mpatches.Patch(color='g', label='R reward')
        # r_patch = mpatches.Patch(color='r', label='L reward')
        # plt.legend(handles=[g_patch,r_patch], loc='upper right')
        plt.show()
        figtemp.savefig(f'{fname}_{title}.png')
        figtemp.savefig(f'{fname}_{title}.svg')


    # def mean_pref(self, min = '10Min'): #not finished
    #     mean_pref = self.df_score.resample(min, self.base, label='right').mean()

    def fill_bat_id_gaps (self, gap_limit = 10):
        """ fills gaps in reading bat_ids, good when there is more than 2 bats
        and we need to know which one activiated the feeder
            input: self.df, output: self.df_filled"""
        self.df_filled = self.df.copy()
        self.df_filled['bat1_id'].fillna (method= 'ffill', limit= gap_limit, inplace= True)
        self.df_filled['bat2_id'].fillna (method= 'ffill', limit= gap_limit, inplace= True)
        self.df_filled.to_csv(f'{fname}_fill_gaps.csv')

    def fill_bat_loc_gaps (self, gap_limit = 10):
        """ fills gaps in reading bat_locs, after fill_bat_id_gaps"""
        self.df_filled['bat1_loc'].fillna (method= 'ffill', limit= gap_limit, inplace= True)
        self.df_filled['bat2_loc'].fillna (method= 'ffill', limit= gap_limit, inplace= True)
        self.df_filled.to_csv(f'{fname}_fill_gaps.csv')

    def fill_pumps_gaps (self, gap_limit = 2):
        """ fills gaps """
        self.df_filled['pump_1'].fillna (method= 'bfill', limit= gap_limit, inplace= True)
        self.df_filled['pump_2'].fillna (method= 'bfill', limit= gap_limit, inplace= True)
        self.df_filled.to_csv(f'{fname}_fill_gaps.csv')

    def fill_cond_gaps (self, gap_limit = 2):
        """ fills conditions gaps """
        self.df_filled['bat1_condition'].fillna (method= 'ffill', limit= gap_limit, inplace= True)
        self.df_filled['bat2_condition'].fillna (method= 'ffill', limit= gap_limit, inplace= True)
        self.df_filled.to_csv(f'{fname}_fill_gaps.csv')

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

    def plot_all_choices_match(self, name):
        """ """
        pd.plotting.register_matplotlib_converters(explicit=True)

        fig = plt.figure(figsize=(30,30))
        figtemp, ax = plt.subplots(1, 1)
        plt.style.use('seaborn')
        # # choices = plt.plot_date(self.df_score.index, self.df_score['sum_pump'], marker = (np.where((self.df_score[self.df_score['match'] == 'y']), 's', 'x')), linestyle=':')
        self.df_score.index = pd.to_datetime(self.df_score.index, dayfirst=True)
        data = self.df_score
        marker = self.df_score['match']
        markers = {"reward": "o", "no reward": "X"}
        # sns.scatterplot(data=data, x='time', y='sum_pump', style='match')
        # # sns.scatterplot( x=self.df_score['time'], y='sum_pump', style='match', data=data)
        # sns.lineplot( x=self.df_score.index, y=self.df_score['sum_pump'], hue=self.df_score['match'], style = self.df_score['match'], data=data, markers= True)
        sns.scatterplot( x=self.df_score.index,y=self.df_score['sum_pump'],
                                    hue=marker, style = marker, markers=markers,
                                    data=data, palette = {"reward": "blue", "no reward": "darkorange"})
        # sns.lineplot( x=self.df_score['time'], y=self.df_score['sum_pump'], data=data, markers= True)
        # g.fig.autofmt_xdate()
        plt.title (f'bats choices')
        plt.ylabel('feeder')
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

        # cond_dict = { 'unknown': 'y', 'R reward': 'g', 'L reward': 'r', 'equal reward': 'c'}
        # # cond_dict = { 'unknown': 'y', 'R reward': 'g', 'L reward': 'r'}
        # # cond_dict = { 'unknown': 'y', 'R reward': 'g', 'equal reward': 'r'}
        # # cond_dict = { self.conds[2]: 'y', self.conds[0]: 'g', self.conds[1]: 'r'}
        # for min_time,max_time in self.condition_start_end:
        #     cond = self.df_min.loc[min_time]['bat2_condition']
        #     plt.axvspan(min_time,max_time, alpha=0.2, color=cond_dict[cond])
        # g_patch = mpatches.Patch(color='g', label='R reward')
        # r_patch = mpatches.Patch(color='r', label='L reward')
        # plt.legend(handles=[g_patch,r_patch], loc='upper right')
        figtemp.savefig(f'{fname}_choices_plot_{name}.png')
        figtemp.savefig(f'{fname}_choices_plot_{name}.svg')
        plt.show()

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

        cond_dict = { 'unknown': 'y', 'R reward': 'g', 'L reward': 'r', 'equal reward': 'c'}
        # cond_dict = { 'unknown': 'y', 'R reward': 'g', 'L reward': 'r'}
        # cond_dict = { 'unknown': 'y', 'R reward': 'g', 'equal reward': 'r'}
        # cond_dict = { self.conds[2]: 'y', self.conds[0]: 'g', self.conds[1]: 'r'}
        for min_time,max_time in self.condition_start_end:
            cond = self.df_min.loc[min_time]['bat2_condition']
            plt.axvspan(min_time,max_time, alpha=0.2, color=cond_dict[cond])
        g_patch = mpatches.Patch(color='g', label='R reward')
        r_patch = mpatches.Patch(color='r', label='L reward')
        plt.legend(handles=[g_patch,r_patch], loc='upper right')
        figtemp.savefig(f'{fname}_choices_plot_{name}.png')
        figtemp.savefig(f'{fname}_choices_plot_{name}.svg')


    def plot_pref (self, minutes = '10Min', name= 'choices_only'): 
        """ """
        df_mean_pref = self.df_score.resample(minutes, base = self.base, label='right').mean()
   
        pd.plotting.register_matplotlib_converters(explicit=True)

        fig = plt.figure(figsize=(10,10))
        figtemp, ax = plt.subplots(1, 1)
        plt.style.use('seaborn')
        choices = plt.plot_date(df_mean_pref.index, df_mean_pref['sum_pump'], linestyle=':')
        plt.title (f'mean ({minutes}) of choices')
        plt.ylabel('1 = left feeder, (-1) = right feeder')
        plt.yticks(np.arange(-1, 1.2, step=0.25))
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

        cond_dict = { 'unknown': 'y', 'R reward': 'g', 'L reward': 'r', 'equal reward': 'c'}
        # cond_dict = { 'unknown': 'y', 'R reward': 'g', 'equal reward': 'r'}
        # cond_dict = { self.conds[2]: 'y', self.conds[0]: 'g', self.conds[1]: 'r'}
        for min_time,max_time in self.condition_start_end:
            cond = self.df_min.loc[min_time]['bat2_condition']
            plt.axvspan(min_time,max_time, alpha=0.2, color=cond_dict[cond])
        g_patch = mpatches.Patch(color='g', label='R reward')
        r_patch = mpatches.Patch(color='r', label='L reward')
        plt.legend(handles=[g_patch,r_patch], loc='upper right')
        figtemp.savefig(f'{fname}_{minutes}_mean_plot_{name}.png')
        figtemp.savefig(f'{fname}_{minutes}_mean_plot_{name}.svg')
        plt.show()

    def map_feeders(self):
        """replace feeder number with its location (left or right)
            input: self.df_filled, output: self.df_filled"""
        # self.df_filled['bat2_loc'].fillna(0, inplace= True) # works
        # map_1 = {101: 'Right',102: 'Left',103: 'Left',0:'Neutral',104: 'Right'}
        map_1 = {101: 'Right',102: 'Left',103: 'Left',104: 'Right'}
        # self.df_filled.dropna(subset=['bat2_loc'], inplace=True)
        # map_2 = {102: 'left'}
        self.df_filled.replace({'bat1_loc': map_1, 'bat2_loc': map_1}, inplace=True)

    def plot_bat_movement(self, bat):
        """ plots bat movement and reward for all events (not choices)
            input: self.df_filled, self.df_min_ev,
            output: movement and rewards plot """
        if bat==1:
            bat_loc = 'bat1_loc'
        elif bat==2:
            bat_loc = 'bat2_loc'
        try:
            fig = plt.figure(figsize=(30,30))
            figtemp, ax = plt.subplots(1, 1)
            # pd.plotting.register_matplotlib_converters(explicit=True)
            self.df_filled.index = pd.to_datetime(self.df_filled.index,dayfirst=True)
            # x = self.df_filled.index
            # y = self.df_filled[bat_loc]
            # y = self.df_filled[bat_loc].sort_values([bat_loc],ascending = [True])
            x = self.df_min_ev.index
            y = self.df_min_ev[bat_loc]
            marker = self.df_min_ev['output']
            sns.set()
            # plt.plot_date(x,y) #works
            sns_fig = sns.scatterplot( x=x,y=y,
                            hue=marker, style = marker, 
                            data=self.df_min_ev, markers= True)
            xformatter = md.DateFormatter('%H:%M')
            xlocator = md.MinuteLocator(interval = 60)
            ax.xaxis.set_major_locator(xlocator)
            plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
            for label in ax.get_xticklabels():
                label.set_rotation(40)
                label.set_horizontalalignment('right')
            sns_fig.set_xlabel('Time', fontweight='bold')
            sns_fig.set_ylabel('Feeder')
            sns_fig.set_title(f'Bat {bat} movement and rewards')
            # plt.plot(self.df_filled[bat_loc]) # works
            figtemp.tight_layout()
            plt.show()
            figtemp.savefig(f'{fname}_movement_plot.png')
            figtemp.savefig(f'{fname}_movement_plot.svg')
            # figtemp.savefig('right-left.png')
        except NameError as e:
            print (e, 'bat can be 1 or 2')


    def run_landings_chunks (self,bat, cond):
        """count landing chunks as events on each feeder"""
        self.time_to_index()
        self.fill_bat_id_gaps()
        self.fill_bat_loc_gaps()
        self.fill_cond_gaps()
        self.fill_pumps_gaps()
        self.map_feeders()
        self.start_event(bat)
        self.mark_reward(bat)
        self.plot_bat_movement(bat=bat)
        self.run_prob_ev(cond=cond,bat=bat)
        # self.run_prob_ev(cond='R reward')
    #    print (self.df_filled['bat1_loc'])

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

    def mark_reward (self,bat): #not working yet
        """ mark all often and rare rewards, bat can be 1 or 2
            input: self.df_min_ev, output: self.df_min_ev"""
        # self.df_min_ev['mark'] = np.where( 
        #                         ( (self.df_min_ev['pump_1'] == '1') & (self.df_min_ev['bat2_condition'] == 'R reward' ) )
        #                         | ( (self.df_min_ev['pump_2'] == '2') & (self.df_min_ev['bat2_condition'] == 'L reward' ) )
        #                         , 'reward', 'no reward')
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
        self.df_min_ev.to_csv('all_events_marked.csv')

    def find_tag(self):
        """find if bat1 or bat2 by the tag"""
        pass

    def find_first_cond:
        """find if starts with R reward or L reawrd """     
        pass   
        


    def run_fill_na(self,bat):
        self.time_to_index()
        self.find_base()
        self.match(bat)
        self.pump_score()
        # self.pump_score(fill_na=False)
        self.cond_times()
        self.plot_pref (minutes = '10Min', name = 'fill_na')
        self.plot_pref (minutes = '60Min', name = 'fill_na')
        self.plot_all_choices('fill_na')
        self.basic_stat()
        # print (self.df_stat)

    def run(self,bat):
        self.time_to_index()
        self.find_base()
        self.fill_bat_id_gaps()
        self.fill_bat_loc_gaps()
        self.fill_cond_gaps()
        self.map_feeders()
        self.match(bat) 
        # self.pump_score()
        self.pump_score(fill_na=False) 
        # self.map_feeders()
        self.cond_times()
        self.plot_pref (minutes = '10Min', name = 'choices_only')
        self.plot_pref (minutes = '60Min', name = 'choices_only')
        # self.plot_all_choices_match('choices_only') # need to fix?
        # self.fill_bat_id_gaps()
        self.basic_stat()
        # print (self.df_stat)


if __name__ == "__main__":

    # fname = '2020-03-09-08_A_Gimel_fast.csv'
    # fname = '/Users/gonina/Library/Mobile Documents/com~apple~CloudDocs/lab/python_codes/feeders/feeders analysis/2020-04-02-09_B_Eight_slow_cut_midnight.csv'
    # fname = '/Users/gonina/Library/Mobile Documents/com~apple~CloudDocs/lab/python_codes/feeders/feeders analysis/2020-03-24-05_B_Lamed_slow.csv'
    # fname = '/Users/gonina/Library/Mobile Documents/com~apple~CloudDocs/lab/python_codes/feeders/feeders analysis/2020-04-24-08_A_Arrow_slow.csv'
    fname = '/Users/gonina/Library/Mobile Documents/com~apple~CloudDocs/lab/python_codes/feeders/feeders analysis/2020-03-20-07_B_Shin_slow.csv'
    # fname = '2020-01-20_A_train_zurik_lamed.csv'
    # fname = '2019-12-06_F_percent.csv'
    # fname = '2019-12-16_S_X.csv' #not working
    # fname = '2019-12-20_S_dot_line_train.csv'
    # fname = '2019-12-30_lior_kaf_teit_gimel_training7.csv'
    # fname = '2019-12-30_shraga_hagai_training.csv' #problem with bats_stat
    # f = pd.read_csv(fname)
    # print (f.dtypes)
   
    exp = Data(fname)
    # exp.run_fill_na()
    # exp = Data(fname)

    exp.run(bat=1) # works (choices only)
    # exp.run_prob('L reward') #works (choices only)
    # exp.run_landings_chunks(bat=1, cond= 'L reward') #works

    # print (exp.df_min_ev['bat2_loc'].head(10))
    # print (exp.df_min_ev.head(10))
    # print (exp.df_filled['bat2_loc'].unique)
    # print (exp.df_filled[exp.df_filled['bat2_loc']=='Left'])


    # exp.time_to_index()
    # exp.find_base()
    # exp.pump_score(fill_na=False) 
    # exp.match()
    # exp.fill_bat_id_gaps()
    # exp.bats_stat()
    # exp.basic_stat()
    # print (exp.df_stat)
    # print (exp.df.head())
  