import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.dates as md
import matplotlib.patches as mpatches

def create_one_side_df (activity_df):
    activity_df = pd.read_csv('activity')
    activity_df.rename(columns={"feeder.1": "activity"}, inplace=True)
    activity_df['time'] = pd.to_datetime(activity_df['time'])
    is_b2 = activity_df['feeder'] == "b'2'" #filter/mask
    right_sec_df = activity_df[is_b2]
    is_b1 = activity_df['feeder'] == "b'1'" #filter/mask
    left_sec_df = activity_df[is_b1]
    return right_sec_df, left_sec_df

def plot_learning(one_side_df, condition_start_end, df_min):
    fig = plt.figure(figsize=(10,10))
    figtemp, ax = plt.subplots(1, 1)
    plt.style.use('seaborn')
    right_activity = plt.plot_date(df['time'], df['activity'], linestyle='solid', label = 'Right feeder activity')

    plt.ylabel('Time spend on right feeder (in sec)')
    # Set time format and the interval of ticks (every 15 minutes)
    xformatter = md.DateFormatter('%H:%M')
    xlocator = md.MinuteLocator(interval = 60)
    # Set xtick labels to appear every 60 minutes
    ax.xaxis.set_major_locator(xlocator)
    ## Format xtick labels as HH:MM
    plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
    # rotate_labels...
    for label in ax.get_xticklabels():
        label.set_rotation(40)
        label.set_horizontalalignment('right')

    cond_dict = {'unknown': 'y', 'R reward': 'g', 'L reward': 'r'}
    for min_time,max_time in condition_start_end:
        cond = df_min.loc[min_time]['condition']
        plt.axvspan(min_time, max_time, alpha=0.2, color=cond_dict[cond])
    act_label = ax.legend(['Right feeder activity'])
    ax = plt.gca().add_artist(act_label)
    g_patch = mpatches.Patch(color='g', label='R reward')
    r_patch = mpatches.Patch(color='r', label='L reward')
    plt.legend(handles=[g_patch,r_patch], loc='upper right')
    plt.show()


if __name__ == "__main__":
    right_sec_df, left_sec_df = create_one_side_df ('activity_10Min.csv')   
    # plot_learning(right_sec_df, condition_start_end, df_min)