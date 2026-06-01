import streamlit as st
import plotly.graph_objects as go
from src.data import load_rental_data

st.markdown("""
<style>
/* ── Hero ────────────────────────────────────────────────── */
.hero {
    background: linear-gradient(135deg, #0F172A 0%, #1E3A5F 40%, #4F46E5 80%, #7C3AED 100%);
    border-radius: 20px;
    padding: 64px 52px 56px;
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -80px;
    width: 420px; height: 420px;
    background: radial-gradient(circle, rgba(124,58,237,0.35) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 30%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(79,70,229,0.25) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 50px;
    padding: 6px 16px;
    color: rgba(255,255,255,0.9);
    font-size: 13px;
    font-weight: 500;
    margin-bottom: 28px;
    letter-spacing: 0.3px;
}
.hero-title {
    font-size: 58px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.08;
    margin: 0 0 20px 0;
    letter-spacing: -2px;
}
.hero-title span {
    background: linear-gradient(90deg, #A5B4FC, #C4B5FD);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    font-size: 17px;
    color: rgba(255,255,255,0.72);
    max-width: 560px;
    line-height: 1.65;
    margin: 0;
}

/* ── Stats ───────────────────────────────────────────────── */
.stat-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 28px 20px 24px;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07), 0 6px 20px rgba(0,0,0,0.05);
    border-top: 3px solid #4F46E5;
    height: 100%;
}
.stat-icon { font-size: 26px; margin-bottom: 6px; }
.stat-value {
    font-size: 30px;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -1px;
    margin: 4px 0 6px;
    line-height: 1;
}
.stat-label {
    font-size: 11.5px;
    color: #64748B;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.9px;
}

/* ── Feature cards ───────────────────────────────────────── */
.feature-card {
    background: #ffffff;
    border-radius: 18px;
    padding: 30px 24px 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07), 0 6px 20px rgba(0,0,0,0.04);
    border: 1.5px solid #F1F5F9;
    height: 100%;
    transition: box-shadow 0.25s ease, border-color 0.25s ease, transform 0.25s ease;
}
.feature-card:hover {
    box-shadow: 0 12px 32px rgba(79,70,229,0.13);
    border-color: #C7D2FE;
    transform: translateY(-3px);
}
.feature-icon {
    font-size: 38px;
    margin-bottom: 14px;
    display: block;
    line-height: 1;
}
.feature-title {
    font-size: 17px;
    font-weight: 700;
    color: #0F172A;
    margin: 0 0 10px;
}
.feature-desc {
    font-size: 13.5px;
    color: #64748B;
    line-height: 1.65;
    margin: 0 0 18px;
}
.badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 10.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}
.badge-live { background: #DCFCE7; color: #15803D; }
.badge-soon { background: #FEF3C7; color: #92400E; }

/* ── Section headings ────────────────────────────────────── */
.sec-title {
    font-size: 26px;
    font-weight: 800;
    color: #0F172A;
    margin: 0 0 4px;
    letter-spacing: -0.5px;
}
.sec-sub {
    font-size: 14.5px;
    color: #64748B;
    margin: 0 0 28px;
}

/* ── Divider ─────────────────────────────────────────────── */
.hdivider {
    height: 1px;
    background: linear-gradient(90deg, #E2E8F0 0%, rgba(226,232,240,0) 100%);
    margin: 44px 0 40px;
}

/* ── Chart card ──────────────────────────────────────────── */
.chart-card {
    background: #ffffff;
    border-radius: 18px;
    padding: 28px 28px 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07), 0 6px 20px rgba(0,0,0,0.04);
    border: 1.5px solid #F1F5F9;
}

/* ── Footer ──────────────────────────────────────────────── */
.footer {
    text-align: center;
    padding: 32px 0 16px;
    color: #94A3B8;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🇮🇪 Powered by Official RTB Data</div>
    <h1 class="hero-title">Ireland Housing<br><span>Intelligence</span></h1>
    <p class="hero-subtitle">
        Explore rental trends, property prices, and affordability across Ireland
        using official government data — interactive charts, county comparisons, and live insights.
    </p>
</div>
""", unsafe_allow_html=True)

# CTA buttons
cta1, cta2, _ = st.columns([1.2, 1.4, 4])
with cta1:
    st.page_link("pages/0_Overview.py", label="📊 &nbsp;Explore Data", use_container_width=True)
with cta2:
    st.page_link("pages/1_Rent_Trends.py", label="📈 &nbsp;View Rent Trends", use_container_width=True)

# ── Live Stats ────────────────────────────────────────────────────────────────
df = load_rental_data()

if not df.empty:
    st.markdown('<div class="hdivider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="sec-title">At a Glance</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-sub">Key metrics from the latest RTB dataset</p>', unsafe_allow_html=True)

    total_records = len(df)
    avg_rent = df["average_rent"].mean()
    max_rent = df["average_rent"].max()
    locations = df["location"].nunique()
    years_str = f"{int(df['year'].min())}–{int(df['year'].max())}"
    latest_yr = int(df["year"].max())
    latest_avg = df[df["year"] == latest_yr]["average_rent"].mean()

    s1, s2, s3, s4, s5 = st.columns(5)
    for col, icon, val, label in [
        (s1, "📋", f"{total_records:,}", "Rental Records"),
        (s2, "📅", years_str,             "Years Covered"),
        (s3, "📍", f"{locations}",        "Locations"),
        (s4, "💶", f"€{avg_rent:,.0f}",   "All-time Avg Rent"),
        (s5, "🏆", f"€{max_rent:,.0f}",   "Peak Rent Recorded"),
    ]:
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">{icon}</div>
                <div class="stat-value">{val}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Feature Cards ─────────────────────────────────────────────────────────────
st.markdown('<div class="hdivider"></div>', unsafe_allow_html=True)
st.markdown('<p class="sec-title">Explore the Platform</p>', unsafe_allow_html=True)
st.markdown('<p class="sec-sub">Four modules covering Ireland\'s full housing picture</p>', unsafe_allow_html=True)

features = [
    ("📊", "Overview Dashboard",
     "A bird's-eye view of the entire rental market — KPIs, time trends, rent distribution, and property-type breakdowns.",
     "live", "pages/0_Overview.py"),
    ("📈", "Rent Trends",
     "Drill into rent movements by year, property type, and bedrooms. Identify the cheapest and most expensive areas.",
     "live", "pages/1_Rent_Trends.py"),
    ("🏡", "Property Prices",
     "Track CSO property price index movements by county and compare trends against rental yields over time.",
     "soon", None),
    ("⚖️", "Affordability Index",
     "Measure rent burden using income-to-rent ratios. Identify housing pressure zones and at-risk counties.",
     "soon", None),
]

fc1, fc2, fc3, fc4 = st.columns(4)
for col, (icon, title, desc, status, page) in zip([fc1, fc2, fc3, fc4], features):
    badge_class = "badge-live" if status == "live" else "badge-soon"
    badge_text  = "Live" if status == "live" else "Coming Soon"
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <span class="feature-icon">{icon}</span>
            <p class="feature-title">{title}</p>
            <p class="feature-desc">{desc}</p>
            <span class="badge {badge_class}">{badge_text}</span>
        </div>
        """, unsafe_allow_html=True)
        if page:
            st.page_link(page, label=f"Open →", use_container_width=True)
        else:
            st.button("Coming Soon", disabled=True, use_container_width=True, key=title)

# ── National Rent Trend Chart ─────────────────────────────────────────────────
if not df.empty:
    st.markdown('<div class="hdivider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="sec-title">National Rent Trend</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-sub">Average monthly rent across Ireland — all property types combined</p>', unsafe_allow_html=True)

    trend = df.groupby("year")["average_rent"].mean().reset_index()
    yoy = trend["average_rent"].pct_change() * 100
    trend["yoy"] = yoy

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trend["year"],
        y=trend["average_rent"],
        fill="tozeroy",
        fillcolor="rgba(79,70,229,0.07)",
        line=dict(color="#4F46E5", width=3),
        mode="lines+markers",
        marker=dict(size=9, color="#4F46E5", line=dict(color="white", width=2)),
        name="Avg Rent",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Avg Rent: <b>€%{y:,.0f}</b>/mo<extra></extra>"
        ),
    ))
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=0, r=0, t=16, b=0),
        height=300,
        xaxis=dict(
            showgrid=False, title=None, tickformat="d",
            tickfont=dict(color="#64748B", size=12),
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#F1F5F9",
            title="Monthly Rent (€)", tickprefix="€",
            tickfont=dict(color="#64748B", size=12),
            title_font=dict(color="#94A3B8", size=12),
        ),
        hovermode="x unified",
        showlegend=False,
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hdivider"></div>
<div class="footer">
    Ireland Housing Intelligence &nbsp;·&nbsp; Data sourced from RTB &amp; CSO &nbsp;·&nbsp; Built with Streamlit
</div>
""", unsafe_allow_html=True)
