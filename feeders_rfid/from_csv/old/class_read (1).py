import pandas as pd
import datetime

class DATA:

    def __init__ (self,fname):
        self.fname = fname
        self.df = pd.read_csv(self.fname).tail(n = 50)
        self.df_last = None
        self.activity = False
        self.bat = None

    def time_index(self):
        """ add headers and convert time to datetimeIndex"""
        self.df.columns = ["A", "B", "TAG", "D", "db", "F", "time", "H", "ANTENNA", "J", "K"]
        self.df['TIME'] = pd.to_datetime(self.df['time'])
        self.df = self.df.set_index(['TIME'])
        self.df.pop('time')

    def check_activity (self):
        """ detrmine if there been activity in the last second"""
        # ten_sec_ago = (datetime.datetime.now()- datetime.timedelta(seconds=10))
        second_ago = (datetime.datetime.now()- datetime.timedelta(seconds=1))
        self.df = self.df.last('1s')
        row_time = self.df.index.unique()
        # print (row_time)
        if row_time[0] >= second_ago:
            self.activity = True
        else :
            self.activity = False

    def find_bat(self):
        """ find next to which antenna the bat is"""
        # for now, can only read one bat
        antenna_count = self.df['ANTENNA'].value_counts()
        ant = antenna_count.idxmax()
        th = 1
        if antenna_count[ant] >= th:
            self.bat = f"b'{ant}'"
        else:
            self.bat = None

        # for future use:
        # antennas = self.df.ANTENNA.unique()
        # for ant in antennas:
        #     if antenna_count[ant] >= th:
        #         print (f'bat_{ant}')
                

    def write_over (self):
        """ write over the file, to save time and memory"""
        # df = pd.DataFrame()
        # df.to_csv(fname)  #write over file
        pass

    def save_bat (self):
        pass

    def run (self): 
        self.time_index()
        self.check_activity()
        if self.activity == True:
            self.find_bat()
        # self.save_bat()
        # self.write_over()


if __name__ == "__main__":
    fname = 'test_new_02-12-18.csv'
    data = DATA(fname)
    data.run()
    print (data.bat)
 