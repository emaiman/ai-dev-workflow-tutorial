# ShopSmart Sales Dashboard — Design

**Date:** 2026-09-22
**Source requirements:** `prd/ecommerce-analytics.md` (Phase 1 only)
**Milestone tracking:** `TASKS.md` (TASK-1 … TASK-7)
**Branch:** `feature/sales-dashboard` (no worktree)

## Goal

A single-page Streamlit dashboard that shows ShopSmart's 2024 sales from
`data/sales-data.csv`: two KPI cards, a monthly sales trend, and sales by
category and by region. Code stays simple and readable; all calculations
live in their own tested module.

## Decisions

| Topic | Decision |
|---|---|
| Code structure | Two modules: `data.py` (pandas only) and `app.py` (Streamlit + Plotly) |
| Trend granularity | Monthly (12 points, Jan–Dec 2024) |
| Page title | "ShopSmart Sales Dashboard" (the PRD sketch's "SHOPMART" is treated as a typo) |
| Total Sales format | Whole dollars: `$116,500` |
| Total Orders format | Thousands separator: `482` |
| CSV validation | Check required columns only; raise a clear error naming any missing ones |
| Environment | Plain `venv/` + `requirements.txt` (no uv, no conda) |
| Tests | pytest, for `data.py` only |

## Project Layout

```
app.py              # Streamlit page: title, KPI cards, three charts
data.py             # load + validate CSV, all calculations (pandas only)
tests/test_data.py  # pytest tests for data.py
requirements.txt    # streamlit, pandas, plotly, pytest
data/sales-data.csv # existing source data
venv/               # local virtual environment (already in .gitignore)
```

## `data.py`

Pure pandas. It never imports Streamlit, so tests run without starting the app.

| Function | Returns |
|---|---|
| `load_sales_data(path)` | DataFrame with `date` parsed as datetime. Raises `ValueError("Missing columns: ...")` if any of `date, order_id, product, category, region, quantity, unit_price, total_amount` is absent. |
| `total_sales(df)` | float: sum of `total_amount` |
| `total_orders(df)` | int: number of unique `order_id` values |
| `sales_by_month(df)` | DataFrame with columns `month` (datetime, first day of each month) and `sales`, one row per month, in date order |
| `sales_by_category(df)` | DataFrame with columns `category`, `sales`, sorted highest to lowest |
| `sales_by_region(df)` | DataFrame with columns `region`, `sales`, sorted highest to lowest |

- `total_orders` counts unique order IDs rather than rows. Today the two are
  equal (482), but unique IDs stay correct if an order ever spans several rows.
- The sorting is done here, not in the chart code, so the tests can check it.
- No formatting happens here. Functions return plain numbers and DataFrames.

## `app.py`

Layout, top to bottom:

1. `st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")` and `st.title`.
2. Two KPI cards side by side (`st.columns(2)` + `st.metric`):
   Total Sales (`f"${value:,.0f}"`) and Total Orders (`f"{value:,}"`).
3. "Sales Trend Over Time": full-width Plotly line chart of monthly sales,
   with markers, axis titles "Month" and "Sales ($)".
4. Two charts side by side (`st.columns(2)`): "Sales by Category" and
   "Sales by Region", each a horizontal Plotly bar chart with the largest bar
   on top, one bar color, and axis title "Sales ($)".

All chart tooltips show exact dollar values with cents (e.g., `$42,683.67`).
Charts fill their column using the installed Streamlit version's
non-deprecated full-width option (`width="stretch"` in current releases;
the older `use_container_width=True` prints a deprecation warning), and use
Plotly's default theme.

**Data flow:** A small `@st.cache_data` function in `app.py` wraps
`load_sales_data`, so the CSV is read once rather than on every Streamlit
rerun. That data goes to the `data.py` functions, and their results go to
`st.metric` and the Plotly figures. `app.py` does no calculations itself.

**CSV path:** Built relative to `app.py`'s own folder
(`Path(__file__).parent / "data" / "sales-data.csv"`), so the app works
no matter which folder it's launched from, including on Streamlit Cloud.

**Error handling:** If loading fails (file missing or required columns
absent), the page shows `st.error("Could not load sales data: <reason>")`
and calls `st.stop()`, so users see a readable message instead of a traceback.

## Testing

`tests/test_data.py` runs against the real CSV. Expected values were
calculated separately with Python's built-in `csv` module:

- `total_sales` ≈ 116500.21 (compared with `pytest.approx`)
- `total_orders` == 482
- `sales_by_month`: 12 rows, in chronological order, summing to the total
- `sales_by_category`: 5 rows, Electronics first ($42,683.67), sorted highest to lowest
- `sales_by_region`: 4 rows, North first ($38,857.24), sorted highest to lowest
- `load_sales_data`: raises `ValueError` naming the missing column, using a
  small CSV written to pytest's `tmp_path`

`data.py` is built test-first: write a failing test, run pytest and see it
fail, write the code, then run pytest and see it pass. `app.py` is checked by
running `streamlit run app.py` and looking at the page.

## Milestone Mapping

| Milestone | Scope |
|---|---|
| TASK-1 | Create `venv/`, `requirements.txt`, and an `app.py` that shows the title |
| TASK-2 | `load_sales_data` + column check (tests first), and placeholder page sections |
| TASK-3 | `total_sales`, `total_orders` (tests first), then the KPI cards |
| TASK-4 | `sales_by_month` (tests first), then the trend line chart |
| TASK-5 | `sales_by_category`, `sales_by_region` (tests first), then the two bar charts |
| TASK-6 | Full test run, check values against the CSV, confirm the page loads within 5 s with no errors or warnings, tidy code and comments |
| TASK-7 | **Done by the user, not by Claude:** after merging to `main`, deploy to Streamlit Community Cloud from `main` |

Every commit message starts with its milestone ID (e.g., `TASK-3: Add KPI cards`).
When a milestone finishes, its entry in `TASKS.md` moves to Done and its
Commit line is filled in.

## Out of Scope

Everything in the PRD's Phase 2: filters and date ranges, authentication,
export, alerts, drill-down, database integration, and mobile-specific
layout. Also no custom theming beyond clear labels.
