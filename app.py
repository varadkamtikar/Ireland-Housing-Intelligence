import streamlit as st

st.set_page_config(
    page_title="Ireland Housing Intelligence",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

pg = st.navigation([
    st.Page("home.py",                    title="Homepage",        icon="🏠"),
    st.Page("pages/0_Overview.py",        title="Overview",        icon="📊"),
    st.Page("pages/1_Rent_Trends.py",     title="Rent Trends",     icon="📈"),
    st.Page("pages/2_Property_Prices.py", title="Property Prices", icon="🏡"),
    st.Page("pages/3_Affordability.py",   title="Affordability",   icon="⚖️"),
])

pg.run()
