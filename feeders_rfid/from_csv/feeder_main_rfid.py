import serial
import time
import numpy as np
import pandas as pd
from datetime import date
import csv
from stereo import *  # playing files import
from class_read import *

com_pump = 'COM1'
pump = serial.Serial(com_pump, 9600, timeout=1) # pump

class Feeder:

    def __init__(self, fname):
        self.df_signal = pd.DataFrame(columns=['signal'])
        self.df_feeder = pd.DataFrame(columns=['feeder'])
        self.df_pump = pd.DataFrame(columns=['pump'])
        self.disconnect = []
        self.df_all = pd.concat([self.df_signal, self.df_feeder, self.df_pump], axis=1, sort = True)
        # self.msg = "first msg"
        self.bat = False
        self.fname = fname
        self.bat_loc = "no_bat"


    def signal_on (self, intervals = 20):
        """ intervals = 20 sec between signals"""
        while self.bat == False:
            signals = stereo('left_sig.wav', 'right_sig.wav')
            print (f"{pd.Timestamp.now()} playing signal")
            self.df_signal.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 'play'
            df = pd.concat([self.df_signal, self.df_feeder, self.df_pump], axis=1, sort = True)
            df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
            # print (df)
            signals.run()  # play signals from both feeders
            flag_t = 0
            t_end = time.time()+intervals
            while time.time() < t_end:
                self.read_rfid()
                self.decide()
                if self.bat == True and flag_t == 0:
                    self.which_pump()
                    flag_t += 1
            if self.bat == True:
                break

    def read_rfid (self):
            data = DATA(self.fname)
            data.run()
            self.bat_loc = data.bat

            self.df_feeder.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = self.bat_loc
            df = pd.concat([self.df_signal, self.df_feeder, self.df_pump], axis=1, sort = True)
            df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
            print(self.bat_loc) 
            self.decide()


    def pump_it (self, pump_id):
        global pump

        try:
            # val = np.random.choice(2, 1, p=[0.6, 0.4])
            val = 0 # val always = 0
            if(val == 0):
                pump.write([pump_id])
                self.df_pump.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = pump_id
                df = pd.concat([self.df_signal, self.df_feeder, self.df_pump], axis=1, sort = True)
                df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
            else:
                self.df_pump.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 'no {}'.format(pump_id)
                df = pd.concat([self.df_signal, self.df_feeder, self.df_pump], axis=1, sort = True)
                df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")

        except serial.SerialException as e:
            self.dis_time()
            try:
                if(pump.isOpen()):
                    pump.close()
                pump = serial.Serial(com_pump, 9600, timeout=1)  # pump
                time.sleep(3)
                print("restart")
            except serial.SerialException as e2:
                self.dis_time()
                print("I couldnt open the port jesus!!!")


    def decide (self):
        """check if bat true or false"""
        if (self.bat_loc == "b'101'") or (self.bat_loc == "b'102'"):  # reads bats
            self.bat = True
        elif self.bat_loc == "no_bat": # if reads "no bat"
            search_t = 10 #search time
            t_end = time.time()+search_t
            while time.time() < t_end:
                self.read_rfid()
                if (self.bat_loc == "b'101'") or (self.bat_loc == "b'102'"):
                    break
            if self.bat_loc == "no_bat" and time.time() > t_end:
                self.bat = False

    def which_pump (self):
        """decide which pump to use"""
        if self.bat_loc == "b'101'":
            self.pump_it(1)
            # self.pump_it(1)
            # self.pump_it(1)
            # self.pump_it(1)
            # self.pump_it(1)
        elif self.bat_loc == "b'102'":
            self.pump_it(2)
            # self.pump_it(2)
            # self.pump_it(2)
            # self.pump_it(2)
            # self.pump_it(2)

    def dis_time (self):
        """ return current time to self.disconnect"""
        current_time = time.localtime()  # get struct_time
        time_string = time.strftime("%m/%d/%Y, %H:%M:%S", current_time)
        self.disconnect.append(time_string)
        with open("disconnect.txt", "w") as text_file:
            print(self.disconnect, file=text_file)

    def clean (self, pumps=1):
        self.pump_it(1)
        self.pump_it(1)
        self.pump_it(1)
        self.pump_it(1)
        self.pump_it(1)
        self.pump_it(1)
        self.pump_it(1)
        self.pump_it(1)
        self.pump_it(1)
        self.pump_it(1)
        self.pump_it(2)
        self.pump_it(2)
        self.pump_it(2)
        self.pump_it(2)
        self.pump_it(2)
        self.pump_it(2)
        self.pump_it(2)
        self.pump_it(2)
        self.pump_it(2)
        self.pump_it(2)

    def run (self):
        """main"""
        while True:
            self.read_rfid()
            time.sleep(1)
            self.signal_on()

    def find_bat (self):
        data = DATA(self.fname)
        data.run()
        self.bat_loc = data.bat


if __name__ == "__main__":
    filename = date.today().strftime("%d-%m-%Y")
    fname = f"test_{filename}.csv"   #date of today

    feeder = Feeder(fname)
    


    while True:
        try:
            feeder.run()
            time.sleep(1)
        except:
            feeder.run()
            time.sleep(1)
        # f = feeder.signal_on()
        # print (f)
        #  feeder.pump_it(1)
        #time.sleep(4)
        #feeder.pump_it(1) #left
        #time.sleep(4)
        #feeder.pump_it(2)  # right
      #
        # read = feeder.read_ir()
        # print (read)
    # feeder.clean(1)









     






