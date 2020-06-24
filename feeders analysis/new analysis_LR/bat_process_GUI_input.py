import attr
from attr.validators import instance_of
from pathlib import Path
from typing import Union

@attr.s(frozen=True)
class BatFile:
    """File object path attribute and several metadata attributes.
    Instantiated by the ProcessFilelist class, passed to the ProcessData class
    Attributes: path, fname, experiment."""
    path = attr.ib(validator=instance_of(Path))
    fname = attr.ib(validator=instance_of(str))
    date = attr.ib(validator=instance_of(str))
    tent = attr.ib(validator=instance_of(str))
    # maybe add user input...
    env = attr.ib(validator=instance_of(str))
    # bat_name = attr.ib(validator=instance_of(str))
    # tag = attr.ib(validator=instance_of(str))
    # cond (right or left)


# @attr.s
class ProcessFile:
    """Pipeline to process a list of files.
    Reads attributes from filename and creates a list of EyeFile objects to pass.
    Attributes: filelist, invalid_files, eyedict.
    Methods: instantiate_eye_file, assert_csv, extract_file_attrs.
    """
    # filelist = attr.ib(validator=instance_of(list))
    # batitem = attr.ib() #  BatFile instances to pass forward
    # invalid_files = attr.ib(default=attr.Factory(list)) ### should add invalid files output ###
    def __init__(self, filelist):
        self.filelist = filelist
        self.invalid_files = []  

    def get_file_attrs(self) -> None:
        """Analizes file attributes and instantiate BatFile objects"""
        for batfile in self.filelist:
            path = Path(batfile)
            fname = path.name
            if not self.assert_csv(path): # accepts only .csv files
                self.invalid_files.append(fname)
                continue

            fattrs = self.extract_file_attrs(fname)
            if not fattrs: # accepts files only if named in the appropriate pattern
                self.invalid_files.append(fname)
                continue
            date, tent = fattrs[0], fattrs[1]

            if 'slow' in fname:
                env = 'slow'
            elif 'fast' in fname:
                env = 'fast'
            elif 'test' in fname:
                env = 'test'
            else: # accepts only slow, fast or test files
                self.invalid_files.append(fname)
                continue
            self.instantiate_bat_file(path, fname, date, tent, env)

    def assert_csv(self, path: Path) -> bool:
        """Asserts that a file is a csv file"""
        return str.lower(path.suffix) == '.csv'

    def extract_file_attrs(self, fname: str) -> Union[list, bool]:
        """If the file named appropriately, extracts its attributes from filename"""
        fattrs = fname.split('_')
        # return fattrs if len(fattrs) == 10 else False
        return fattrs

    def instantiate_bat_file(self, path: Path, fname: str, date: str, tent: str, env: str) -> BatFile:
        """Instantiates BatFile objects"""
        self.batitem = BatFile(path=path, fname=fname, date=date, tent=tent, env=env) #to add user input too


    



if __name__ == "__main__":
    # filelist =    ['/Users/gonina/Dropbox/classes/machine_learning/project/1_clio/After feeding/food/Yovel_20190513_3_neg.txt','/Users/gonina/Dropbox/classes/machine_learning/project/1_clio/After feeding/food/Yovel_20190513_3_pos.txt']
    filelist =    ['/Users/gonina/Library/Mobile Documents/com~apple~CloudDocs/lab/python_codes/feeders/feeders analysis/2020-03-20-07_B_Shin_slow.csv']
    files = ProcessFile(filelist)
    files.get_file_attrs()
    
    print(files.batitem)