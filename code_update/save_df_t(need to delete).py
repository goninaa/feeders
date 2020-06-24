import time
import numpy as np
import pandas as pd


df = pd.DataFrame(columns=['time','signal','bat1_id','bat1_loc','bat1_condition',
                                        'pump_1','pump_2', 'bat2_id','bat2_loc','bat2_condition'])

start = time.time()
### faster!
# df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_id'] = '1A'
# df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_id'] = '2A'
# df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_loc'] = 101
# df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_loc'] = 102
# df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat1_condition'] = 'R REWARD'
# df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'bat2_condition'] = 'R REWARD'
# # self.df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}_{self.bat_name}.csv")
# df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H')}_{'self.bat_name'}.csv") #saves different file every hour

# tr_end = time.time() + 1
# start = time.time()
# while time.time() < tr_end:
#     a = 1
# start = time.time()
df = df.append({'time':pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'), 'bat1_id' :'3A' , 'bat1_loc' : 101, 'pump_1': 1,'bat2_id' :'2A'} , ignore_index=True)
df.to_csv(f"{pd.Timestamp.now().strftime('%Y-%m-%d-%H')}_{'self.bat_name'}.csv")
elapsed = time.time()- start
# elapsed = time.strftime("%H:%M:%S:%ms", time.gmtime(elapsed))
print (df)
print (elapsed)
