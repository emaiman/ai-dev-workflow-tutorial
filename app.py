"""ShopSmart Sales Dashboard.

A one-page Streamlit app showing 2024 sales KPIs and charts
(see prd/ecommerce-analytics.md). All calculations live in data.py.
"""
from pathlib import Path

import streamlit as st

from data import load_sales_data, total_orders, total_sales

# Built from this file's folder so the app finds the CSV wherever it's launched.
DATA_PATH = Path(__file__).parent / "data" / "sales-data.csv"


@st.cache_data
def get_sales_data():
    """Load the sales CSV once; Streamlit reuses the result on every rerun."""
    return load_sales_data(DATA_PATH)


st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

try:
    sales = get_sales_data()
except (FileNotFoundError, ValueError) as error:
    st.error(f"Could not load sales data: {error}")
    st.stop()

# --- KPI cards ---
kpi_left, kpi_right = st.columns(2)
kpi_left.metric("Total Sales", f"${total_sales(sales):,.0f}")
kpi_right.metric("Total Orders", f"{total_orders(sales):,}")

# --- Sales trend ---
st.subheader("Sales Trend Over Time")
st.caption("Chart coming soon")

# --- Category and region breakdowns ---
category_col, region_col = st.columns(2)
with category_col:
    st.subheader("Sales by Category")
    st.caption("Chart coming soon")
with region_col:
    st.subheader("Sales by Region")
    st.caption("Chart coming soon")
