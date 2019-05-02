import serial
import time
import numpy as np
from stereo import stereo

pump = serial.Serial('COM5', 9600, timeout=30) # pump
ir = serial.Serial('COM15', 9600, timeout=30)# IR
time.sleep(2)

signals = stereo('left_sig.wav', 'right_sig.wav')
signals.run() # play signals from both feeders

def read_ir ():
    try:
        msg = ir.read() #Ir Reader
    except serial.SerialException as e:
        try:
            if (pump.isOpen()):
                pump.close()
            if (ir.isOpen()):
                ir.close()
            pump = serial.Serial('COM5', 9600, timeout=30)  # pump  #s1
            ir = serial.Serial('COM15', 9600, timeout=30)  # IR  #s
            time.sleep(3)
        except serial.SerialException as e2:
                print("I couldnt open the port jesus!!!")

    print(msg) #print to screen
    return msg


#get 1000 numbers that are 1 or 2 with normal distrubution

while True: #infinte loop
    msg = read_ir()
    # try:
    #     msg = ir.read() #Ir Reader
    # except serial.SerialException as e:
    #     try:
    #         if (pump.isOpen()):
    #             pump.close()
    #         if (ir.isOpen()):
    #             ir.close()
    #         pump = serial.Serial('COM5', 9600, timeout=30)  # pump  #s1
    #         ir = serial.Serial('COM15', 9600, timeout=30)  # IR  #s
    #         time.sleep(3)
    #     except serial.SerialException as e2:
    #             print("I couldnt open the port jesus!!!")

    # print(msg) #print to screen

    if(msg == b'1'):

        time.sleep(2)
        try:
            val = np.random.choice(2, 1, p=[0.6, 0.4])
            if(val == 2):
                pump.write([2])
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

    if (msg == b'2'):

        time.sleep(2)
        try:
            val = np.random.choice(2, 1, p=[0.6, 0.4])
            if (val == 0):
                pump.write([1])
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
        time.sleep(2)



