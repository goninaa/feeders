import time
import numpy as np
import pandas as pd
# import csv
from datetime import date

df = pd.DataFrame(columns=['signal','bat1_id','bat1_loc','bat1_condition',
                            'pump_1','pump_2', 'bat2_id','bat2_loc','bat2_condition'])

df.loc[pd.Timestamp.now().strftime('%d-%m-%Y-%H:%M:%S'),'signal'] = 'play'

# with open(f"{pd.Timestamp.now().strftime('%Y-%m-%d')}_{'saving_test'}.csv", 'w') as f:
#                 f.write(df)