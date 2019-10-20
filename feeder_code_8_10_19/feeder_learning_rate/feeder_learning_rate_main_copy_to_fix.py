import serial
import time
import numpy as np
import pandas as pd
import csv
from stereo_one_signal import *  # playing files import

com_ir = 'COM14'
com_pump = 'COM17'
pump = serial.Serial(com_pump, 9600, timeout=1) # pump
ir = serial.Serial(com_ir, 9600, timeout=10)# IR

class Feeder:

    def __init__(self):
        self.df = pd.DataFrame(columns=['signal','feeder','pump','condition'])
        # self.df_signal = pd.DataFrame(columns=['signal'])
        # self.df_ir = pd.DataFrame(columns=['feeder'])
        # self.df_pump = pd.DataFrame(columns=['pump'])
        # self.df_cond = pd.DataFrame(columns=['condition'])
        self.disconnect = []
        # self.df_all = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)
        self.msg = "first msg"
        self.bat = False
        self.cond = None


    def signal_on_reward (self, rewarding_feeder = 'R', intervals = 20, running_time = 3200, R_p=(1,0), L_p=(1,0)):
        """ intervals = 20 sec between signals"""
        print (rewarding_feeder)
        self.cond = (f'{rewarding_feeder} reward')
        tr_end = time.time() + running_time
        while time.time() < tr_end:
            if time.time() >= tr_end:
                break
            self.read_ir()
            while self.bat == False:
                if time.time() >= tr_end:
                    break
                signals = stereo('left_sig.wav', 'right_sig.wav')
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'signal'] = 'play'
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'condition'] = self.cond
                self.df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
                # print (df)
                print (f"{pd.Timestamp.now()} playing signal")
                print (self.cond)
                signals.run()  # play signals from both feeders
                flag_t = 0
                t_end = time.time()+intervals
                while time.time() < t_end:
                    if time.time() >= tr_end:
                        break
                    self.read_ir()
                    self.decide()
                    if self.bat == True and flag_t == 0:
                        self.which_pump(R_p, L_p)
                        flag_t += 1
                if self.bat == True:
                    break

    def read_ir (self):
        """read from ir reader, print the result and save to data frame in csv"""
        global ir
        global pump
        try:
            self.msg = ir.read() #Ir Reader
        except serial.SerialException as e:
            self.dis_time()
            try:
                if (pump.isOpen()):
                    pump.close()
                if (ir.isOpen()):
                    ir.close()
                pump = serial.Serial(com_pump, 9600, timeout=1)  # pump
                ir = serial.Serial(com_ir, 9600, timeout=5)  # IR
                time.sleep(1) #3
                print ("restart")
            except serial.SerialException as e2:
                    self.dis_time()
                    print("I couldnt open the port jesus!!!")

        self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'feeder'] = self.msg
        self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'condition'] = self.cond
        self.df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
        print(self.msg) #print to screen
        self.decide()


    def pump_it (self, pump_id, win_lose_p = (1,0)):
        """pump from selected pump with the selected probability"""
        global ir
        global pump

        try:
            choice_arr = ["win", "lose"]
            val = np.random.choice(choice_arr, 1, p=win_lose_p)
            if(val == "win"):
                pump.write([pump_id])
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'pump'] = pump_id
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'condition'] = self.cond
                self.df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
                print ("pumping")
            else: 
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'pump'] = 'no {}'.format(pump_id)
                self.df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'condition'] = self.cond
                self.df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")

        except serial.SerialException as e:
            self.dis_time()
            try:
                if(pump.isOpen()):
                    pump.close()
                if (ir.isOpen()):
                    ir.close()
                pump = serial.Serial(com_pump, 9600, timeout=1)  # pump
                ir = serial.Serial(com_ir, 9600, timeout=5)  # IR
                time.sleep(3)
                print("restart")
            except serial.SerialException as e2:
                self.dis_time()
                print("I couldnt open the port jesus!!!")

    def decide (self):
        """check if bat true or false"""
        if (self.msg == b'1') or (self.msg == b'2'):  # reads bats
            self.bat = True
        # else:  # if doesn't read
        elif self.msg == b'': # if reads "no bat"
            self.bat = False

    def which_pump_reward (self, R_p=(1,0), L_p=(1,0)):
        """decide which pump to use. 
            right feeder with probability of 0.8
            left feeder probability 0.2"""
        if self.msg == b'1':
            self.pump_it(pump_id = 1, L_p = L_p)
        elif self.msg == b'2':
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


    # def r_reward(self, rewarding_feeder= 'R', intervals = 20, running_time= 3600, R_p=(0.8,0.2), L_p=(0.2,0.8)):
    #     """ running r_reward condition for n running time (in sec)"""
    #     print('R')
    #     self.cond = 'R reward'
    #     self.df_cond.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 'R reward'
    #     self.read_ir()
    #     self.signal_on_reward(rewarding_feeder, intervals, running_time, R_p, L_p)
        

    # def l_reward(self, intervals = 20, running_time= 3600, R_p=(0.2,0.8), L_p=(0.8,0.2)):
    #     """ running l_reward condition for n running time (in sec)"""
    #     print ('L')
    #     self.cond = 'L reward'
    #     self.df_cond.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 'L reward'
    #     self.read_ir()
    #     self.signal_on_reward(intervals, running_time, R_p, L_p)

    def run (self, intervals = 20, running_time= 3600, cond1_R_p=(0.8,0.2), cond1_L_p=(0.2,0.8), cond2_R_p=(0.2,0.8), cond2_L_p=(0.8,0.2)):
        """main- alternate between conditions"""
        self.signal_on_reward(rewarding_feeder = 'R', intervals = intervals, running_time = running_time, R_p=cond1_R_p, L_p=cond1_L_p) # cond1
        self.signal_on_reward(rewarding_feeder = 'L', intervals = intervals, running_time = running_time, R_p=cond2_R_p, L_p=cond2_L_p) #cond2
       
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
        # feeder.run( intervals, running_time, cond1_R_p, cond1_L_p, cond2_R_p, cond2_L_p)
        # f = feeder.signal_on()
        # print (f)
        feeder.pump_it(2)
        time.sleep(2)
        feeder.pump_it(1) #left
        time.sleep(2)
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









     






