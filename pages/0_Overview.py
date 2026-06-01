import streamlit as st
import pandas as pd
import plotly.express as px
from src.db import engine

st.set_page_config(
    page_title="Housing Overview",
    layout="wide"
)

st.title("Ireland Housing Intelligence Overview")

st.markdown("""
This platform analyses Ireland's rental market using official RTB rental data.
It helps identify rent trends, expensive locations, cheaper areas, and housing pressure patterns.
""")

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
    st.warning("No rental data found.")
    st.stop()

# KPIs
total_records = len(df)
avg_rent = df["average_rent"].mean()
highest_location = df.loc[df["average_rent"].idxmax(), "location"]
lowest_location = df.loc[df["average_rent"].idxmin(), "location"]
locations_count = df["location"].nunique()
years_covered = f"{df['year'].min()} - {df['year'].max()}"

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Rental Records", f"{total_records:,}")

with col2:
    st.metric("Average Rent", f"€{avg_rent:,.2f}")

with col3:
    st.metric("Locations Covered", f"{locations_count:,}")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("Years Covered", years_covered)

with col5:
    st.metric("Highest Rent Location", highest_location)

with col6:
    st.metric("Lowest Rent Location", lowest_location)

st.divider()

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
    title="Average Rental Price Trend in Ireland"
)

st.plotly_chart(fig_trend, use_container_width=True)

# Two columns
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Top 10 Most Expensive Locations")

    latest_year = df["year"].max()
    latest_df = df[df["year"] == latest_year]

    top_expensive = (
        latest_df.groupby("location")["average_rent"]
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
        title=f"Most Expensive Locations in {latest_year}"
    )

    st.plotly_chart(fig_expensive, use_container_width=True)

with right_col:
    st.subheader("Rent Distribution")

    fig_hist = px.histogram(
        latest_df,
        x="average_rent",
        nbins=40,
        title=f"Rent Distribution in {latest_year}"
    )

    st.plotly_chart(fig_hist, use_container_width=True)

# Property type analysis
st.subheader("Average Rent by Property Type")

property_df = (
    latest_df.groupby("property_type")["average_rent"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig_property = px.bar(
    property_df,
    x="property_type",
    y="average_rent",
    title=f"Average Rent by Property Type in {latest_year}"
)

st.plotly_chart(fig_property, use_container_width=True)

with st.expander("View Raw Dataset Sample"):
    st.dataframe(df.head(100))