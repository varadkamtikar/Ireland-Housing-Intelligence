from sqlalchemy import text
from src.db import engine

tables_sql = """
CREATE TABLE IF NOT EXISTS rental_prices (
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