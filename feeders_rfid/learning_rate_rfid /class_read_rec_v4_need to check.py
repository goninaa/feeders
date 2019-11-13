import pandas as pd
import datetime

class DATA:

    def __init__ (self,fname):
        self.fname = fname    
        self.df = pd.read_csv(self.fname).tail(n = 50)
        self.df_last = None
        self.activity = False
        self.bat = "no_bat"
        self.loc_bat1 = None
        self.loc_bat2 = None
        self.bat_id_1 = None
        self.bat_id_2 = None
        self.beacon = '307410CD2C02D58000000001'
        self.tag1 = '307410CD2C02D9C000000001' #D9
        self.tag2 = '307410CD2C040B4000000001' #B4

    def time_index(self):
        """ add headers and convert time to datetimeIndex"""
        self.df.columns = ["A", "B", "TAG", "D", "db", "F", "time", "H", "ANTENNA", "J"]
        self.df['TIME'] = pd.to_datetime(self.df['time'])
        self.df = self.df.set_index(['TIME'])
        self.df.pop('time')

    def check_activity (self):
        """ detrmine if there been activity in the last second"""
        ten_sec_ago = (datetime.datetime.now()- datetime.timedelta(seconds=10)) ##changed
        th_seconds = 1 ##changed
        second_ago = (datetime.datetime.now()- datetime.timedelta(seconds=th_seconds))
        # second_ago = (datetime.datetime.utcnow()- datetime.timedelta(seconds=th_seconds))
        self.df = self.df.last('1s')
        row_time = self.df.index.unique()
        # print (row_time[0])
        if row_time[0] >= second_ago:
            self.activity = True
        elif row_time[0] >= ten_sec_ago and row_time[0] < second_ago: ##changed
            self.activity = "bat in last 10" ##changed
        else:
            self.activity = False  #false only if was no bat for 10 sec

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

    # def find_bat_id (self):  #option without knowing tags
    #     # self.df = self.df.last('1s')
    #     # last_bat = self.df.tail(1)
    #     last_bats = self.df.tail(5)
    #     unique_bats  = last_bats['TAG'].unique()
    #     if (len(unique_bats)) == 1 and (unique_bats[0] != self.beacon): 
    #         self.bat_id_1 = unique_bats[0]
    #     elif len(unique_bats) > 1:
    #     # elif len(unique_bats) == 2:
    #         if unique_bats[0] != self.beacon: 
    #             self.bat_id_1 = unique_bats[0]
    #         if unique_bats[1] != self.beacon:
    #             self.bat_id_2 = unique_bats[1]

    def find_bat_id (self):
        """ find id and location for more than one bat, acording to known tags"""
        # self.df = self.df.last('1s')
        # last_bat = self.df.tail(1)
        try:
            if len(self.df) >= 1 & len(self.df) <=5 :
                last_bats = self.df.tail(len(self.df))
            elif len(self.df) > 5:
                last_bats = self.df.tail(5)
            elif len(self.df) < 1:
                print ("error")
            unique_bats  = last_bats['TAG'].unique()
            # print (f"unique {unique_bats[0]}")
            # print (len(unique_bats))
            if self.tag1 in unique_bats:
                self.bat_id_1 = self.tag1
                bat1 = last_bats['TAG'] == self.tag1
                self.loc_bat1 = last_bats[bat1]['ANTENNA'].tail(1)[0]
                # print (last_bats[bat1]['ANTENNA'])
            if self.tag2 in unique_bats:
                self.bat_id_2 = self.tag2
                bat2 = last_bats['TAG'] == self.tag2
                self.loc_bat2 = last_bats[bat2]['ANTENNA'].tail(1)[0]
                # print (last_bats[bat2]['ANTENNA'])
                    
        except:
            print ("some error")


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
        # print ('checking data') 
        self.time_index()
        self.check_activity()
        if self.activity == True:
            self.find_bat_id()
            # if self.bat_id_1 != "no bat" and self.bat_id_1 != None:
            #     self.find_bat()
            # and self.bat_id_2 != "no bat" and self.bat_id_2 != None
        elif self.activity == False:
        # else:
            self.bat = 'no_bat'
        # print (self.activity)
        # self.save_bat()
        # self.write_over()


if __name__ == "__main__":
    fname = 'test_28-10-19.csv'
    data = DATA(fname)
    data.run()
    # print (data.bat)
 