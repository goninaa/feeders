import serial
import time
import numpy as np
import pandas as pd
import csv
from stereo_one_signal import *  # playing files import
com_ir = 'COM14'
com_pump = 'COM5'
pump = serial.Serial(com_pump, 9600, timeout=1) # pump
ir = serial.Serial(com_ir, 9600, timeout=10)# IR

class Feeder:

    def __init__(self):
        self.df_signal = pd.DataFrame(columns=['signal'])
        self.df_ir = pd.DataFrame(columns=['feeder'])
        self.df_pump = pd.DataFrame(columns=['pump'])
        self.disconnect = []
        self.df_all = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)
        self.msg = "first msg"
        self.bat = False


    def signal_on_r_reward (self, intervals = 20):
        """ intervals = 20 sec between signals"""
        while self.bat == False:
            signals = stereo('left_sig.wav', 'right_sig.wav')
            print (f"{pd.Timestamp.now()} playing signal")
            self.df_signal.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 'play'
            df = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)
            df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
            # print (df)
            signals.run()  # play signals from both feeders
            flag_t = 0
            t_end = time.time()+intervals
            while time.time() < t_end:
                self.read_ir()
                self.decide()
                if self.bat == True and flag_t == 0:
                    self.which_pump_r_reward()
                    flag_t += 1
            if self.bat == True:
                break

        def signal_on_l_reward (self, intervals = 20):
        """ intervals = 20 sec between signals"""
        while self.bat == False:
            signals = stereo('left_sig.wav', 'right_sig.wav')
            print (f"{pd.Timestamp.now()} playing signal")
            self.df_signal.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 'play'
            df = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)
            df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
            # print (df)
            signals.run()  # play signals from both feeders
            flag_t = 0
            t_end = time.time()+intervals
            while time.time() < t_end:
                self.read_ir()
                self.decide()
                if self.bat == True and flag_t == 0:
                    self.which_pump_l_reward()
                    flag_t += 1
            if self.bat == True:
                break


    def read_ir (self):
        """read from ir reader, print the result and save to data frame in csv"""
        global ir
        global pump
        global df_ir
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

        self.df_ir.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = self.msg
        df = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)
        df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
        print(self.msg) #print to screen
        self.decide()


    def pump_it (self, pump_id):
        """pump from selected pump"""
        global ir
        global pump

        try:
            # val = np.random.choice(2, 1, p=[0.6, 0.4])
            val = 0 # val always = 0
            if(val == 0):
                pump.write([pump_id])
                print ("pumping")
                self.df_pump.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = pump_id
                df = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)
                df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
            else:
                self.df_pump.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 'no {}'.format(pump_id)
                df = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)
                df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")

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

    def pump_it_80 (self, pump_id):
        """pump from selected pump with the probability of 0.8"""
        global ir
        global pump

        try:
            choice_arr = ["win", "lose"]
            val = np.random.choice(choice_arr, 1, p=[0.8, 0.2])
            # val = 0 # val always = 0
            if(val == "win"):
                pump.write([pump_id])
                print ("pumping")
                self.df_pump.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = pump_id
                df = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)
                df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
            else:
                self.df_pump.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 'no {}'.format(pump_id)
                df = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)
                df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")

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

    def pump_it_20 (self, pump_id):
         """pump from selected pump with the probability of 0.2"""
        global ir
        global pump

        try:
            choice_arr = ["win","lose"]
            val = np.random.choice(choice_arr, 1, p=[0.2, 0.8])
            # val = 0 # val always = 0
            if(val == "win"):
                pump.write([pump_id])
                print ("pumping")
                self.df_pump.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = pump_id
                df = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)
                df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
            else:
                self.df_pump.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 'no {}'.format(pump_id)
                df = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)
                df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")

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

    def which_pump_r_reward (self):
        """decide which pump to use. 
            right feeder with probability of 0.8
            left feeder probability 0.2"""
        if self.msg == b'1':
            self.pump_it_20(1)
        elif self.msg == b'2':
            self.pump_it_80(2)

    def which_pump_l_reward (self):
         """decide which pump to use. 
            right feeder with probability of 0.2
            left feeder probability 0.8"""
        if self.msg == b'1':
            self.pump_it_80(1)
        elif self.msg == b'2':
            self.pump_it_20(2)
          

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


    def r_reward(self, running_time = 60):
        """ running r_reward condition for n running time (in sec)"""
        t_end = time.time()+ running_time
        while time.time() < t_end:
            if time.time() >= t_end:
                break
            self.read_ir()
            self.signal_on_r_reward()

     def l_reward(self, running_time = 60):
         """ running l_reward condition for n running time (in sec)"""
        t_end = time.time()+ running_time
        while time.time() < t_end:
            if time.time() >= t_end:
                break
            self.read_ir()
            self.signal_on_l_reward()

    def run (self):
        """main- alternate between conditions"""
        while True:
            self.r_reward(running_time = 60)
            self.l_reward(running_time = 60)


            # threading.Timer(WAIT_SECONDS, foo).start()
        # t_end = time.time()+ 60
        # while time.time() < t_end:
        #     if time.time() >= t_end:
        #         break
        #     self.read_ir()
        #     self.signal_on_r_reward()
      


        #     sec = 60
        #     timer = time.time()+sec
        #     while time.time() < timer:
        #     self.read_ir()
        #     self.signal_on_r_reward()




if __name__ == "__main__":
    feeder = Feeder()
    # try:
    while True:
        feeder.run()
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









     






