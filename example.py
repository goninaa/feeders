import serial
import time
s1 = serial.Serial('COM5', 9600, timeout=30)
s = serial.Serial('COM15', 9600, timeout=30)
time.sleep(2)

while True:
    msg = s.read()
    print(msg)

    if(msg == b'1'):

        time.sleep(2)
        s1.write([2])
        time.sleep(2)

    if (msg == b'2'):

        time.sleep(2)
        s1.write([1])
        time.sleep(2)
