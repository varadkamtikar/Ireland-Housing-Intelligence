import pandas as pd
import streamlit as st
from src.db import engine


@st.cache_data(ttl=3600)
def load_rental_data() -> pd.DataFrame:
    try:
        return pd.read_sql(
            """
            SELECT year, bedrooms, property_type, location_code, location, average_rent, unit, source
            FROM rental_prices
            WHERE average_rent IS NOT NULL
            """,
            engine,
        )
    except Exception as e:
        st.error(f"Database unavailable: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def load_property_prices() -> pd.DataFrame:
    try:
        return pd.read_sql(
            """
            SELECT county, property_type, year, month, price_index, source
            FROM property_prices
            WHERE price_index IS NOT NULL
            """,
            engine,
        )
    except Exception as e:
        st.error(f"Database unavailable: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def load_affordability() -> pd.DataFrame:
    try:
        return pd.read_sql(
            """
            SELECT county, average_rent, affordability_score, risk_level
            FROM affordability_index
            """,
            engine,
        )
    except Exception as e:
        st.error(f"Database unavailable: {e}")
        return pd.DataFrame()
