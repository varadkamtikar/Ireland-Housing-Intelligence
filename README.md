<div align="center">

# 🏠 Ireland Housing Intelligence

**Explore Ireland's housing market through real data, interactive charts, and live insights.**

Built with official RTB rental data — tracking rent trends, property prices, and affordability across every county in Ireland.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.58-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)

[![Live App](https://img.shields.io/badge/Live%20App-ireland--housing--intelligence.streamlit.app-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://ireland-housing-intelligence.streamlit.app)

</div>

---

## ✨ What This Is

Ireland's housing crisis is one of the most pressing issues facing the country. This platform cuts through the noise by pulling **official government data** into a single, interactive dashboard — making it easy to see where rents are rising, which counties are most affordable, and how the market has shifted over the past decade.

> Data sourced from the **Residential Tenancies Board (RTB)** and the **Central Statistics Office (CSO)** — the same sources policymakers use.

---

## 🖥️ Platform Modules

| Module | Status | Description |
|--------|--------|-------------|
| 📊 **Overview Dashboard** | ✅ Live | KPIs, all-time rent trends, location rankings, property type breakdown |
| 📈 **Rent Trends** | ✅ Live | Filter by year, property type, and bedrooms — find cheapest and most expensive areas |
| 🏡 **Property Prices** | 🚧 Coming Soon | CSO property price index by county, price vs rent yield comparison |
| ⚖️ **Affordability Index** | 🚧 Coming Soon | Rent-to-income ratios, Housing Pressure Zone mapping, risk scoring |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL (local or hosted — [Neon](https://neon.tech) recommended for free hosted)

### 1. Clone the repo

```bash
git clone https://github.com/varadkamtikar/Ireland-Housing-Intelligence.git
cd Ireland-Housing-Intelligence
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your database connection string:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/ireland_housing
```

### 5. Set up the database

```bash
# Create tables
python src/create_tables.py

# Load RTB rental data
python src/fetch_rtb_data.py
```

### 6. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🗂️ Project Structure

```
ireland-housing-intelligence/
│
├── app.py                      # Entry point — Streamlit navigation
├── home.py                     # Homepage (hero, stats, feature cards)
│
├── pages/
│   ├── 0_Overview.py           # Overview dashboard
│   ├── 1_Rent_Trends.py        # Rent trends with filters
│   ├── 2_Property_Prices.py    # Property prices (coming soon)
│   └── 3_Affordability.py      # Affordability index (coming soon)
│
├── src/
│   ├── db.py                   # SQLAlchemy engine setup
│   ├── data.py                 # Shared cached data queries
│   ├── create_tables.py        # DB schema initialisation
│   ├── fetch_rtb_data.py       # RTB rental data ETL
│   └── fetch_cso_data.py       # CSO property price ETL (in progress)
│
├── data/
│   └── raw/
│       └── rtb.csv             # Raw RTB average monthly rent data
│
├── requirements.txt
└── .env.example
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | [Streamlit](https://streamlit.io) — multi-page app with custom CSS |
| **Charts** | [Plotly](https://plotly.com/python/) — interactive line, bar, histogram, scatter |
| **Database** | [PostgreSQL](https://postgresql.org) via [SQLAlchemy](https://sqlalchemy.org) |
| **ETL** | [Pandas](https://pandas.pydata.org) — CSV ingestion and data cleaning |
| **Maps** *(planned)* | [Folium](https://python-visualization.github.io/folium/) + [GeoPandas](https://geopandas.org) |
| **ML** *(planned)* | [scikit-learn](https://scikit-learn.org) + [XGBoost](https://xgboost.readthedocs.io) |

---

## 📊 Data Sources

| Source | Dataset | Coverage |
|--------|---------|----------|
| [RTB](https://www.rtb.ie) | Average Monthly Rent Report | 2007–2024, all counties, by property type and bedrooms |
| [CSO](https://www.cso.ie) | Residential Property Price Index | County-level, monthly *(in progress)* |
| [CSO](https://www.cso.ie) | Earnings and Labour Costs | For affordability scoring *(planned)* |

---

## 🗺️ Roadmap

- [x] RTB rental data ETL pipeline
- [x] Overview dashboard with KPIs and charts
- [x] Rent Trends page with year/type/bedroom filters
- [x] Shared cached data layer (`src/data.py`)
- [ ] CSO Property Price Register integration
- [ ] Property Prices dashboard
- [ ] Affordability Index with rent-to-income ratios
- [ ] Interactive county choropleth map (Folium)
- [ ] Housing Pressure Zone (HPZ) highlighting
- [ ] Rent forecasting model (XGBoost)
- [ ] Streamlit Community Cloud deployment

---

## ⚙️ Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |

---

## 🤝 Contributing

Contributions are welcome. If you have access to additional Irish housing datasets or want to build out one of the planned modules:

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/property-prices`
3. Commit your changes
4. Open a pull request

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

<div align="center">

Built by [Varad Kamtikar](https://github.com/varadkamtikar) &nbsp;·&nbsp; Data from RTB &amp; CSO Ireland

</div>
