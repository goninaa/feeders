import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def read_file(fname):
    df = pd.read_csv(fname, delimiter = ',', index_col= 'time')
    df.index = pd.to_datetime(df.index)
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

    head = df.head()    
    group_df = df.groupby(pd.Grouper(freq='60Min', base=8, label='right'))['signal'].value_counts()
    activity_df = df.groupby(pd.Grouper(freq='60Min', base=8, label='right'))['feeder'].value_counts()
    activity_df_15min = df.groupby(pd.Grouper(freq='15Min', base=8, label='right'))['feeder'].value_counts()
    activity_df_norm = df.groupby(pd.Grouper(freq='15Min', base=8, label='right'))['feeder'].value_counts(normalize=True) #precentage
   
    # print (head)
    # print (group_df)
    # print (activity_df) #good
    print (activity_df_15min)
    print (activity_df_norm)
    
    #plot data
    # fig, ax = plt.subplots(figsize=(15,7))
    # data.groupby(['date','type']).count()['amount'].plot(ax=ax)
    # activity_df_15min.plot(ax=ax) # wrong
    # ax = activity_df_15min.plot(kind='bar')
    # plt.show()
  


