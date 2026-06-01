import requests
import pandas as pd
from sqlalchemy import text
from src.db import engine

CSO_URL = (
    "https://ws.cso.ie/public/api.restful/"
    "PxStat.Data.Cube_API.ReadDataset/HPM09/JSON-stat/2.0/en"
)

TARGET_STATISTIC = "HPM09C01"  # Residential Property Price Index only

# Maps the raw suffix in the CSO label to a clean property type name
PROPERTY_TYPE_MAP = {
    "all residential properties": "All Residential",
    "houses":                     "Houses",
    "apartments":                 "Apartments",
}


def _parse_label(label: str) -> tuple[str, str]:
    """
    Split a CSO region label into (region, property_type).

    'Dublin - all residential properties' → ('Dublin', 'All Residential')
    'National excluding Dublin - houses'  → ('National excluding Dublin', 'Houses')
    """
    region, raw_type = label.rsplit(" - ", 1)
    property_type = PROPERTY_TYPE_MAP.get(raw_type.lower(), raw_type.title())
    return region.strip(), property_type


def fetch_property_price_index() -> None:
    print("Fetching CSO Residential Property Price Index (HPM09)...")

    resp = requests.get(CSO_URL, timeout=30)
    resp.raise_for_status()
    js = resp.json()

    # Dimension order: ["STATISTIC", "TLIST(M1)", "C02803V03373"]
    dim_ids    = js["id"]
    dimensions = js["dimension"]
    values     = js["value"]

    stat_dim     = dim_ids[0]
    month_dim    = dim_ids[1]
    proptype_dim = dim_ids[2]

    # index is a plain list of codes in order
    stat_codes     = dimensions[stat_dim]["category"]["index"]
    month_codes    = dimensions[month_dim]["category"]["index"]
    proptype_codes = dimensions[proptype_dim]["category"]["index"]
    proptype_labels = dimensions[proptype_dim]["category"]["label"]

    n_months    = len(month_codes)
    n_proptypes = len(proptype_codes)

    stat_pos    = stat_codes.index(TARGET_STATISTIC)
    month_pos   = {c: i for i, c in enumerate(month_codes)}
    proptype_pos = {c: i for i, c in enumerate(proptype_codes)}

    print(f"  Regions/types available: {n_proptypes} | Months: {n_months}")

    records = []
    for pt_code in proptype_codes:
        label = proptype_labels.get(pt_code, pt_code)
        region, property_type = _parse_label(label)
        pt_pos = proptype_pos[pt_code]

        for month_code in month_codes:
            m_pos = month_pos[month_code]
            flat_idx = stat_pos * n_months * n_proptypes + m_pos * n_proptypes + pt_pos
            val = values[flat_idx]

            if val is None:
                continue

            # Month code format: "200501" → year=2005, month=1
            year  = int(month_code[:4])
            month = int(month_code[4:])

            records.append({
                "county":        region,
                "property_type": property_type,
                "year":          year,
                "month":         month,
                "price_index":   float(val),
                "source":        "CSO Residential Property Price Index (HPM09)",
            })

    df = pd.DataFrame(records)
    print(
        f"  Parsed {len(df):,} records | "
        f"{df['county'].nunique()} regions | "
        f"{df['property_type'].unique().tolist()} | "
        f"{df['year'].min()}–{df['year'].max()}"
    )

    with engine.connect() as conn:
        conn.execute(text("DELETE FROM property_prices;"))
        conn.commit()

    df.to_sql(
        "property_prices",
        engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=5000,
    )
    print(f"  Inserted {len(df):,} records into property_prices. Done.")


if __name__ == "__main__":
    fetch_property_price_index()
