import pandas as pd
from pathlib import Path

def read_save(fname):
    df = pd.read_csv(fname).tail(n = 50)
    output_file = (f"test_{pd.Timestamp.now().strftime('%d-%m-%y')}.csv")
    output_dir = Path('media/sf_share_vm')
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_dir / output_file)

if __name__ == "__main__":
    
