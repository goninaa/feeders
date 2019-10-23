import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def read_file(fname):
    df = pd.read_csv(fname, delimiter = ',', index_col= 'time')
    df.index = pd.to_datetime(df.index)
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

    is_b0 = activity_norm['feeder'] == "b''" #filter/mask
    b0_activity = activity_norm[is_b0]
    b0_activity.rename(columns={'count':'no_action'}, inplace=True)
    b0_activity = b0_activity.drop(columns=['feeder'])
    # print (b0_activity)

    is_b1 = activity_norm['feeder'] == "b'1'" #filter/mask
    b1_activity = activity_norm[is_b1]
    b1_activity.rename(columns={'count':'left'}, inplace=True)
    b1_activity = b1_activity.drop(columns=['feeder'])
    # print (b1_activity)

    new_df = pd.concat([b0_activity,b1_activity,b2_activity], axis=1, sort = True)
    new_df =  new_df.fillna(0)
    new_df.to_csv('feeders_prob')
    # self.df_all = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)
    # print (new_df)

    #plot data
    # fig, ax = plt.subplots(figsize=(15,7))
    # ax = activity_norm.plot(kind='bar',stacked=True)
    # new_df.plot(kind='bar')

    new_df.head().plot(kind='scatter',x=new_df.index,y='left',color='red')
    plt.show()
    # # for i in activity_norm.index:
    # #     ax = activity_norm.iloc[i].plot(kind='bar')
    # plt.show()

