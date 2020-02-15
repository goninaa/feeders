import serial
import time
import numpy as np
import pandas as pd
import csv
from datetime import date
from pathlib import Path
from stereo_one_signal_v2 import *  # playing files import
from class_read_rec_v6 import *

# com_pump = '/dev/ttyUSB0'
# pump = serial.Serial(com_pump, 9600, timeout=1) # pump

#new

new_port = '/dev/ttyUSB1'
# new_port =  '/dev/ttyUSB0'
new_pump = serial.Serial(port=new_port, baudrate=9600)
pumpamount = 200 # can be 1 - 254
pump_1 = bytearray([1,pumpamount])
pump_2 = bytearray([2,pumpamount])

new_pump.isOpen()
print ('open')
new_pump.write(pump_1)
print ('pump1')
new_pump.write(pump_2)
print ('pump2')
new_pump.flush()
print ('flush')
data_raw = new_pump.readline()
print(data_raw)
print ('done')

# import serial

# ser = serial.Serial(
#     port='/dev/ttyUSB1',
#     baudrate=9600
# )

# pumpnumber = 1 # can be 1 or 2
# pumpamount = 200 # can be 1 - 254

# values = bytearray([pumpnumber,pumpamount])
# ser.isOpen()
# ser.write(values)
# ser.flush()
# data_raw = ser.readline()
# print(data_raw)