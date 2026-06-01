import pandas as pd
from src.db import engine

query = "SELECT * FROM rental_prices"

df = pd.read_sql(query, engine)

print(df)