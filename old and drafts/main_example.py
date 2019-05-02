import serial
import time
import numpy as np
s1 = serial.Serial('COM5', 9600, timeout=30) # pump
s = serial.Serial('COM15', 9600, timeout=30)# IR
time.sleep(2)

#get 1000 numbers that are 1 or 2 with normal distrubution

while True: #infinte loop

    try:
        msg = s.read() #Ir Reader
    except serial.SerialException as e:
        try:
            if (s1.isOpen()):
                s1.close()
            if (s.isOpen()):
                s.close()
            s1 = serial.Serial('COM5', 9600, timeout=30)  # pump
            s = serial.Serial('COM15', 9600, timeout=30)  # IR
            time.sleep(3)
        except serial.SerialException as e2:
                print("I couldnt open the port jesus!!!")

    print(msg) #print to screen

    if(msg == b'1'):

        time.sleep(2)
        try:
            val = np.random.choice(2, 1, p=[0.6, 0.4])
            if(val == 0):
                s1.write([2])
        except serial.SerialException as e:
            try:
                if(s1.isOpen()):
                    s1.close()
                if (s.isOpen()):
                    s.close()
                s1 = serial.Serial('COM5', 9600, timeout=30)  # pump
                s = serial.Serial('COM15', 9600, timeout=30)  # IR
                time.sleep(3)
            except serial.SerialException as e2:
                print("I couldnt open the port jesus!!!")
        time.sleep(2)

    if (msg == b'2'):

        time.sleep(2)
        try:
            val = np.random.choice(2, 1, p=[0.6, 0.4])
            if (val == 0):
                s1.write([1])
        except serial.SerialException as e:
            try:
                if (s1.isOpen()):
                    s1.close()
                if (s.isOpen()):
                    s.close()
                s1 = serial.Serial('COM5', 9600, timeout=30)  # pump
                s = serial.Serial('COM15', 9600, timeout=30)  # IR
                time.sleep(3)
            except serial.SerialException as e2:
                print("I couldnt open the port jesus!!!")
        time.sleep(2)



