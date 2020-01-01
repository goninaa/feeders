import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.dates as md
import matplotlib.patches as mpatches

fname = '2019-12-20_S_dot_line_train.csv'
df = pd.read_csv(fname)

def match (df):
    """ add a column with y/n if value was as expected or not. later used for plotting"""
    df_score = pd.DataFrame(df.copy())
    df_score['match'] = np.where( 
                            ( (df_score['pump_1'] == '1') & (df_score['bat2_condition'] == 'L reward' ) ) 
                            | ( (df_score['pump_1'] == 'no 1') & (df_score['bat2_condition'] == 'R reward' ) )
                            | ( (df_score['pump_2'] == '2') & (df_score['bat2_condition'] == 'R reward' ))
                            | ( (df_score['pump_2'] == 'no 2') & (df_score['bat2_condition'] == 'L reward' ))
                            , 'y', 'n')
    return df_score

df_score = match(df)

# sns.scatterplot(data=df_score, x='Unnamed: 0', y='sum_pump', style='match')
print (df_score.head())