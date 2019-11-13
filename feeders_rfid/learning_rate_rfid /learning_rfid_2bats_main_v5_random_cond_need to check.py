import serial
import time
import numpy as np
import pandas as pd
import csv
from datetime import date
from pathlib import Path
from stereo_one_signal_v2 import *  # playing files import
from class_read_rec_v4 import *

com_pump = '/dev/ttyUSB0'
pump = serial.Serial(com_pump, 9600, timeout=1) # pump

class Feeder:

    def __init__(self, fname):
        self.df = pd.DataFrame(columns=['signal','bat1_id','bat1_loc','pump_1','bat1_condition',
                                        'bat2_id','bat2_loc','pump_2','bat2_condition'])
        self.disconnect = []
        # self.bat = False
        # self.cond = None
        self.fname = fname
        # self.bat_loc = "no_bat"
        self.bat1_id = None
        self.bat2_id = None
        self.loc_bat1 = "no_bat"
        self.loc_bat2 = "no_bat"
        self.activity = False
        # self.bat1_cond = ''
        # self.bat2_cond = ''


    def signal_on_reward (self, rewarding_feeder = 'R', intervals = 20, running_time = 3200, R_p=(1,0), L_p=(1,0)):
        """ intervals = 20 sec between signals"""
        print (rewarding_feeder)
        self.cond = (f'{rewarding_feeder} reward')
        tr_end = time.time() + running_time
        while time.time() < tr_end:
            if time.time() >= tr_end:
                break
            self.read_rfid()
            time.sleep(0.5)
            while self.activity == False:
                if time.time() >= tr_end:
                    break
                signals = stereo('learning_rate_rfid /left_sig.wav', 'learning_rate_rfid /left_sig.wav')
                signals.run()  # play signals from both feeders
            
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'signal'] = 'play'
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_condition'] = self.cond
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_condition'] = self.cond
                self.df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")

                # print (df)
                print (f"{pd.Timestamp.now()} playing signal")
                print (self.cond)
                flag_t = 0
                t_end = time.time()+intervals
                while time.time() < t_end:
                    if time.time() >= tr_end:
                        break
                    self.read_rfid()
                    # time.sleep(3)
                    # self.decide()
                    time.sleep(0.5)
                    if self.activity == True and flag_t == 0:
                        self.which_pump(R_p, L_p)
                        flag_t += 1
                if self.activity == True:
                    break


    def read_rfid (self):
            # print ("read rfid")
            # print (self.bat_loc)
            data = DATA(self.fname)
            data.run()
            self.activity = data.activity
            self.bat1_id = data.bat_id_1 
            self.bat2_id = data.bat_id_2
            self.loc_bat1 = data.loc_bat1
            self.loc_bat2 = data.loc_bat2
            
            self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_id'] = self.bat1_id
            self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_id'] = self.bat2_id
            self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_loc'] = self.loc_bat1
            self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_loc'] = self.loc_bat2
            self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_condition'] = self.cond
            self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_condition'] = self.cond
            self.df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
            # print(self.bat_loc) 
            # self.decide()


    def pump_it (self, pump_id, win_lose_p = (1,0)):
        """pump from selected pump with the selected probability"""
        global pump

        try:
            choice_arr = ["win", "lose"]
            val = np.random.choice(choice_arr, 1, p=win_lose_p)
            if(val == "win"):
                pump.write([pump_id])
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_id'] = self.bat1_id
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_id'] = self.bat2_id
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_loc'] = self.loc_bat1
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_loc'] = self.loc_bat2
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_condition'] = self.cond
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_condition'] = self.cond
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),f'pump_{pump_id}'] = pump_id
                self.df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
                print ("pumping")
            else:
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_id'] = self.bat1_id
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_id'] = self.bat2_id
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_loc'] = self.loc_bat1
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_loc'] = self.loc_bat2
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_condition'] = self.cond
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_condition'] = self.cond
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),f'pump_{pump_id}'] = 'no {}'.format(pump_id)
                self.df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
                print ("no luck!")

        except serial.SerialException as e:
            self.fix_pump_ir

    # def decide (self):
    #     """check if bat true or false"""
    #     # print ("decide where bat is")
    #     if (self.bat_loc == "b'101'") or (self.bat_loc == "b'102'"):  # reads bats
    #         self.bat = True
    #     elif self.bat_loc == "no_bat": # if reads "no bat"
    #         search_t = 10 #search time
    #         t_end = time.time()+search_t
    #         while time.time() < t_end:
    #             self.read_rfid()
    #             time.sleep(0.5)
    #             if (self.bat_loc == "b'101'") or (self.bat_loc == "b'102'"):
    #                 break
    #         if self.bat_loc == "no_bat" and time.time() > t_end:
    #             self.bat = False

    def which_pump (self, R_p=(1,0), L_p=(1,0)): 
        """decide which pump to use. 
            right feeder with probability of 0.8
            left feeder probability 0.2"""
        # if 101 in [self.loc_bat1, self.loc_bat2]:
        if self.loc_bat1 == 101 or self.loc_bat2 == 101: #left pump
            self.pump_it(pump_id = 1, win_lose_p = L_p)
        if self.loc_bat1 == 102 or self.loc_bat2 == 102: #right pump
            self.pump_it(pump_id = 2, win_lose_p = R_p)
        
    def fix_pump_ir (self):
        """restart pump in case of disconnection """
        global pump
        self.dis_time()
        try:
            if(pump.isOpen()):
                pump.close()
            time.sleep(3)
            print("restart")
        except serial.SerialException as e2:
            self.dis_time()
            print("I couldnt open the port jesus!!!")

    def dis_time (self):
        """ return current time to self.disconnect"""
        current_time = time.localtime()  # get struct_time
        time_string = time.strftime("%m/%d/%Y, %H:%M:%S", current_time)
        self.disconnect.append(time_string)
        with open("disconnect.txt", "w") as text_file:
            print(self.disconnect, file=text_file)

    def clean (self, pumps=10):
        """function for cleaning fedders between uses"""
        for i in range (pumps):
            self.pump_it(1)
            time.sleep(2)
            self.pump_it(2)
            time.sleep(2)

    def run (self, intervals = 20, running_time= 3600, cond1_R_p=(0.8,0.2), cond1_L_p=(0.2,0.8), cond2_R_p=(0.2,0.8), cond2_L_p=(0.8,0.2)):
        """main- alternate randomly between conditions every x time"""
        conds = ["cond1", "cond2"]
        cond_val = np.random.choice(conds, 1, p=(0.5,0.5))
        if (cond_val == "cond1"):
            self.signal_on_reward(rewarding_feeder = 'R', intervals = intervals, running_time = running_time, R_p=cond1_R_p, L_p=cond1_L_p) # cond1
        elif (cond_val == "cond2"):
            self.signal_on_reward(rewarding_feeder = 'equal', intervals = intervals, running_time = running_time, R_p=cond2_R_p, L_p=cond2_L_p) #cond2
            # self.signal_on_reward(rewarding_feeder = 'L', intervals = intervals, running_time = running_time, R_p=cond2_R_p, L_p=cond2_L_p) #cond2
        
       # self.signal_on_reward(rewarding_feeder = 'L', intervals = intervals, running_time = running_time, R_p=cond2_R_p, L_p=cond2_L_p) #cond2
       
if __name__ == "__main__":
    filename = date.today().strftime("%d-%m-%y")
    fname = f"test_{filename}.csv"
    feeder = Feeder(fname)

    # variables:
    intervals = 20 # between signals (in sec)
    running_time = 3600 # running time of each condition (in sec)
    cond1_R_p=(0.8,0.2) # right feeder win-lose p in cond1
    cond1_L_p=(0.2,0.8) # left win-lose p in cond1
    cond2_R_p=(0.5,0.5) # right win-lose p in cond2
    cond2_L_p=(0.5,0.5) # left win-lose p in cond2

    #feeder.cond = 'R'
    #feeder.clean(60)
        
    # feeder.cond = 'R'
    # read = feeder.read_rfid()

    while True:
        feeder.run(intervals, running_time, cond1_R_p, cond1_L_p, cond2_R_p, cond2_L_p)
    
        # feeder.cond = 'R'
    # read = feeder.read_rfid()
    # print (read)
        # f = feeder.signal_on()
        # print (f)
        # feeder.pump_it(1)
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
        # read = feeder.read_rfid()
        # print (read)
    # feeder.clean(1)









     






