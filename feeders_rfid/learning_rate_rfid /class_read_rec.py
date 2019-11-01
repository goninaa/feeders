import pandas as pd
import datetime

class DATA:

    def __init__ (self,fname):
        self.fname = fname    
        self.df = pd.read_csv(self.fname).tail(n = 50)
        self.df_last = None
        self.activity = False
        self.bat = "no_bat"
        self.bat_id_1 = None
        self.bat_id_2 = None
        self.beacon = "307410CD2C040B4000000001"

    def time_index(self):
        """ add headers and convert time to datetimeIndex"""
        self.df.columns = ["A", "B", "TAG", "D", "db", "F", "time", "H", "ANTENNA", "J"]
        self.df['TIME'] = pd.to_datetime(self.df['time'])
        self.df = self.df.set_index(['TIME'])
        self.df.pop('time')

    def check_activity (self):
        """ detrmine if there been activity in the last second"""
        # ten_sec_ago = (datetime.datetime.now()- datetime.timedelta(seconds=10))
        th_seconds = 3
        second_ago = (datetime.datetime.now()- datetime.timedelta(seconds=th_seconds))
        # second_ago = (datetime.datetime.utcnow()- datetime.timedelta(seconds=th_seconds))
        self.df = self.df.last('1s')
        row_time = self.df.index.unique()
        # print (row_time[0])
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
            # self.find_bat_id()
            # self.bat_id = self.df['TAG']
        else:
            self.bat = "no_bat"
            # self.bat_id_1 = "no bat"
            # self.bat_id_2 = "no bat"

    def find_bat_id (self):
        # self.df = self.df.last('1s')
        last_bat = self.df.tail(1)
        unique_bats  = last_bat['TAG'].unique()
        if (len(unique_bats)) == 1 and (last_bat['TAG'].unique()[0] != self.beacon): 
            self.bat_id_1 = last_bat['TAG'].unique()
        # elif len(unique_bats) == 2:
        #     if last_bat['TAG'].unique()[0] != self.beacon: 
        #         self.bat_id_1 = last_bat['TAG'].unique()[0]
        #     if last_bat['TAG'].unique()[1] != self.beacon:
        #         self.bat_id_2 = last_bat['TAG'].unique()[1]
        

    # def remove_beacon (self):
    #     if self.bat_id_1 == self.beacon:
    #         self.bat_id_1 == "no bat"
    #     elif self.bat_id_2 ==  self.beacon:
    #         self.bat_id_2 == "no bat"
        # print (self.bat_id)



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
            self.find_bat_id()
            if self.bat_id_1 != "no bat" and self.bat_id_1 != None :
                self.find_bat()
        else:
            self.bat = 'no_bat'
        # self.save_bat()
        # self.write_over()


if __name__ == "__main__":
    fname = 'test_28-10-19.csv'
    data = DATA(fname)
    data.run()
    # print (data.bat)
 