import serial
import time
import numpy as np
import pandas as pd
import csv
from stereo import *  # playing files import

pump = serial.Serial('COM5', 9600, timeout=1) # pump
ir = serial.Serial(com_ir, 9600, timeout=1)# IR
# time.sleep(2)
# df_signal = pd.DataFrame(columns=['signal'])
# df_ir = pd.DataFrame(columns=['feeder'])
# df_pump = pd.DataFrame(columns=['pump'])

class Feeder:

    # def __init__(self):
    #     self.pump = serial.Serial('COM5', 9600, timeout=30)  # pump
    #     self.ir = serial.Serial(com_ir, 9600, timeout=30)  # IR

    def __init__(self):
        self.df_signal = pd.DataFrame(columns=['signal'])
        self.df_ir = pd.DataFrame(columns=['feeder'])
        self.df_pump = pd.DataFrame(columns=['pump'])
        self.df_all = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1)


    def signal_on (self, intervals = 10):
        """ intervals = 20 sec between signals"""
        # global df_signal
        signals = stereo('left_sig.wav', 'right_sig.wav')
        print (f"{pd.Timestamp.now()} playing signal")
        # signal_s = (pd.Series('play', index=[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] ))
        self.df_signal.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 'play'
        # self.write_to_csv() # not working
        df = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1)
        df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%M')}.csv")
        # print (df)
        signals.run() # play signals from both feeders
        time.sleep(intervals)
        # return df



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
        # ir_s = ( pd.Series(msg, index=[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')]))
        # self.df_ir.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = msg
        # df_ir.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'] = msg #needs to be check
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
                # pump_s = pd.Series(pump_id, index=[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')])
                self.df_pump.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = pump_id
                df = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1)
                df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%M')}.csv")
                # df_pump.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'] = [pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),pump_id] #needs to be check
            else:
                self.df_pump.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 'no'
                df = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1)
                df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%M')}.csv")
                # self.pump_s = pd.Series('no', index=[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')])
                # df_pump.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 'no'
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


    # def write_to_csv (self, df_signal_1, df_ir_2, df_pump_3):
    def write_to_csv(self):
        self.df_all = pd.concat([self.df_signal, self.df_ir, self.df_pump], axis=1)
        df_all = self.df_all
        # df_data.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%M')}.csv")
        df_all.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%M')}.csv")
        # return df_data


    def run (self):  
        global ir
        global pump
        # global df_signal
        # global df_ir
        # global df_pump
        # while True:
        # self.df_all.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%M')}.csv")
        r_msg = self.read_ir()
        print (r_msg)
        if (r_msg == b'1') or (r_msg == b'2'):  # reads
            bat = True
            # self.df_all.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%M')}.csv")
            # feeder.write_to_csv(df_signal, df_ir, df_pump)
        else: # doesn't read
            bat = False
        while bat == False:
            df_signal2 = self.signal_on()
            # self.df_all.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%M')}.csv")
            # feeder.write_to_csv(df_signal, df_ir, df_pump)
            r_msg = self.read_ir()
            print(r_msg)
            if r_msg == b'1':
                self.pump_it(2)
                bat = True
                # self.df_all.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%M')}.csv")
                # feeder.write_to_csv(df_signal, df_ir, df_pump)
            elif r_msg == b'2':
                self.pump_it(1)
                bat = True
                # self.df_all.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%M')}.csv")

            # self.df_all.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%M')}.csv")
        # feeder.write_to_csv(df_signal, df_ir, df_pump)

        # data = feeder.write_to_csv(df_signal2, df_ir1, df_pump3)
        # data.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%m')}.csv")
        # df_data = pd.concat([df_signal_1, df_ir_2, df_pump_3], axis=1)
        # print (df_data)
        # return df_data






if __name__ == "__main__":
    feeder = Feeder()
    # try:
    while True:
        # feeder.write_to_csv(df_signal, df_ir, df_pump)
        feeder.run()
        # feeder.write_to_csv()
        # data.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%m')}.csv")
        # f = feeder.signal_on()
        # print (f)
        # feeder.pump_it(1)
        # read = feeder.read_ir()
        # print (read)

        # df_data = pd.concat([df_signal, df_ir, df_pump], axis=1)
        # df_data.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%M')}.csv")
        # feeder.write_to_csv(df_signal, df_ir, df_pump)

    # except KeyboardInterrupt:

        # global df_signal
        # global df_ir
        # global df_pump
        # while True:

        """"
        feeder.df_all.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%M')}.csv")
        r_msg = feeder.read_ir()
        print(r_msg)
        if (r_msg == b'1') or (r_msg == b'2'):  # reads
            bat = True
            feeder.df_all.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%M')}.csv")
            # feeder.write_to_csv(df_signal, df_ir, df_pump)
        else:  # doesn't read
            bat = False
        while bat == False:
            df_signal2 = feeder.signal_on()
            feeder.df_all.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%M')}.csv")
            # feeder.write_to_csv(df_signal, df_ir, df_pump)
            r_msg = feeder.read_ir()
            print(r_msg)
            if r_msg == b'1':
                feeder.pump_it(2)
                bat = True
                feeder.df_all.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%M')}.csv")
                # feeder.write_to_csv(df_signal, df_ir, df_pump)
            elif r_msg == b'2':
                feeder.pump_it(1)
                bat = True
                feeder.df_all.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%M')}.csv")

            feeder.df_all.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%M')}.csv")
"""



     






