from sqlalchemy import text
from src.db import engine

query = """
DROP TABLE IF EXISTS rental_prices;

CREATE TABLE rental_prices (
    id SERIAL PRIMARY KEY,
    year INTEGER,
    bedrooms VARCHAR(100),
    property_type VARCHAR(150),
    location_code VARCHAR(50),
    location VARCHAR(255),
    average_rent NUMERIC(10,2),
    unit VARCHAR(20),
    source VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

with engine.connect() as conn:
    conn.execute(text(query))
    conn.commit()

print("rental_prices table reset successfully!")