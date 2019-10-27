import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.collections import PolyCollection

def read_file(fname):
    df = pd.read_csv(fname, delimiter = ',')
    df['time'] = pd.to_datetime(df['time'])
    # df['time'] = pd.to_datetime(df.time)
    # df = pd.read_csv(fname, delimiter = ',', index_col= 'time')
    # df.index = pd.to_datetime(df.index)
    return df

def time_interval (row):
    if row['condition'] == row['condition'].shift(1):
        row['start'] = row['time'].shift(1)
    #   return 'Hispanic'
    elif row['condition'] != row['condition']:
        row['start'] = row['time']
    return row
        # row['end'].shift(1) = row['start']- timedelta(milliseconds=1)
 
  


def start_end(df):
    df['start'] = df['time']
    # df['last_time'] = df['start'].shift(1)
    df['end'] = df['start'].shift(-1)
    df['prev_cond'] = df['condition'].shift(1)


   

    # df['end'] = df['time']+ timedelta(milliseconds=999)
    return df
    


def find_activity(df, freq = '15Min', base = 8):
    # activity_df_60min = df.groupby(pd.Grouper(freq='60Min', base=base, label='right'))['feeder'].value_counts()
    activity_df_15min = df.groupby(pd.Grouper(freq=freq, base=base, label='right'))['feeder'].value_counts()
    activity_df_norm = df.groupby(pd.Grouper(freq=freq, base=base, label='right'))['feeder'].value_counts(normalize=True) #precentage
    activity_df_15min = pd.DataFrame(activity_df_15min)
    activity_df_norm = pd.DataFrame(activity_df_norm)
    return activity_df_15min, activity_df_norm

def fix_save_df (df):
    df.to_csv('file')
    df = pd.read_csv('file', delimiter = ',', index_col= 'time')
    df.rename(columns={'feeder.1':'count'}, inplace=True)
    return df

# def add_cond(df, new_df):
#     new_df.where
#     new_df['cond'] = 'R'

# def get_reward_time(df):
#     r_reward = df['condition'] == 'R reward'


  
# # filtering data 
#     df.where(r_reward, inplace = True) 




# head = df.head()

# g_df = df.groupby(['signal']).count()
# group_df = df.groupby(pd.Grouper(freq='60Min', base=30, label='right')).first()
# g_df = df.groupby(['feeder', pd.Grouper(key='time',base=30, freq='H')]).sum()
# group_df = df.groupby(pd.Grouper(freq='60Min', base=8, label='right'))['signal'].value_counts()
# print (head)
# print (group_df)
# print (g_df)
# play = df['signal'].value_counts()
# print (play)

if __name__ == "__main__":
    fname = '2019-10-21_dotline.csv'
    df = read_file(fname)

    reward_df = df[df['condition']=="R reward"]
    reward_df.set_index("time", inplace=True)
    print (reward_df.head())

    

    # df = start_end(df)
    # df = df.replace("b''", np.nan) 

    # # df['start'] = df['start'].shift().where(df['condition'].shift() == df['condition'], '')
    # df['start'] = df.groupby('condition').start.shift()
    # for i in df.loc[2:3]:
    #     new_df = df.apply (lambda row: time_interval(row), axis=1)
    # cond_df = df['time']
    # # print (cond_df.head)
    # # df = df.replace("R reward", 1)
    # # df = df.replace("L reward", 2)
    # # df.time=pd.to_numeric(df.time)
    # cond_df = cond_df.dropna()
    # # cond_df = cond_df.replace("R reward", 1)
    # # cond_df.index = cond_df.index.to_pydatetime()
    # print (cond_df.head)
    # # df.condition=pd.to_numeric(df.condition)
    # # ax = cond_df.plot.barh(y= 'time')
    # # ax = cond_df.plot.barh(x='condition', y= cond_df.index)
    # # ax = cond_df.plot.barh(x=cond_df.index, y= 'condition')
    # # ax = df.loc['time', 'condition'].plot()
    # # print (df.head)
    # # ax = cond_df.plot(kind = 'barh')
    # plt.plot (cond_df)
    # plt.show()

    # print (new_df)
    # r_reward = df['condition'] == 'R reward'
    # l_reward = df['condition'] == 'L reward'
    # print (df[l_reward])
"""
    activity, activity_norm = find_activity(df, freq = '15Min', base = 8)
    activity_norm = fix_save_df(activity_norm)
    # print (activity_norm.iloc[0]['feeder'])
    # print (len(activity_norm.index))

    is_b2 = activity_norm['feeder'] == "b'2'" #filter/mask
    b2_activity = activity_norm[is_b2]
    b2_activity.rename(columns={'count':'right'}, inplace=True)
    # b2_activity.drop(['feeder'], axis=1)
    b2_activity = b2_activity.drop(columns=['feeder'])
    # print (b2_activity)

    # is_b0 = activity_norm['feeder'] == "b''" #filter/mask
    # b0_activity = activity_norm[is_b0]
    # b0_activity.rename(columns={'count':'no_action'}, inplace=True)
    # b0_activity = b0_activity.drop(columns=['feeder'])
    # # print (b0_activity)

    is_b1 = activity_norm['feeder'] == "b'1'" #filter/mask
    b1_activity = activity_norm[is_b1]
    b1_activity.rename(columns={'count':'left'}, inplace=True)
    b1_activity = b1_activity.drop(columns=['feeder'])
    # print (b1_activity)

    df_Rreward = df['condition'] == "R reward" #filter/mask
    df_Rreward = df[df_Rreward]
    print (df_Rreward)

    # new_df = pd.concat([b0_activity,b1_activity,b2_activity], axis=1, sort = True)
    new_df = pd.concat([b1_activity,b2_activity], axis=1, sort = True)
    new_df =  new_df.fillna(0)
    new_df.to_csv('feeders_prob')
    # new_df['cond'] = 'cond'
    # print (new_df)

    # df2= df.drop(columns=['signal','feeder','pump'])
    # new_df2 = pd.concat([new_df,df2], axis=1, sort = True)
    # print (new_df2)

    #plot data
    # fig, ax = plt.subplots(figsize=(15,7))
    # ax = activity_norm.plot(kind='bar',stacked=True)
    # new_df.plot(kind='bar')

    # x = np.arange(0, len(new_df.index), 10)
    #good ploting:
    # ax = new_df.plot(kind='line')
    # plt.plot(new_df.index,new_df['right'])
    # plt.xlabel('time')
    # plt.ylabel('activity (in %)')
    # plt.xticks([])   
   
    # plt.show()


 

"""