"""Tests for data.py, checked against the real sales CSV."""
from pathlib import Path

import pandas as pd
import pytest

from data import load_sales_data, total_orders, total_sales

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
