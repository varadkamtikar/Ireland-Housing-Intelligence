import pandas as pd
from src.db import engine

df = pd.read_sql("SELECT * FROM rental_prices LIMIT 10;", engine)
count_df = pd.read_sql("SELECT COUNT(*) AS total_rows FROM rental_prices;", engine)

print(df)
print(count_df)