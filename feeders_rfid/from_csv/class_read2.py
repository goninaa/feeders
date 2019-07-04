import csv
import pandas as pd
import datetime

class DATA:

    def __init__ (self,fname):
        self.fname = fname
        self.df = pd.read_csv(self.fname).tail(n = 50)
        # self.df_len = len(self.df.index)
        self.df_last = None
        self.activity = False
        self.bat = None

    def time_index(self):
        """ add headers and convert time to datetimeIndex"""
        self.df.columns = ["A", "B", "TAG", "D", "db", "F", "time", "H", "ANTENNA", "J"]
        self.df['TIME'] = pd.to_datetime(self.df['time'])
        self.df = self.df.set_index(['TIME'])
        self.df.pop('time')

    def check_activity (self):
        """ detrmine if there been activity in the last second"""
        # now = (datetime.datetime.now())
        # ten_sec_ago = (datetime.datetime.now()- datetime.timedelta(seconds=10))
        second_ago = (datetime.datetime.now()- datetime.timedelta(seconds=1))
        self.df = self.df.last('1s')
        row_time = self.df.index.unique()
        # print (row_time)
        if row_time >= second_ago:
            self.activity = True
        else :
            self.activity = False

    def find_bat(self):
        # for now, can only read one bat
      # read where is bat
        antenna_count = self.df['ANTENNA'].value_counts()
        ant = antenna_count.idxmax()
        th = 1
        if antenna_count[ant] >= th:
            self.bat = f'bat_{ant}'
            # print (self.bat)
        else:
            self.bat = None

        # for future use:
        # antennas = self.df.ANTENNA.unique()
        # for ant in antennas:
        #     if antenna_count[ant] >= th:
        #         print (f'bat_{ant}')
                
       

    def bat_loc(self):
        # data[(data['Date'] > created_time) & (data['Date'] <datetime.datetime.utcnow())]
        # bat = False
        # th = 10
        # if len(last_sec.index) < th :
            # bat = False  # remove noise (less than th reads)
        # if df> ten_sec_ago:
        #     print ('bat')
        # else:
        #     print ('none') 
        pass      


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
    # data.time_index()
    # data.find_bat()
    # print (datetime.datetime.now())
    # print (datetime.datetime.now()- datetime.timedelta(seconds=10))
    # (datetime.datetime.now()- datetime.timedelta(microseconds=1))

    # fname = 'filename2.csv'
    # tag, antenna = read_rfid (fname)
    # if antenna == '102':
    #     print ("yes")