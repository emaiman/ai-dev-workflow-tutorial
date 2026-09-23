"""Data loading and sales calculations for the ShopSmart dashboard.

Everything here is plain pandas (no Streamlit), so it can be tested with
pytest without starting the app.
"""
import pandas as pd

REQUIRED_COLUMNS = [
    "date",
    "order_id",
    "product",
    "category",
    "region",
    "quantity",
    "unit_price",
    "total_amount",
]


def load_sales_data(path):
    """Read the sales CSV and parse the date column.

    Raises ValueError naming any required columns that are missing.
    """
    df = pd.read_csv(path)
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {', '.join(missing)}")
    df["date"] = pd.to_datetime(df["date"])
    return df


def total_sales(df):
    """Sum of every order's total, in dollars."""
    return float(df["total_amount"].sum())


def total_orders(df):
    """Number of distinct orders (unique order IDs, not rows)."""
    return int(df["order_id"].nunique())
