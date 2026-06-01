import streamlit as st

st.set_page_config(
    page_title="Ireland Housing Intelligence",
    page_icon="🏠",
    layout="wide"
)

st.title("Ireland Housing Intelligence Platform")

st.markdown("""
This platform analyses Ireland's housing market using rental, property price,
affordability, and regional housing data.

### Planned Features
- Rental price trends
- Property price trends
- County comparison
- Affordability analysis
- Housing pressure prediction
- Interactive maps
""")