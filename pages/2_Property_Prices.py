import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.data import load_property_prices

st.title("🏡 Property Prices")
st.markdown(
    "Ireland's Residential Property Price Index from 2005 to today — "
    "sourced directly from the CSO via the PxStat API. "
    "**Base year: 2015 = 100.** An index of 175 means prices are 75% above 2015 levels."
)

df = load_property_prices()

if df.empty:
    st.warning("No property price data found. Run `python -m src.fetch_cso_data` to load data.")
    st.stop()

# Build a proper date column for time-series plotting
df["date"] = pd.to_datetime(df[["year", "month"]].assign(day=1))

# ── Sidebar filters ────────────────────────────────────────────────────────────
st.sidebar.header("Filters")

property_types = sorted(df["property_type"].unique())
default_type   = "All Residential" if "All Residential" in property_types else property_types[0]
selected_type  = st.sidebar.selectbox("Property Type", property_types,
                                       index=property_types.index(default_type))

all_regions   = sorted(df["county"].unique())
default_regions = ["National", "Dublin", "National excluding Dublin"]
selected_regions = st.sidebar.multiselect(
    "Regions for trend chart",
    all_regions,
    default=[r for r in default_regions if r in all_regions],
)

# Working slice: selected property type only
type_df = df[df["property_type"] == selected_type].copy()

# ── KPIs ───────────────────────────────────────────────────────────────────────
national_ts = type_df[type_df["county"] == "National"].sort_values("date")

if national_ts.empty:
    st.warning("National data not available for the selected property type.")
    st.stop()

latest        = national_ts.iloc[-1]
national_idx  = latest["price_index"]
latest_year   = int(latest["year"])
latest_month  = int(latest["month"])
latest_label  = latest["date"].strftime("%b %Y")

# Year-over-year change
yoy_delta = None
if len(national_ts) >= 13:
    prev_idx  = national_ts.iloc[-13]["price_index"]
    yoy_delta = ((national_idx - prev_idx) / prev_idx) * 100

# Dublin stats
dublin_ts  = type_df[type_df["county"] == "Dublin"].sort_values("date")
dublin_idx = dublin_ts.iloc[-1]["price_index"] if not dublin_ts.empty else None
dublin_premium = ((dublin_idx - national_idx) / national_idx * 100) if dublin_idx else None

# Peak national
peak_row   = national_ts.loc[national_ts["price_index"].idxmax()]
peak_idx   = peak_row["price_index"]
peak_label = peak_row["date"].strftime("%b %Y")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        f"National Index ({latest_label})",
        f"{national_idx:.1f}",
        delta=f"{yoy_delta:+.1f}% year-on-year" if yoy_delta is not None else None,
    )
with k2:
    st.metric(
        f"Dublin Index ({latest_label})",
        f"{dublin_idx:.1f}" if dublin_idx else "N/A",
        delta=f"{dublin_premium:+.1f}% vs National" if dublin_premium else None,
    )
with k3:
    st.metric("All-time Peak (National)", f"{peak_idx:.1f}", delta=peak_label, delta_color="off")
with k4:
    st.metric("Above 2015 baseline", f"{national_idx - 100:+.1f} pts",
              delta="Base: 2015 = 100", delta_color="off")

st.divider()

# ── Chart 1: Price trend for selected regions ──────────────────────────────────
st.subheader("Price Index Trend Over Time")

if not selected_regions:
    st.info("Select at least one region in the sidebar.")
else:
    trend_df = (
        type_df[type_df["county"].isin(selected_regions)]
        .sort_values("date")
    )

    color_seq = ["#4F46E5", "#EF4444", "#10B981", "#F59E0B",
                 "#8B5CF6", "#EC4899", "#06B6D4", "#84CC16"]
    color_map  = {r: color_seq[i % len(color_seq)] for i, r in enumerate(selected_regions)}

    fig_trend = go.Figure()
    for region in selected_regions:
        rdf = trend_df[trend_df["county"] == region]
        fig_trend.add_trace(go.Scatter(
            x=rdf["date"], y=rdf["price_index"],
            mode="lines",
            name=region,
            line=dict(color=color_map[region], width=2.5),
            hovertemplate=f"<b>{region}</b><br>%{{x|%b %Y}}: %{{y:.1f}}<extra></extra>",
        ))

    fig_trend.add_hline(
        y=100, line_dash="dot", line_color="#94A3B8",
        annotation_text="2015 baseline (100)",
        annotation_font_color="#94A3B8",
    )
    fig_trend.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        height=400,
        hovermode="x unified",
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", title="Price Index"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=40, b=0),
    )
    st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})

st.divider()

# ── Charts 2 & 3 side by side ──────────────────────────────────────────────────
left, right = st.columns(2)

with left:
    st.subheader("Regional Snapshot")

    latest_date     = type_df["date"].max()
    latest_regional = (
        type_df[type_df["date"] == latest_date]
        .sort_values("price_index", ascending=True)
        .reset_index(drop=True)
    )

    fig_bar = px.bar(
        latest_regional,
        x="price_index",
        y="county",
        orientation="h",
        title=f"Price Index by Region — {latest_label}",
        color="price_index",
        color_continuous_scale=[[0, "#DBEAFE"], [0.5, "#4F46E5"], [1, "#1E1B4B"]],
        labels={"price_index": "Index", "county": ""},
    )
    fig_bar.add_vline(
        x=100, line_dash="dot", line_color="#94A3B8",
        annotation_text="2015 = 100", annotation_font_color="#94A3B8",
    )
    fig_bar.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        height=400, coloraxis_showscale=False,
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9", title="Price Index"),
        yaxis=dict(showgrid=False),
        margin=dict(l=0, r=0, t=40, b=0),
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

with right:
    st.subheader("Houses vs Apartments — National")

    national_all = df[df["county"] == "National"].sort_values("date")

    fig_types = go.Figure()
    type_colors = {
        "All Residential": "#4F46E5",
        "Houses":          "#10B981",
        "Apartments":      "#F59E0B",
    }
    for pt in national_all["property_type"].unique():
        sub = national_all[national_all["property_type"] == pt]
        fig_types.add_trace(go.Scatter(
            x=sub["date"], y=sub["price_index"],
            mode="lines", name=pt,
            line=dict(color=type_colors.get(pt, "#6B7280"), width=2.5),
            hovertemplate=f"<b>{pt}</b><br>%{{x|%b %Y}}: %{{y:.1f}}<extra></extra>",
        ))

    fig_types.add_hline(
        y=100, line_dash="dot", line_color="#94A3B8",
        annotation_text="2015 = 100", annotation_font_color="#94A3B8",
    )
    fig_types.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        height=400, hovermode="x unified",
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", title="Price Index"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=40, b=0),
    )
    st.plotly_chart(fig_types, use_container_width=True, config={"displayModeBar": False})

# ── Context callout ────────────────────────────────────────────────────────────
st.divider()
st.info(
    "**How to read this:** The index is set to 100 in 2015. "
    "Dublin's index above the national average shows the capital's premium. "
    "Apartment prices are more volatile than houses — particularly visible during the 2008–2013 crash and post-2020 recovery."
)

with st.expander("View Raw Data"):
    display_df = (
        type_df[["county", "property_type", "year", "month", "price_index"]]
        .sort_values(["county", "year", "month"])
        .reset_index(drop=True)
    )
    st.dataframe(display_df, use_container_width=True)
