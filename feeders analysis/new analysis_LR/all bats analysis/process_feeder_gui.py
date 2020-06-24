import attr
from attr.validators import instance_of
from typing import Union
import pandas as pd
from pathlib import Path
import pathlib
import time
import numpy as np

@attr.s(frozen=True)
class BatFile:
    """File objects with path attribute and several metadata attributes.
    Instantiated by the ProcessFilelist class, passed to the ProcessData class
    Attributes: path, fname, bat ,food, sample_time, sample, sample_kind, pos_neg.
    """
    path = attr.ib(validator=instance_of(Path))
    fname = attr.ib(validator=instance_of(str))
    subj = attr.ib(validator=instance_of(int))
    date = attr.ib(validator=instance_of(str))
    env = attr.ib(validator=instance_of(int))


class ProcessFilelist:

    def __init__(self, filelist):
        self.df = None
        self.filelist = filelist
        self.invalid_files = [] ### should add invalid files output ###
        self.batdict = {} # nested dict of BatFile instances to pass forward


    def get_file_attrs(self) -> None:
        """Analizes file attributes and instantiate BatFile objects"""
        for bfile in self.filelist:
            path = Path(bfile)
            fname = path.name
            subj = int(path.parent.name.split('_')[1])
            date = path.name.split('_')[0]
            env = int(path.name.split('_')[1])
    
            if not self.assert_csv(path): # accepts only .csv files
                self.invalid_files.append(fname)
                print ('some of the files are not csv files')
                continue
            if not self.assert_not_empty(path):
                self.invalid_files.append(fname)
                print ('some of the files are empty')
                continue
            if not self.assert_format(path):
                self.invalid_files.append(fname)
                print ('some of the folders are not in the right name format')
                continue
            if not self.assert_fname(path): 
                self.invalid_files.append(fname)
                print ('some of the files not in the right name format')
                continue
            self.instantiate_bat_file(path, fname, subj, date, env)
           

    # def mass_file_to_df (self,path):
    #     bat_file = pd.read_csv(path)
        
    #     return bat_file

    def assert_csv(self, path: Path) -> bool:
        """Asserts that a file is a csv file"""
        return str.lower(path.suffix) == '.csv'

    
    def assert_format (self, path: Path) -> bool:
        """Asserts that the folder is in the right name format"""
        return 'subj' and 'bat' in path.parent.name
        

    def assert_fname (self, path: Path) -> bool:
        """Asserts that the file is in the right name format """
        return 'all_events_marked' in path.name
    

    def assert_not_empty (self, path: Path) -> bool:
        """Asserts that the file is not empty"""
        return path.stat().st_size != 0


    def instantiate_bat_file(self, path: Path, fname: str, subj: int, date: str, env: int) -> BatFile:
        """Instantiates EyeFile objects"""
        batitem = BatFile(path=path, fname=fname, subj=subj, date=date, env=env)
        try:
            self.batdict[subj][date] = batitem
        except KeyError:
            self.batdict[subj]= {date: batitem}




if __name__ == "__main__":
    # filelist =    ['/Users/gonina/Dropbox/classes/machine_learning/project/1_clio/After feeding/food/Yovel_20190513_3_neg.txt','/Users/gonina/Dropbox/classes/machine_learning/project/1_clio/After feeding/food/Yovel_20190513_3_pos.txt']
    filelist =    ['/Users/gonina/Desktop/mock data/subj_1_bat/16032020_1_all_events_marked.csv']
    files = ProcessFilelist(filelist)
    files.get_file_attrs()
    file_dict = files.batdict
    print(files.batdict)
    # # print(files.invalid_files)
    # print (file_dict['Yovel_20190513_3_neg.txt'].date)
    # sample_df = pd.DataFrame(columns=['sample_id','bat','date','sample_time',
                                        # 'food','mouth/anus', 'pos/neg'])
    # sample_df.append({'sample_id':file_dict['Yovel_20190513_3_neg.txt'].sample), 'bat':file_dict['Yovel_20190513_3_neg.txt'].bat , 'bat1_loc' : 101, 'pump_1': 1,'bat2_id' :'2A'} , ignore_index=True)
    # print(files.sample)
    # print (files.sample_df)
    # print (files.df)