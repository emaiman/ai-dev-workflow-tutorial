"""Tests for data.py, checked against the real sales CSV."""
from pathlib import Path

import pandas as pd
import pytest

from data import (
    load_sales_data,
    sales_by_category,
    sales_by_month,
    sales_by_region,
    total_orders,
    total_sales,
)

CSV_PATH = Path(__file__).parent.parent / "data" / "sales-data.csv"


@pytest.fixture
def sales():
    """The real sales data, loaded fresh for each test."""
    return load_sales_data(CSV_PATH)


def test_load_sales_data_reads_every_row(sales):
    assert len(sales) == 482
    assert sales["category"].nunique() == 5
    assert sales["region"].nunique() == 4


def test_load_sales_data_parses_dates(sales):
    assert pd.api.types.is_datetime64_any_dtype(sales["date"])


def test_load_sales_data_reports_missing_columns(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("date,order_id\n2024-01-01,ORD-1\n")
    with pytest.raises(ValueError, match="Missing columns: product"):
        load_sales_data(bad_csv)


def test_total_sales_matches_csv(sales):
    assert total_sales(sales) == pytest.approx(116500.21)


def test_total_orders_matches_csv(sales):
    assert total_orders(sales) == 482


def test_total_orders_counts_each_order_once():
    # An order spread over two rows still counts as one order.
    df = pd.DataFrame({"order_id": ["ORD-1", "ORD-1", "ORD-2"]})
    assert total_orders(df) == 2


def test_sales_by_month_has_one_row_per_month_in_order(sales):
    monthly = sales_by_month(sales)
    assert list(monthly.columns) == ["month", "sales"]
    assert len(monthly) == 12
    assert monthly["month"].is_monotonic_increasing
    assert monthly["month"].iloc[0] == pd.Timestamp("2024-01-01")


def test_sales_by_month_adds_up_to_total_sales(sales):
    assert sales_by_month(sales)["sales"].sum() == pytest.approx(116500.21)


def test_sales_by_category_lists_every_category_highest_first(sales):
    by_category = sales_by_category(sales)
    assert list(by_category.columns) == ["category", "sales"]
    assert set(by_category["category"]) == {
        "Electronics",
        "Accessories",
        "Audio",
        "Wearables",
        "Smart Home",
    }
    assert by_category["sales"].is_monotonic_decreasing


def test_sales_by_category_top_is_electronics(sales):
    top = sales_by_category(sales).iloc[0]
    assert top["category"] == "Electronics"
    assert top["sales"] == pytest.approx(42683.67)


def test_sales_by_region_lists_every_region_highest_first(sales):
    by_region = sales_by_region(sales)
    assert list(by_region.columns) == ["region", "sales"]
    assert set(by_region["region"]) == {"North", "South", "East", "West"}
    assert by_region["sales"].is_monotonic_decreasing


def test_sales_by_region_top_is_north(sales):
    top = sales_by_region(sales).iloc[0]
    assert top["region"] == "North"
    assert top["sales"] == pytest.approx(38857.24)
