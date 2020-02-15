import serial
import time
import numpy as np
import pandas as pd
import csv
from datetime import date
from pathlib import Path
from stereo_one_signal_v2 import *  # playing files import
from B_class_read_rec_v6 import *

#104 right, 103, left
# com_pump = '/dev/ttyUSB0'
# pump = serial.Serial(com_pump, 9600, timeout=1) # pump

#new
# new_port = '/dev/ttyS4'
#new_port = '/dev/ttyUSB1'
new_port =  '/dev/ttyUSB2'
new_pump = serial.Serial(port=new_port, baudrate=9600)
pumpamount = 254 # can be 1 - 254 , 254=1 ml
pump_1 = bytearray([1,pumpamount])
pump_2 = bytearray([2,pumpamount])

# new_pump.isOpen()
# new_pump.write(pump_1)
# new_pump.write(pump_2)
# new_pump.flush()
# data_raw = new_pump.readline()
# print(data_raw)


class Feeder:

    def __init__(self, fname, bat_name):
        self.df = pd.DataFrame(columns=['signal','bat1_id','bat1_loc','bat1_condition',
                                        'pump_1','pump_2', 'bat2_id','bat2_loc','bat2_condition'])
        self.disconnect = []
        # self.bat = False
        # self.cond = None
        self.fname = fname
        self.bat_name = bat_name
        # self.bat_loc = "no_bat"
        self.bat1_id = None
        self.bat2_id = None
        self.loc_bat1 = "no_bat"
        self.loc_bat2 = "no_bat"
        self.activity = False
        # self.bat1_cond = ''
        # self.bat2_cond = ''
        self.pumpamount = 200 # can be 1 - 254


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
                # signals.run()  # play signals from both feeders
                signals.play_right() #play only on tent B
            
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'signal'] = 'play'
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_condition'] = self.cond
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_condition'] = self.cond
                self.df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}_{self.bat_name}.csv")

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
                if self.activity == True or self.activity == "bat in last 10": # new change
                    break


    def read_rfid (self):
            # print ("read rfid")
            # print (self.bat_loc)
            data = DATA(self.fname)
            data.run()
            self.activity = data.activity
            self.bat1_id = data.bat_id_3 
            self.bat2_id = data.bat_id_4
            self.loc_bat1 = data.loc_bat3
            self.loc_bat2 = data.loc_bat4
            
            self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_id'] = self.bat1_id
            self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_id'] = self.bat2_id
            self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_loc'] = self.loc_bat1
            self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_loc'] = self.loc_bat2
            self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_condition'] = self.cond
            self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_condition'] = self.cond
            self.df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}_{self.bat_name}.csv")
            # print(self.bat_loc) 
            # self.decide()


    def pump_it (self, pump_id, win_lose_p = (1,0)):
        """pump from selected pump with the selected probability"""
        # global pump
        global new_pump
        global pump_1
        global pump_2
        # new_port = '/dev/ttyUSB1'
        # new_pump = serial.Serial(port=new_port, baudrate=9600)
        # pump_1 = bytearray([1,pumpamount])
        # pump_2 = bytearray([2,pumpamount])

        try:
            choice_arr = ["win", "lose"]
            val = np.random.choice(choice_arr, 1, p=win_lose_p)
            if(val == "win"):
                # new_pump.write(pump_id)
                new_pump.write(pump_id)
                # new_pump.write(bytearray([1,200]))
                # print (pump_id[0])
                new_pump.flush()
                data_raw = new_pump.readline()
                # print(data_raw)
                # pump.write([pump_id])
                # self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),f'pump_{pump_id}'] = pump_id
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),f'pump_{pump_id[0]}'] = pump_id[0]
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_id'] = self.bat1_id
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_id'] = self.bat2_id
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_loc'] = self.loc_bat1
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_loc'] = self.loc_bat2
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_condition'] = self.cond
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_condition'] = self.cond
                self.df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}_{self.bat_name}.csv")
                print ("pumping")
            else:
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),f'pump_{pump_id[0]}'] = 'no {}'.format(pump_id[0])
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_id'] = self.bat1_id
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_id'] = self.bat2_id
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_loc'] = self.loc_bat1
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_loc'] = self.loc_bat2
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_condition'] = self.cond
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_condition'] = self.cond
                self.df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}_{self.bat_name}.csv")
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
        global pump_1
        global pump_2
        # if 101 in [self.loc_bat1, self.loc_bat2]:
        if self.loc_bat1 == 104 or self.loc_bat2 == 104: #right pump
            # self.pump_it(pump_id = 1, win_lose_p = L_p)
            self.pump_it(pump_id = pump_1, win_lose_p = L_p)
        if self.loc_bat1 == 103 or self.loc_bat2 == 103: #left pump
            # self.pump_it(pump_id = 2, win_lose_p = R_p)
            self.pump_it(pump_id = pump_2, win_lose_p = R_p)
        
    def fix_pump_ir (self):
        """restart pump in case of disconnection """
        global pump
        global new_pump
        
        self.dis_time()
        try:
            if(new_pump.isOpen()):
                new_pump.close()
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
            self.pump_it(pump_1) #down right
            time.sleep(2)
            self.pump_it(pump_2)#up, left
            time.sleep(2)

    def run_slow (self, intervals = 20, running_time= 3600, cond1_R_p=(0.8,0.2), cond1_L_p=(0.2,0.8), cond2_R_p=(0.2,0.8), cond2_L_p=(0.8,0.2)):
        """main- alternate between conditions every x time"""
        # self.signal_on_reward(rewarding_feeder = 'R', intervals = intervals, running_time = running_time, R_p=cond2_R_p, L_p=cond2_L_p) #cond2
        # self.signal_on_reward(rewarding_feeder = 'L', intervals = intervals, running_time = running_time, R_p=cond1_R_p, L_p=cond1_L_p) # cond1
        self.signal_on_reward(rewarding_feeder = 'equal', intervals = intervals, running_time = running_time, R_p=cond1_R_p, L_p=cond1_L_p) # cond1

    def run_fast (self, intervals = 20, running_time= 3600, cond1_R_p=(0.8,0.2), cond1_L_p=(0.2,0.8), cond2_R_p=(0.2,0.8), cond2_L_p=(0.8,0.2)):
        """main- alternate between conditions every x time"""
        # self.signal_on_reward(rewarding_feeder = 'L', intervals = intervals, running_time = running_time, R_p=cond1_R_p, L_p=cond1_L_p) # cond1
        self.signal_on_reward(rewarding_feeder = 'R', intervals = intervals, running_time = running_time, R_p=cond2_R_p, L_p=cond2_L_p) #cond2
        self.signal_on_reward(rewarding_feeder = 'L', intervals = intervals, running_time = running_time, R_p=cond1_R_p, L_p=cond1_L_p) # cond1
     
if __name__ == "__main__":
    bat_name = 'B_test'
    # bat_name = 'dot_line_X' 
    # bat_name = 'gimel_yud_training' #slow training
    # bat_name = 'F_hagai' #fast
    # bat_name = 'S_X' # slow
    # bat_name = 'tent_B_training'
    filename = date.today().strftime("%d-%m-%y")
    fname = f"test_{filename}.csv"
    feeder = Feeder(fname, bat_name)

    # variables:
    intervals = 20 # between signals (in sec)
    running_time = 3600 # running time of each condition (in sec)
    cond1_R_p=(0.8,0.2) # right feeder win-lose p in cond1 (LEFT)
    cond1_L_p=(0.2,0.8) # left win-lose p in cond1 (RIGHT)
    cond2_R_p=(0.2,0.8) # right win-lose p in cond2 (LEFT)
    cond2_L_p=(0.8,0.2) # left win-lose p in cond2 (RIGHT)

    # clean
    feeder.cond = 'clean_tent_B'
    feeder.clean(40)
    #     
    # new_pump.write(bytearray([2,200]))
    # new_pump.flush()
    # feeder.pump_it(pump_1) #right (down)
    # time.sleep(2)
    # feeder.pump_it(pump_2)  # left
    # time.sleep(2)
   
        
    
    # feeder.cond = 'R'
    # read = feeder.read_rfid()

    # while True:
    #    feeder.run_slow(intervals, running_time, (1,0), (1,0), (1,0), (1,0))
    #     # feeder.run_slow(intervals, running_time, cond1_R_p, cond1_L_p, cond2_R_p, cond2_L_p)
    #     feeder.run_fast(intervals, running_time, cond1_R_p, cond1_L_p, cond2_R_p, cond2_L_p)
    
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









     





