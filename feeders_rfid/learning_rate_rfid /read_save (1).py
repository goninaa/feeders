import pandas as pd
from pathlib import Path
from datetime import date

def read_save(fname):
    df = pd.read_csv(fname).tail(n = 50)
    filename = date.today().strftime("%d-%m-%Y")
    output_file = f"test_{filename}.csv"
    output_dir = Path('media/sf_share_vm')
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_dir / output_file)

if __name__ == "__main__":
    
    filename = date.today().strftime("%d-%m-%Y")
    fname = f"bat_eat_data/test_{filename}.csv"   #date of today
    while True:
        read_save(fname)
    
