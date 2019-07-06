import csv
import pandas as pd
import datetime

# must have header
class DATA:

    def __init__ (self,fname):
        self.fname = fname
        self.df = pd.read_csv(self.fname).tail(n = 50)
        self.df_len = len(self.df.index)
        self.df_last = None

    def time_index(self):
        """ add headers and convert time to datetimeIndex"""
        self.df.columns = ["A", "B", "TAG", "D", "db", "F", "time", "H", "ANTENNA", "J"]
        self.df['TIME'] = pd.to_datetime(self.df['time'])
        self.df = self.df.set_index(['TIME'])
        self.df.pop('time')

    def read_last (self):
        now = (datetime.datetime.now())
        ten_sec_ago = (datetime.datetime.now()- datetime.timedelta(seconds=10))
        # print (tail['2018-12-02 13:37:08':'2018-12-02 13:37:08'])
        self.df = self.df.last('1s')
        self.df_len = len(self.df.index)
        
        print (self.df)
        print (self.df_len)
        # count_antenna = self.df.groupby(['TAG']).count()
        g = self.df.groupby(['TAG', 'ANTENNA']).count()
        gr = self.df.groupby(['TAG', 'ANTENNA'])
        # print (count_antenna)
        # if count_antenna['ANTENNA'] > 3:
        antenna_count = self.df['ANTENNA'].value_counts()
        # print (g.describe)
        # print (len(gr))
        th = 10
        antennas = self.df.ANTENNA.unique()
        print (antennas)
        for ant in antennas:
            if antenna_count[ant] >= th:
                print (f'bat_{ant}')
                
        # print (antenna_count.idxmax())
        # if antenna_count[102] > 7:
        #     print ('y')
        #     print (antenna_count[102])
       
       
      
        # print (tail)

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

    # def read_file2 (fname):
    #     with open(fname) as csvfile:
    #         reader = csv.DictReader(csvfile)
    #         for row in reader:
    #             tag, antenna = row['TAG'], row['ANTENNA']
    #             # print (antenna)
    #             return tag, antenna

if __name__ == "__main__":
    fname = 'test_new_02-12-18.csv'
    data = DATA(fname)
    data.time_index()
    data.read_last()
    # print (datetime.datetime.now())
    # print (datetime.datetime.now()- datetime.timedelta(seconds=10))
    # (datetime.datetime.now()- datetime.timedelta(microseconds=1))

    # fname = 'filename2.csv'
    # tag, antenna = read_rfid (fname)
    # if antenna == '102':
    #     print ("yes")