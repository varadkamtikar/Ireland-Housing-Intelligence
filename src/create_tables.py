from sqlalchemy import text
from src.db import engine

tables_sql = """
CREATE TABLE IF NOT EXISTS rental_prices (
    id SERIAL PRIMARY KEY,
    county VARCHAR(100),
    area VARCHAR(255),
    year INTEGER,
    quarter VARCHAR(10),
    average_rent NUMERIC(10,2),
    source VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS property_prices (
    id SERIAL PRIMARY KEY,
    county VARCHAR(100),
    year INTEGER,
    month INTEGER,
    price_index NUMERIC(10,2),
    source VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS affordability_index (
    id SERIAL PRIMARY KEY,
    county VARCHAR(100),
    average_rent NUMERIC(10,2),
    affordability_score NUMERIC(10,2),
    risk_level VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

with engine.connect() as conn:
    conn.execute(text(tables_sql))
    conn.commit()

print("Tables created successfully!")