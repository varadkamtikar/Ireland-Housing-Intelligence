import pandas as pd
from sqlalchemy import text
from src.db import engine

CSV_PATH = "data/raw/rtb.csv"

def load_rtb_data():
    df = pd.read_csv(CSV_PATH, low_memory=False)

    df = df[
        [
            "Year",
            "Number of Bedrooms",
            "Property Type",
            "C03004V03625",
            "Location",
            "UNIT",
            "VALUE",
        ]
    ].copy()

    df = df.rename(
        columns={
            "Year": "year",
            "Number of Bedrooms": "bedrooms",
            "Property Type": "property_type",
            "C03004V03625": "location_code",
            "Location": "location",
            "UNIT": "unit",
            "VALUE": "average_rent",
        }
    )

    df["average_rent"] = pd.to_numeric(df["average_rent"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    df = df.dropna(subset=["year", "location", "average_rent"])

    df["year"] = df["year"].astype(int)
    df["source"] = "RTB Average Monthly Rent Report"

    with engine.connect() as conn:
        conn.execute(text("DELETE FROM rental_prices;"))
        conn.commit()

    df.to_sql(
        "rental_prices",
        engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=5000,
    )

    print(f"Inserted {len(df)} RTB rental records successfully!")

if __name__ == "__main__":
    load_rtb_data()