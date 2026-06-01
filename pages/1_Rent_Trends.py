import streamlit as st
import pandas as pd
import plotly.express as px
from src.db import engine

st.set_page_config(
    page_title="Rent Trends",
    layout="wide"
)

st.title("Rent Trends in Ireland")

# Load data
df = pd.read_sql(
    """
    SELECT
        year,
        bedrooms,
        property_type,
        location,
        average_rent
    FROM rental_prices
    WHERE average_rent IS NOT NULL
    """,
    engine
)

if df.empty:
    st.warning("No rental data found in the database.")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")

selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["year"].dropna().unique(), reverse=True)
)

selected_property_type = st.sidebar.selectbox(
    "Select Property Type",
    ["All"] + sorted(df["property_type"].dropna().unique())
)

selected_bedrooms = st.sidebar.selectbox(
    "Select Bedrooms",
    ["All"] + sorted(df["bedrooms"].dropna().unique())
)

# Apply filters
filtered_df = df[df["year"] == selected_year]

if selected_property_type != "All":
    filtered_df = filtered_df[filtered_df["property_type"] == selected_property_type]

if selected_bedrooms != "All":
    filtered_df = filtered_df[filtered_df["bedrooms"] == selected_bedrooms]

# KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", len(filtered_df))

with col2:
    st.metric("Average Rent", f"€{filtered_df['average_rent'].mean():,.2f}")

with col3:
    highest_location = filtered_df.loc[filtered_df["average_rent"].idxmax(), "location"]
    st.metric("Highest Rent Location", highest_location)

with col4:
    lowest_location = filtered_df.loc[filtered_df["average_rent"].idxmin(), "location"]
    st.metric("Lowest Rent Location", lowest_location)

# Top 10 expensive locations
st.subheader("Top 10 Most Expensive Locations")

top_expensive = (
    filtered_df.groupby("location")["average_rent"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_expensive = px.bar(
    top_expensive,
    x="average_rent",
    y="location",
    orientation="h",
    title="Top 10 Most Expensive Rental Locations"
)

st.plotly_chart(fig_expensive, use_container_width=True)

# Top 10 cheapest locations
st.subheader("Top 10 Cheapest Locations")

top_cheapest = (
    filtered_df.groupby("location")["average_rent"]
    .mean()
    .sort_values(ascending=True)
    .head(10)
    .reset_index()
)

fig_cheapest = px.bar(
    top_cheapest,
    x="average_rent",
    y="location",
    orientation="h",
    title="Top 10 Cheapest Rental Locations"
)

st.plotly_chart(fig_cheapest, use_container_width=True)

# Rent trend over time
st.subheader("Average Rent Trend Over Time")

trend_df = (
    df.groupby("year")["average_rent"]
    .mean()
    .reset_index()
)

fig_trend = px.line(
    trend_df,
    x="year",
    y="average_rent",
    markers=True,
    title="Average Rent Trend in Ireland"
)

st.plotly_chart(fig_trend, use_container_width=True)

# Raw data
with st.expander("View Filtered Data"):
    st.dataframe(filtered_df)