import datetime
import csv
import pandas as pd
import time

# csvdata = [datetime.datetime.now()]
# with open(f"{datetime.date.today().strftime('%Y-%m-%d')}.csv","w") as csvFile:
#     Fileout = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_ALL)
#     Fileout.writerow(csvdata)

# print(datetime.datetime.now().time())
# print (datetime.date.today().strftime('%Y-%m-%d'))

# print (pd.Timestamp.now().strftime('%d-%m-%Y')) 

# for i in range (10):
# s = pd.Series([])
# time = pd.Series([pd.Timestamp.now()])
# time2 = pd.Series([pd.Timestamp.now()])
# time.append(time2)
# print (pd.Timestamp.now()) 
# df = pd.DataFrame({'time': time})


# df = pd.DataFrame(columns=['time'])
# for i in range(5):
#     # df.loc[i] = ['name' + str(i)] + list(randint(10, size=2))
#     df.loc[i] = [pd.Timestamp.now()] 
# print (df)


df_1 = pd.DataFrame(columns=['signal'])
df_2 = pd.DataFrame(columns=['feeder'])
df_3 = pd.DataFrame(columns=['pump'])
def play_sig ():
    global df_1
    df_1.loc[f'{pd.Timestamp.now()}'] = 'play'
    time.sleep (3)
    return df_1

for i in range (3):
    df_1 = play_sig()
    # df_2 = df_1.assign(feeder_id=['1'])
    pump_id = 2
    df_1.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 3
    df_2.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = pump_id
    df_3.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S')] = 'yes'
    # df_1['feeder_id']=1
print (df_1)

df_data = pd.concat([df_1, df_2, df_3], axis=1)
print (df_data)
"""
# df_f = pd.DataFrame(columns=['time'] index = ['a'])
df_f = pd.DataFrame(index=['a', 'b', 'c'], columns=['time', 'feeder_id', 'pump(y/n)'])
pump_id = 2
df_f.loc['d'] = [pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),1,(f'{pump_id} pumps')]
# df_2 = df_f.assign(feeder_id=['1','2','3'])
print (df_f)
# def write_to_csv (csv_data):
#     # csvdata = [datetime.datetime.now()]
#     with open(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H:%m')}.csv","w") as csvFile:
#         Fileout = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_ALL)
#         Fileout.writerow(csv_data)

# write_to_csv(df_1)"""


# with open(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%m')}.csv","w") as csvFile:
#     Fileout = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_ALL)
#     Fileout.writerow(df_1)

# df_1.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%m')}.csv")

