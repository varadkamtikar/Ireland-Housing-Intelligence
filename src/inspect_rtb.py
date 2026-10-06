# src/inspect_rtb.py

import pandas as pd

df = pd.read_csv("data/raw/rtb.csv")

print(df.columns.tolist())
print()
print(df.head())
print()
print("Rows:", len(df))