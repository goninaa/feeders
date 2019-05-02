import serial
import time
import numpy as np
from stereo import *  # playing files import

pump = serial.Serial('COM5', 9600, timeout=1) # pump
ir = serial.Serial('COM15', 9600, timeout=1)# IR
time.sleep(2)

class Feeder:

    # def __init__(self):
    #     self.pump = serial.Serial('COM5', 9600, timeout=30)  # pump
    #     self.ir = serial.Serial('COM15', 9600, timeout=30)  # IR

    def signal_on (self, intervals = 10):
        """ intervals = 20 sec between signals"""
        signals = stereo('left_sig.wav', 'right_sig.wav')
        signals.run() # play signals from both feeders
        time.sleep(intervals) 


    def read_ir (self):
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


    def run (self):  # for some reson doesn't work
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

        # r_msg = feeder.read_ir()
        # print (r_msg)
        # if (r_msg == b'1') or (r_msg == b'2'):  # reads
        #     bat = True
        # else: # doesn't read
        #     bat = False
        # while bat == False:
        #     feeder.signal_on()
        #     r_msg = feeder.read_ir()
        #     print(r_msg)
        #     if r_msg == b'1':
        #         feeder.pump_it(2)
        #         bat = True
        #     elif r_msg == b'2':
        #         feeder.pump_it(1)
        #         bat = True






