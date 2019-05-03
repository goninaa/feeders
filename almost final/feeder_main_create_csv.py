import serial
import time
import numpy as np
import pandas as pd
import csv
from stereo import *  # playing files import

pump = serial.Serial('COM5', 9600, timeout=1) # pump
ir = serial.Serial('COM15', 9600, timeout=1)# IR
# time.sleep(2)
df_signal = pd.DataFrame(columns=['signal'])

class Feeder:

    # def __init__(self):
    #     self.pump = serial.Serial('COM5', 9600, timeout=30)  # pump
    #     self.ir = serial.Serial('COM15', 9600, timeout=30)  # IR

    def signal_on (self, intervals = 10):
        """ intervals = 20 sec between signals"""
        global df_signal
        signals = stereo('left_sig.wav', 'right_sig.wav')
        print (f"{pd.Timestamp.now()} playing signal")
        df_signal.loc[f'{pd.Timestamp.now()}'] = 'play'
        signals.run() # play signals from both feeders
        time.sleep(intervals) 


    def read_ir (self):
        global ir
        global pump
        try:
            msg = ir.read() #Ir Reader
        except serial.SerialException as e:
            try:
                if (pump.isOpen()):
                    pump.close()
                if (ir.isOpen()):
                    ir.close()
                # pump = serial.Serial('COM5', 9600, timeout=30)  # pump
                # ir = serial.Serial('COM15', 9600, timeout=30)  # IR
                time.sleep(3)
            except serial.SerialException as e2:
                    print("I couldnt open the port jesus!!!")

        print(msg) #print to screen
        time.sleep(1)
        return msg


    def pump_it (self, pump_id):
        global ir
        global pump
        time.sleep(2)
        try:
            val = np.random.choice(2, 1, p=[0.6, 0.4])
            if(val == 0):
                pump.write([pump_id])
        except serial.SerialException as e:
            try:
                if(pump.isOpen()):
                    pump.close()
                if (ir.isOpen()):
                    ir.close()
                # pump = serial.Serial('COM5', 9600, timeout=30)  # pump
                # ir = serial.Serial('COM15', 9600, timeout=30)  # IR
                time.sleep(3)
            except serial.SerialException as e2:
                print("I couldnt open the port jesus!!!")
        time.sleep(2)

    def write_to_csv (self, df_data):
       df_data.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%m')}.csv")


    def run (self):  
        global ir
        global pump
        # while True:
        r_msg = self.read_ir()
        print (r_msg)
        if (r_msg == b'1') or (r_msg == b'2'):  # reads
            bat = True
        else: # doesn't read
            bat = False
        while bat == False:
            self.signal_on()
            r_msg = self.read_ir()
            print(r_msg)
            if r_msg == b'1':
                self.pump_it(2)
                bat = True
            elif r_msg == b'2':
                self.pump_it(1)
                bat = True



if __name__ == "__main__":
    feeder = Feeder()
    while True:
        feeder.run()
        # feeder.signal_on()
        # feeder.pump_it(1)
        # read = feeder.read_ir()
        # print (read)

     






