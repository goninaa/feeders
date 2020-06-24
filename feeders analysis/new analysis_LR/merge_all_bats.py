import pandas as pd
import numpy as np
import attr
from attr.validators import instance_of
import datetime
import time

class AllBats:
    """get list of bats AllNights and merge them to one df """
    def __init__ (self,bat_list):
        self.fname_list = bat_list
        self.df_list = []
        self.df_all_bats = None


    def fname_to_df (self):
        """ create list of df's from files names """
        for fname in self.fname_list:
            df = pd.read_csv(fname)
            self.df_list.append(df)   

    def merge_bats(self) -> None:
        """Merges all data frames in the list into one data frame"""
        basic_df = self.df_list.pop(0)
        for df in self.df_list:
            basic_df = pd.concat([basic_df, df],ignore_index=True)
        self.df_all_bats = basic_df
        self.df_all_bats.sort_values(by ='epoch', inplace=True)
        self.df_all_bats.to_csv(f"all_bats_{time.strftime('%d-%m-%Y')}.csv")

    def run (self):
        """ main pipeline """
        self.fname_to_df()
        self.merge_bats()


if __name__ == "__main__":

    bat_list = ['/Users/gonina/Library/Mobile Documents/com~apple~CloudDocs/lab/python_codes/feeders/feeders analysis/1_4nights.csv',
                '/Users/gonina/Library/Mobile Documents/com~apple~CloudDocs/lab/python_codes/feeders/feeders analysis/1_4nights.csv']
    all_bats = AllBats(bat_list=bat_list)
    all_bats.run()
