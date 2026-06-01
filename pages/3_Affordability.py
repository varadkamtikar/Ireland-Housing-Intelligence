import streamlit as st

st.title("⚖️ Affordability Index")

st.markdown("""
<div style="
    background: linear-gradient(135deg, #EDE9FE, #DDD6FE);
    border-radius: 14px;
    padding: 36px 32px;
    border-left: 4px solid #7C3AED;
    margin-top: 16px;
">
    <h3 style="color:#4C1D95;margin:0 0 10px;">Coming Soon</h3>
    <p style="color:#5B21B6;margin:0;font-size:15px;line-height:1.6;">
        This module will measure rent burden across Irish counties using income-to-rent
        ratios from CSO earnings data and identify housing pressure zones.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### Planned Features")
st.markdown("""
- **Rent-to-income ratio** by county using CSO wage data
- **Housing Pressure Zone (HPZ)** mapping
- **Affordability score** — risk level per area
- **Trend analysis** — how affordability changed over time
""")
