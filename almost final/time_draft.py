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


df = pd.DataFrame(columns=['signal'])
def play_sig ():
    global df
    df.loc[f'{pd.Timestamp.now()}'] = 'play'
    time.sleep (3)
    return df

for i in range (3):
    df_1 = play_sig()
print (df_1)


# def write_to_csv (csv_data):
#     # csvdata = [datetime.datetime.now()]
#     with open(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H:%m')}.csv","w") as csvFile:
#         Fileout = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_ALL)
#         Fileout.writerow(csv_data)

# write_to_csv(df_1)


# with open(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%m')}.csv","w") as csvFile:
#     Fileout = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_ALL)
#     Fileout.writerow(df_1)

df_1.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H%m')}.csv")

