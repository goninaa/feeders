import serial
import time
import numpy as np
import pandas as pd
import csv
from datetime import date
from stereo_one_signal import *  # playing files import
from class_read import *

com_pump = 'COM3'
pump = serial.Serial(com_pump, 9600, timeout=1) # pump

class Feeder:

    def __init__(self):
        self.df_signal = pd.DataFrame(columns=['signal'])
        self.df_feeder = pd.DataFrame(columns=['feeder'])
        self.df_pump = pd.DataFrame(columns=['pump'])
        self.df_cond = pd.DataFrame(columns=['condition'])
        self.disconnect = []
        self.df_all = pd.concat([self.df_signal, self.df_feeder, self.df_pump, self.df_cond], axis=1, sort = True)
        self.bat = False
        self.cond = None
        self.fname = fname
        self.bat_loc = "no_bat"


    def signal_on_reward (self, intervals = 20, running_time = 3200, R_p=(1,0), L_p=(1,0)):
        """ intervals = 20 sec between signals"""
        tr_end = time.time() + running_time
        while time.time() < tr_end:
            if time.time() >= tr_end:
                break

            while self.bat == False:
                if time.time() >= tr_end:
                    break
                signals = stereo('left_sig.wav', 'right_sig.wav')
                self.df_cond.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = self.cond
                print (f"{pd.Timestamp.now()} playing signal")
                self.df_signal.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 'play'
                df = pd.concat([self.df_signal,self.df_feeder, self.df_pump, self.df_cond], axis=1, sort = True)
                df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
                # print (df)
                print (self.cond)
                signals.run()  # play signals from both feeders
                flag_t = 0
                t_end = time.time()+intervals
                while time.time() < t_end:
                    if time.time() >= tr_end:
                        break
                    self.read_rfid()
                    self.decide()
                    if self.bat == True and flag_t == 0:
                        self.which_pump_reward(R_p, L_p)
                        flag_t += 1
                if self.bat == True:
                    break


    def read_rfid (self):
            data = DATA(self.fname)
            data.run()
            self.bat_loc = data.bat

            self.df_feeder.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = self.bat_loc
            self.df_cond.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = self.cond
            df = pd.concat([self.df_signal,self.df_feeder, self.df_pump, self.df_cond], axis=1, sort = True)
            df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
            print(self.bat_loc) 
            self.decide()

    def pump_it (self, pump_id, win_lose_p = (1,0)):
        """pump from selected pump with the selected probability"""
        global pump

        try:
            choice_arr = ["win", "lose"]
            val = np.random.choice(choice_arr, 1, p=[win_lose_p])
            # val = 0 # val always = 0
            if(val == "win"):
                pump.write([pump_id])
                print ("pumping")
                self.df_pump.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = pump_id
                self.df_cond.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = self.cond
                df = pd.concat([self.df_signal,self.df_feeder, self.df_pump, self.df_cond], axis=1, sort = True)
                df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
            else:
                self.df_pump.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 'no {}'.format(pump_id)
                self.df_cond.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = self.cond
                df = pd.concat([self.df_signal, self.df_feeder, self.df_pump, self.df_cond], axis=1, sort = True)
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

    def which_pump_reward (self, R_p=(1,0), L_p=(1,0)):
        """decide which pump to use. 
            right feeder with probability of 0.8
            left feeder probability 0.2"""
        if self.msg == b'1': #left pump
            self.pump_it(pump_id = 1, L_p = L_p)
        elif self.msg == b'2': #right pump
            self.pump_it(pump_id = 2, R_p = R_p)
          

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


    def r_reward(self, intervals = 20, running_time= 3600, R_p=(0.8,0.2), L_p=(0.2,0.8)):
        """ running r_reward condition for n running time (in sec)"""
        print('R')
        self.cond = 'R reward'
        self.df_cond.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 'R reward'
        self.read_rfid()
        self.signal_on_reward(intervals, running_time, R_p, L_p)
        

    def l_reward(self, intervals = 20, running_time= 3600, R_p=(0.2,0.8), L_p=(0.8,0.2)):
        """ running l_reward condition for n running time (in sec)"""
        print ('L')
        self.cond = 'L reward'
        self.df_cond.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 'L reward'
        self.read_rfid()
        self.signal_on_reward(intervals = intervals, running_time = running_time)

    def run (self, intervals = 20, running_time= 3600, cond1_R_p=(0.8,0.2), cond1_L_p=(0.2,0.8), cond2_R_p=(0.2,0.8), cond2_L_p=(0.8,0.2)):
        """main- alternate between conditions"""
        self.r_reward(intervals = intervals, running_time = running_time, R_p=cond1_R_p, L_p=cond1_L_p) # cond1
        self.l_reward(intervals = intervals, running_time = running_time, R_p=cond2_R_p, L_p=cond2_L_p) #cond2
       
if __name__ == "__main__":
    feeder = Feeder()
    # variables:
    intervals = 20 # between signals (in sec)
    running_time = 3600 # running time of each condition (in sec) 
    cond1_R_p=(0.8,0.2) # right feeder win-lose p in cond1
    cond1_L_p=(0.2,0.8) # left win-lose p in cond1
    cond2_R_p=(0.2,0.8) # right win-lose p in cond2
    cond2_L_p=(0.8,0.2) # left win-lose p in cond2

    while True:
        feeder.run( intervals, running_time, cond1_R_p, cond1_L_p, cond2_R_p, cond2_L_p)
        # f = feeder.signal_on()
        # print (f)
        #feeder.pump_it(1)
        # time.sleep(2)
       # feeder.pump_it(1) #left
       # time.sleep(2)
       # feeder.pump_it(2)  # right
       # time.sleep(2)
       #  feeder.pump_it_20(1) #left
       #  time.sleep(2)
       #  feeder.pump_it_80(2)  # right
       #  time.sleep(2)
      #
        # read = feeder.read_ir()
        # print (read)
    # feeder.clean(1)









     






