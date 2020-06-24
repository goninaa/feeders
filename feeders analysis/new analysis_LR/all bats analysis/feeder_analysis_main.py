from feeder_analysis_GUI import *
from process_feeder_gui import *
from B_combine_4_nights import *
from C_merge_all_bats import *
# from read_mass_data import *


@attr.s
class BatsData:
    """Mass data base builder tool.
    Attributes: user_input, massdict, df_list, b_data.
    Methods:
    method input() prompts for user input.
    method read_data() creates raw data objects for each file.
    method data() converts data of each trail to a pd.Dataframe.
    method big_data() creates one big pd.DataFrame from all data frames of a given experiment.
    method run() is the main function for this process.
    """
    user_input = attr.ib(default=csv_GUI)
    batdict = attr.ib(default=attr.Factory(dict))
    df_list = attr.ib(default=attr.Factory(list))
    invalid_files = attr.ib(default=attr.Factory(list)) #new
    missing_data = attr.ib(default=attr.Factory(list)) #new
    # b_data = attr.ib(default=AllId)
    
        
    def input(self) -> bool:
        """prompts for user input"""
        user_input = csv_GUI()
        assert_input = user_input.run()
        if not assert_input:
            return False
        self.user_input = user_input
        return True
    
    def raw_data(self) -> None:
        """creates raw data objects for each file"""
        filelist = ProcessFilelist(self.user_input.filelist)
        filelist.get_file_attrs()
        self.batdict = filelist.batdict
        self.invalid_files = filelist.invalid_files 


    def data(self) -> None:
        """creates a 4nights df for each bat in batdict and add it to the df_list"""
        
        for key, value in self.batdict.items():
            try:
                val1, val2, val3, val4 = value.values()
            except ValueError:
                self.missing_data.append(key)
                continue
            data = AllNights(nights_list=[val1.path, val2.path,val3.path,val4.path],subj=val1.subj,env=val1.env)
            data.run()
            self.df_list.append(data.df_nights)
            print (data.df_nights)

    
    def big_data(self) -> None:
        """creates one big data frame from all data frames in the df_list"""
        b_data = AllBats (self.df_list)
        b_data.run()
        self.b_data = b_data

    def invalid_files_list (self):
        print (f'invalid files: {self.invalid_files}')
        with open('invalid files.txt', 'w') as f:
            for item in self.invalid_files:
                f.write("%s\n" % item)

    def missing_data_list (self):
        print (f'missing data: {self.missing_data}')
        with open('missing data.txt', 'w') as f:
            for item in self.missing_data:
                f.write("%s\n" % item)


    def run(self) -> bool:
        """main function to run the process"""
        if not self.input():
            print('Cancelling...')
            return False
        print('Collecting files...')
        self.raw_data()
        print('Reading files...')
        self.data()
        print('Building dataframe...')
        self.big_data()
        print('Analyzing...')
        self.invalid_files_list()
        self.missing_data_list()
        print('Done.')
        # return True

if __name__ == "__main__":
    BatsData().run()