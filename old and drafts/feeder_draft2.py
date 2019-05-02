import serial
import time
import numpy as np
from stereo import stereo  # playing files import

pump = serial.Serial('COM5', 9600, timeout=30) # pump
ir = serial.Serial('COM15', 9600, timeout=30)# IR
time.sleep(2)

class feeder:

    def signal_on (self, intervals = 20):
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
                pump = serial.Serial('COM5', 9600, timeout=30)  # pump  
                ir = serial.Serial('COM15', 9600, timeout=30)  # IR  
                time.sleep(3)
            except serial.SerialException as e2:
                    print("I couldnt open the port jesus!!!")

        print(msg) #print to screen
        return msg


    def pump_it (self, pump_id):
        time.sleep(2)
        try:
            val = np.random.choice(2, 1, p=[0.6, 0.4])
            if(val == 2):
                pump.write([pump_id])
        except serial.SerialException as e:
            try:
                if(pump.isOpen()):
                    pump.close()
                if (ir.isOpen()):
                    ir.close()
                pump = serial.Serial('COM5', 9600, timeout=30)  # pump
                ir = serial.Serial('COM15', 9600, timeout=30)  # IR
                time.sleep(3)
            except serial.SerialException as e2:
                print("I couldnt open the port jesus!!!")
        time.sleep(2)


    def run (self, msg):
        while True:
            self.read_ir()
            if (msg == b'1') or (msg == b'2'):  # reads
                bat = True
            else: # doesn't read
                bat = False
            while bat == False:
                self.signal_on()
                if msg == b'1': 
                    self.pump_it(1)
                    bat = True
                elif msg == b'2':
                    self.pump_it(2)
                    bat = True


if __name__ == "__main__":

    feeder = feeder()
    feeder.run
