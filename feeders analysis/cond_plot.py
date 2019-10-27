import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def read_file(fname):
    df = pd.read_csv(fname, delimiter = ',')
    # df = pd.read_csv(fname, delimiter = ',', index_col= 'time')
    # df.index = pd.to_datetime(df.index)
    return df


if __name__ == "__main__":
    fname = '2019-10-21_dotline.csv'
    df = read_file(fname)
    cond_df = df.copy()[['time','condition']]
    cond_df['time'] = pd.to_datetime(cond_df['time'])
    # cond_df.set_index("time", inplace=True)
    # cond_df.sort_index(inplace=True)
    cond_df.sort_values(by=['time'])
    cond_df = cond_df.replace('R reward', 1) 
    cond_df = cond_df.replace('L reward', 2) 
    cond_df = cond_df.dropna()

    cond_df['condition'].plot()

    # cond_df.plot()
    # print (cond_df.time)
    # print (cond_df)
    # cond_df.plot()
