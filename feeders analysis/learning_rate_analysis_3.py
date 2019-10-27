import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as dt

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

    df_Rreward = df['condition'] == "R reward" #filter/mask
    df_Rreward = df[df_Rreward]
    print (df_Rreward)
    # df = df_Rreward

    # reward_act, reward_act_norm = find_activity(df_Rreward, freq = '15Min', base = 8) #worng
    # print (reward_act)

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
    # new_df = pd.concat([b1_activity,b2_activity], axis=1, sort = True)
    new_df =  new_df.fillna(0)
    new_df.to_csv('feeders_prob')
    # print (new_df)
    # print (df['condition'])

    # df2= df.drop(columns=['signal','feeder','pump'])
    # new_df2 = pd.concat([new_df,df2], axis=1, sort = True)
    # print (new_df2)

    #plot data
    # fig, ax = plt.subplots(figsize=(15,7))
    # ax = activity_norm.plot(kind='bar',stacked=True)
    # new_df.plot(kind='bar')

    # # x = np.arange(0, len(new_df.index), 10)
    #good ploting:
    # new_df.plot(kind='line')
    # # plt.plot(df.index,df['condition'])
    # plt.xlabel('time')
    # plt.ylabel('activity (in %)')
    # plt.xticks([]) 

    # annotata
    # x_line = datetime.fromisoformat('2019-10-20 20:23:00')
    # # ax.annotata('R reward', xy = x_line, 230000),
    # plt.axvline(x = x_line, linestyle = 'dashed', alpha = 0.5)

    # df.amin = pd.to_datetime(df.amin).astype(datetime)
    # df.amax = pd.to_datetime(df.amax).astype(datetime)
    # df.dropna(axis=0, subset=['condition'])
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax = ax.xaxis_date()
    # ax = plt.hlines(df.condition, dt.date2num(df.index), dt.date2num(df.index))

    plt.show()

   

    # # for i in activity_norm.index:
    # #     ax = activity_norm.iloc[i].plot(kind='bar')
    # plt.show()

