"""ShopSmart Sales Dashboard.

A one-page Streamlit app showing 2024 sales KPIs and charts
(see prd/ecommerce-analytics.md). All calculations live in data.py.
"""
from pathlib import Path

import plotly.express as px
import streamlit as st

from data import (
    load_sales_data,
    sales_by_category,
    sales_by_month,
    sales_by_region,
    total_orders,
    total_sales,
)

# Built from this file's folder so the app finds the CSV wherever it's launched.
DATA_PATH = Path(__file__).parent / "data" / "sales-data.csv"


@st.cache_data
def get_sales_data():
    """Load the sales CSV once; Streamlit reuses the result on every rerun."""
    return load_sales_data(DATA_PATH)


def sales_bar_chart(table, label_column, axis_label):
    """Horizontal bar chart of a sales table, keeping its highest-first order top to bottom."""
    chart = px.bar(
        table,
        x="sales",
        y=label_column,
        orientation="h",
        labels={"sales": "Sales ($)", label_column: axis_label},
    )
    # Plotly draws the first row at the bottom; reverse so the biggest bar is on top.
    chart.update_yaxes(autorange="reversed")
    chart.update_xaxes(tickformat="$,.0f")
    chart.update_traces(hovertemplate="%{y}<br>%{x:$,.2f}<extra></extra>")
    return chart


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
trend_chart = px.line(
    sales_by_month(sales),
    x="month",
    y="sales",
    markers=True,
    labels={"month": "Month", "sales": "Sales ($)"},
)
trend_chart.update_yaxes(tickformat="$,.0f")
trend_chart.update_traces(hovertemplate="%{x|%B %Y}<br>%{y:$,.2f}<extra></extra>")
st.plotly_chart(trend_chart, width="stretch")

# --- Category and region breakdowns ---
category_col, region_col = st.columns(2)
with category_col:
    st.subheader("Sales by Category")
    category_chart = sales_bar_chart(sales_by_category(sales), "category", "Category")
    st.plotly_chart(category_chart, width="stretch")
with region_col:
    st.subheader("Sales by Region")
    region_chart = sales_bar_chart(sales_by_region(sales), "region", "Region")
    st.plotly_chart(region_chart, width="stretch")
