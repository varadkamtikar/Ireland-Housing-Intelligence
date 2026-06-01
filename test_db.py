from src.db import engine

with engine.connect() as conn:
    print("Database connected successfully!")