import numpy as np
import pandas as pd
from datetime import datetime, timedelta

fname = '2019-10-21_dotline.csv'
df = pd.read_csv(fname, delimiter = ',', index_col= 'time')
df.index = pd.to_datetime(df.index)

head = df.head()

# group_df = df.groupby(pd.Grouper(freq='60Min', base=30, label='right')).first()
# g_df = df.groupby(['feeder', pd.Grouper(key='time',base=30, freq='H')]).sum()
group_df = df.groupby(pd.Grouper(freq='60Min', base=8, label='right'))['signal'].value_counts()
print (head)
print (group_df)
# play = df['signal'].value_counts()
# print (play)