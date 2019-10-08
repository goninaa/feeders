import serial
import time
import numpy as np
import pandas as pd
import csv
from stereo import *  # playing files import

pump = serial.Serial('COM5', 9600, timeout=1) # pump
ir = serial.Serial(com_ir, 9600, timeout=1)# IR

class Feeder:

    # def __init__(self):
    #     self.pump = serial.Serial('COM5', 9600, timeout=30)  # pump
    #     self.ir = serial.Serial(com_ir, 9600, timeout=30)  # IR

    def __init__(self):
        self.df_signal = pd.DataFrame(columns=['signal'])
        self.df_ir = pd.DataFrame(columns=['feeder'])
        self.df_pump = pd.DataFrame(columns=['pump'])
        self.df_all = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)


    def signal_on (self, intervals = 10):
        """ intervals = 20 sec between signals"""
        signals = stereo('left_sig.wav', 'right_sig.wav')
        print (f"{pd.Timestamp.now()} playing signal")
        self.df_signal.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 'play'
        # self.write_to_csv() # not working
        df = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)
        df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
        # print (df)
        signals.run() # play signals from both feeders
        time.sleep(intervals)


    def read_ir (self):
        global ir
        global pump
        global df_ir
        try:
            msg = ir.read() #Ir Reader
        except serial.SerialException as e:
            try:
                if (pump.isOpen()):
                    pump.close()
                if (ir.isOpen()):
                    ir.close()
                # pump = serial.Serial('COM5', 9600, timeout=30)  # pump
                # ir = serial.Serial(com_ir, 9600, timeout=30)  # IR
                time.sleep(3)
            except serial.SerialException as e2:
                    print("I couldnt open the port jesus!!!")

        print(msg) #print to screen
        time.sleep(1)
        return msg


    def pump_it (self, pump_id):
        global ir
        global pump
        global df_pump
        time.sleep(2)
        try:
            val = np.random.choice(2, 1, p=[0.6, 0.4])
            if(val == 0):
                pump.write([pump_id])
                self.df_pump.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = pump_id
                df = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)
                df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
            else:
                self.df_pump.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 'no {}'.format(pump_id)
                df = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)
                df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")

        except serial.SerialException as e:
            try:
                if(pump.isOpen()):
                    pump.close()
                if (ir.isOpen()):
                    ir.close()
                # pump = serial.Serial('COM5', 9600, timeout=30)  # pump
                # ir = serial.Serial(com_ir, 9600, timeout=30)  # IR
                time.sleep(3)
            except serial.SerialException as e2:
                print("I couldnt open the port jesus!!!")
        time.sleep(2)



    def write_to_csv(self): # not useful
        self.df_all = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)
        df_all = self.df_all
        # df_data.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%M')}.csv")
        df_all.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")
        # return df_data


    def run (self):  
        global ir
        global pump

        r_msg = self.read_ir()
        print (r_msg)
        if (r_msg == b'1') or (r_msg == b'2'):  # reads
            bat = True
            self.df_ir.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = r_msg
            df = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)
            df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")

        else: # if doesn't read
            bat = False
        while bat == False:
            df_signal2 = self.signal_on()

            r_msg = self.read_ir()
            print(r_msg)
            if r_msg == b'1':
                self.pump_it(2)
                bat = True
                self.df_ir.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = r_msg
                df = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)
                df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")

            elif r_msg == b'2':
                self.pump_it(1)
                bat = True
                self.df_ir.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = r_msg
                df = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1, sort = True)
                df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv")



if __name__ == "__main__":
    feeder = Feeder()
    # try:
    while True:
        feeder.run()
        # f = feeder.signal_on()
        # print (f)
        # feeder.pump_it(1)
        # read = feeder.read_ir()
        # print (read)







     






