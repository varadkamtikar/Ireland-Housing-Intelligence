import pandas as pd
from sqlalchemy import text
from src.db import engine

sample_data = [
    {
        "county": "Dublin",
        "area": "Dublin",
        "year": 2025,
        "quarter": "Q1",
        "average_rent": 2100,
        "source": "RTB"
    },
    {
        "county": "Cork",
        "area": "Cork",
        "year": 2025,
        "quarter": "Q1",
        "average_rent": 1650,
        "source": "RTB"
    },
    {
        "county": "Galway",
        "area": "Galway",
        "year": 2025,
        "quarter": "Q1",
        "average_rent": 1500,
        "source": "RTB"
    }
]

df = pd.DataFrame(sample_data)

with engine.connect() as conn:
    for _, row in df.iterrows():
        conn.execute(
            text("""
                INSERT INTO rental_prices
                (county, area, year, quarter, average_rent, source)
                VALUES
                (:county, :area, :year, :quarter, :average_rent, :source)
            """),
            row.to_dict()
        )

    conn.commit()

print("Data inserted successfully!")