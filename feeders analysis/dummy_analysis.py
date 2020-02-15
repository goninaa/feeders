import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.dates as md
import matplotlib.patches as mpatches

df = pd.read_csv('2019-12-20_S_dot_line_train.csv_fill_gaps.csv')

def time_to_index(df):
    """change time column into datetime index"""
    df.rename(columns={'Unnamed: 0' :'time'}, inplace=True)
    df.index = pd.to_datetime(df['time'], dayfirst=True)
    df.drop(['time'], axis=1, inplace=True)

if __name__ == "__main__":
    
    time_to_index(df)
    df2 = df.resample('3T').sum()
    time_to_index(df2)
    print (df2)
    # print (df[df['pump_2']==2])


