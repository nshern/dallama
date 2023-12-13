import subprocess

import pandas as pd

df = pd.read_csv("overview.csv")

for index, row in df.iterrows():
    command = f"ollama rm {row['id']}"
    subprocess.run(f"ollama rm {row['id']}", shell=True)
    df.drop(index, inplace=True)
