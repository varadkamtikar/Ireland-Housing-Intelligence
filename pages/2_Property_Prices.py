import streamlit as st

st.title("🏡 Property Prices")

st.markdown("""
<div style="
    background: linear-gradient(135deg, #FEF3C7, #FDE68A);
    border-radius: 14px;
    padding: 36px 32px;
    border-left: 4px solid #F59E0B;
    margin-top: 16px;
">
    <h3 style="color:#92400E;margin:0 0 10px;">Coming Soon</h3>
    <p style="color:#78350F;margin:0;font-size:15px;line-height:1.6;">
        This module will display CSO property price index data by county,
        compare price trends over time, and correlate against rental yields.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### Planned Features")
st.markdown("""
- **County-level price index** from CSO Property Price Register
- **Year-over-year** price change tracking
- **Rental yield calculator** — compare buy vs rent
- **Interactive county map** with price heat overlay
""")
