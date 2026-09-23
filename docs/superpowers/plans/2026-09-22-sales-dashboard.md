# ShopSmart Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a one-page Streamlit dashboard showing ShopSmart's 2024 Total Sales, Total Orders, a monthly sales trend, and sales by category and region, then hand it off to the user to deploy.

**Architecture:** Two modules. `data.py` is plain pandas: it loads and checks the CSV and does every calculation, and it is covered by pytest. `app.py` is Streamlit and Plotly: it lays out the page and draws the charts from `data.py`'s results, and it does no calculations itself.

**Tech Stack:** Python 3.11+, Streamlit, pandas, Plotly Express, pytest. The environment is a plain `venv/` with `requirements.txt`.

**Spec:** `docs/superpowers/specs/2026-09-22-sales-dashboard-design.md`

## How This Plan Is Numbered

- **Plan tasks** are numbered **P1–P12**. They are the units of work in this document.
- **Milestones** are **TASK-1 … TASK-7** from `TASKS.md`. Every plan task is labeled with the one milestone it belongs to.
- A milestone may span more than one plan task. For example, TASK-3 is P4 (calculations) plus P5 (KPI cards).

| Plan task | Milestone | Summary | Done by |
|---|---|---|---|
| P1 | TASK-1 | venv, requirements.txt, app.py showing the title | Claude |
| P2 | TASK-2 | `load_sales_data` with required-column check (TDD) | Claude |
| P3 | TASK-2 | App loads data, error handling, placeholder sections | Claude |
| P4 | TASK-3 | `total_sales`, `total_orders` (TDD) | Claude |
| P5 | TASK-3 | KPI cards | Claude |
| P6 | TASK-4 | `sales_by_month` (TDD) | Claude |
| P7 | TASK-4 | Sales trend line chart | Claude |
| P8 | TASK-5 | `sales_by_category`, `sales_by_region` (TDD) | Claude |
| P9 | TASK-5 | Category and region bar charts | Claude |
| P10 | TASK-6 | Verification and refinement | Claude + user review |
| P11 | TASK-7 | Merge `feature/sales-dashboard` into `main` | Claude, only with user's go-ahead |
| P12 | TASK-7 | **Deploy to Streamlit Community Cloud** | 👤 **User** |

## Global Constraints

- Work on the existing branch `feature/sales-dashboard`. **Do not create a git worktree** and do not create other branches.
- Use a plain virtual environment in `venv/` and list dependencies in `requirements.txt`. **No uv, no conda, no Poetry.** `venv/` is already in `.gitignore`.
- Run Python through the venv. On Windows (this machine) that is `venv/Scripts/python`; on macOS/Linux it is `venv/bin/python`. Commands below use the Windows path.
- `data.py` must never import Streamlit. All calculations live in `data.py`; `app.py` does none.
- Page title, exactly: `ShopSmart Sales Dashboard`
- Total Sales format: whole dollars, `f"${value:,.0f}"` → `$116,500`. Total Orders format: `f"{value:,}"` → `482`.
- Tooltips show exact dollars with cents (Plotly format `$,.2f`, e.g. `$42,683.67`).
- Charts fill their column with `st.plotly_chart(fig, width="stretch")`. Do **not** use `use_container_width`, which is deprecated and prints a warning.
- Every commit message starts with the milestone ID, e.g. `TASK-3: Add KPI cards`.
- Keep code simple and readable: short functions, a docstring on each, and a comment only where the reason isn't obvious.
- Out of scope (PRD Phase 2): filters, date pickers, auth, export, alerts, drill-down, databases, custom themes.

### Milestone bookkeeping in `TASKS.md`

- **Starting a milestone:** in the first plan task for that milestone, move the milestone's whole block (heading, description, checkboxes, `Commit:` line) from `## To Do` to `## In Progress`. Include `TASKS.md` in that task's commit.
- **Finishing a milestone:** in the last plan task for that milestone:
  1. Tick its acceptance-criteria checkboxes (`- [ ]` → `- [x]`).
  2. Set its `Commit:` line to the short hash of the milestone's final code commit, from `git log -1 --format=%h`, e.g. `Commit: a1b2c3d`.
  3. Move the block from `## In Progress` to `## Done`.
  4. Commit on its own: `git commit -m "TASK-N: Mark TASK-N done in TASKS.md"`.

### Reference values (computed independently from the CSV with Python's `csv` module)

| Value | Expected |
|---|---|
| Rows / unique order IDs | 482 / 482 |
| Total sales | 116500.21 |
| Date range | 2024-01-03 to 2024-12-31 (12 months) |
| Category order | Electronics 42683.67, Wearables 23698.23, Audio 19638.44, Smart Home 19317.23, Accessories 11162.64 |
| Region order | North 38857.24, West 27463.74, East 26783.53, South 23395.70 |

---

## File Structure

| File | Responsibility | Created in |
|---|---|---|
| `requirements.txt` | Dependency list for local venv and Streamlit Cloud | P1 |
| `app.py` | Streamlit page: title, KPI cards, charts, load-error message | P1 (grows in P3, P5, P7, P9) |
| `pytest.ini` | Tells pytest where tests live and lets them `import data` | P2 |
| `data.py` | CSV loading, column check, all calculations (pandas only) | P2 (grows in P4, P6, P8) |
| `tests/test_data.py` | pytest tests for `data.py` against the real CSV | P2 (grows in P4, P6, P8) |

> **Name note:** the module `data.py` and the folder `data/` (which holds the CSV) share a name. Python prefers the `data.py` module when you `import data`. Until `data.py` exists, `from data import ...` fails with `cannot import name ... from 'data' (unknown location)`, because Python found the folder instead. That is the expected "red" failure in P2.

---

### P1 [TASK-1]: Environment and app skeleton

**Files:**
- Create: `requirements.txt`
- Create: `app.py`
- Modify: `TASKS.md` (TASK-1 → In Progress, then → Done)

**Interfaces:**
- Consumes: nothing
- Produces: a working `venv/` with streamlit, pandas, plotly, and pytest installed; `app.py` that renders the title.

- [ ] **Step 1: Move TASK-1 to In Progress in `TASKS.md`** (see Milestone bookkeeping).

- [ ] **Step 2: Create `requirements.txt`**

```text
streamlit>=1.50
pandas>=2.2
plotly>=6.0
pytest>=8.0
```

- [ ] **Step 3: Create the virtual environment and install dependencies**

Run:
```bash
python -m venv venv
venv/Scripts/python -m pip install --upgrade pip
venv/Scripts/python -m pip install -r requirements.txt
```
Expected: the final line starts with `Successfully installed`, and the list includes `streamlit`, `pandas`, `plotly`, and `pytest`.

- [ ] **Step 4: Create `app.py`**

```python
"""ShopSmart Sales Dashboard.

A one-page Streamlit app showing 2024 sales KPIs and charts
(see prd/ecommerce-analytics.md). All calculations live in data.py.
"""
import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")
```

- [ ] **Step 5: Check the app runs and shows the title**

Run:
```bash
venv/Scripts/python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py', default_timeout=30).run(); assert not at.exception, at.exception; print(at.title[0].value)"
```
Expected output: `ShopSmart Sales Dashboard`

Then confirm the real server starts. Run `venv/Scripts/streamlit run app.py --server.headless true` in the background, then run `curl -s http://localhost:8501/_stcore/health`. Expected: `ok`. Stop the server afterwards.

- [ ] **Step 6: Commit**

```bash
git add requirements.txt app.py TASKS.md
git commit -m "TASK-1: Add requirements and Streamlit app skeleton"
```

- [ ] **Step 7: Mark TASK-1 done in `TASKS.md` and commit** (see Milestone bookkeeping; the hash is Step 6's commit).

---

### P2 [TASK-2]: CSV loader with required-column check (TDD)

**Files:**
- Create: `pytest.ini`
- Create: `tests/test_data.py`
- Create: `data.py`
- Modify: `TASKS.md` (TASK-2 → In Progress)

**Interfaces:**
- Consumes: nothing
- Produces:
  - `data.REQUIRED_COLUMNS: list[str]`
  - `data.load_sales_data(path) -> pd.DataFrame`, with column `date` as datetime64. Raises `ValueError("Missing columns: a, b")` when required columns are absent, and `FileNotFoundError` when the file doesn't exist (pandas' own error).
  - Test fixture `sales` in `tests/test_data.py`, which later tasks reuse.

- [ ] **Step 1: Move TASK-2 to In Progress in `TASKS.md`.**

- [ ] **Step 2: Create `pytest.ini`**

```ini
[pytest]
testpaths = tests
pythonpath = .
```

- [ ] **Step 3: Write the failing tests in `tests/test_data.py`**

```python
"""Tests for data.py, checked against the real sales CSV."""
from pathlib import Path

import pandas as pd
import pytest

from data import load_sales_data

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
```

- [ ] **Step 4: Run the tests and watch them fail**

Run: `venv/Scripts/python -m pytest -v`
Expected: collection ERROR with `ImportError: cannot import name 'load_sales_data' from 'data' (unknown location)`.

- [ ] **Step 5: Write `data.py`**

```python
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
```

- [ ] **Step 6: Run the tests and watch them pass**

Run: `venv/Scripts/python -m pytest -v`
Expected: `3 passed`

- [ ] **Step 7: Commit**

```bash
git add pytest.ini tests/test_data.py data.py TASKS.md
git commit -m "TASK-2: Add CSV loader with required-column check"
```

---

### P3 [TASK-2]: Load data in the app, with placeholder sections

**Files:**
- Modify: `app.py` (full replacement below)
- Modify: `TASKS.md` (TASK-2 → Done)

**Interfaces:**
- Consumes: `data.load_sales_data(path)` from P2
- Produces: in `app.py`, the variable `sales` (the loaded DataFrame), plus the layout names `kpi_left`, `kpi_right`, `category_col`, `region_col` used by P5, P7, and P9.

- [ ] **Step 1: Replace `app.py` with**

```python
"""ShopSmart Sales Dashboard.

A one-page Streamlit app showing 2024 sales KPIs and charts
(see prd/ecommerce-analytics.md). All calculations live in data.py.
"""
from pathlib import Path

import streamlit as st

from data import load_sales_data

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
kpi_left.caption("Total Sales: coming soon")
kpi_right.caption("Total Orders: coming soon")

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
```

- [ ] **Step 2: Check the page loads the data and shows all sections**

Run:
```bash
venv/Scripts/python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py', default_timeout=30).run(); assert not at.exception, at.exception; assert not at.error, at.error; print([s.value for s in at.subheader])"
```
Expected output: `['Sales Trend Over Time', 'Sales by Category', 'Sales by Region']`

- [ ] **Step 3: Check the error message path**

Run:
```bash
git mv data/sales-data.csv data/sales-data.tmp
venv/Scripts/python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py', default_timeout=30).run(); print(at.error[0].value)"
git mv data/sales-data.tmp data/sales-data.csv
```
Expected output starts with: `Could not load sales data:` and mentions `sales-data.csv`. Then run `git status --short`; expected: no change shown for `data/`.

- [ ] **Step 4: Run all tests**

Run: `venv/Scripts/python -m pytest -v`
Expected: `3 passed`

- [ ] **Step 5: Commit**

```bash
git add app.py
git commit -m "TASK-2: Load sales data in app with placeholder sections"
```

- [ ] **Step 6: Mark TASK-2 done in `TASKS.md` and commit** (hash = Step 5's commit).

---

### P4 [TASK-3]: KPI calculations (TDD)

**Files:**
- Modify: `tests/test_data.py`
- Modify: `data.py`
- Modify: `TASKS.md` (TASK-3 → In Progress)

**Interfaces:**
- Consumes: `load_sales_data`, fixture `sales`
- Produces: `data.total_sales(df) -> float`, `data.total_orders(df) -> int` (number of unique `order_id` values)

- [ ] **Step 1: Move TASK-3 to In Progress in `TASKS.md`.**

- [ ] **Step 2: Add failing tests.** In `tests/test_data.py`, replace the line `from data import load_sales_data` with:

```python
from data import load_sales_data, total_orders, total_sales
```

and add at the end of the file:

```python
def test_total_sales_matches_csv(sales):
    assert total_sales(sales) == pytest.approx(116500.21)


def test_total_orders_matches_csv(sales):
    assert total_orders(sales) == 482


def test_total_orders_counts_each_order_once():
    # An order spread over two rows still counts as one order.
    df = pd.DataFrame({"order_id": ["ORD-1", "ORD-1", "ORD-2"]})
    assert total_orders(df) == 2
```

- [ ] **Step 3: Run the tests and watch them fail**

Run: `venv/Scripts/python -m pytest -v`
Expected: collection ERROR with `ImportError: cannot import name 'total_orders' from 'data'`.

- [ ] **Step 4: Add to the end of `data.py`**

```python


def total_sales(df):
    """Sum of every order's total, in dollars."""
    return float(df["total_amount"].sum())


def total_orders(df):
    """Number of distinct orders (unique order IDs, not rows)."""
    return int(df["order_id"].nunique())
```

- [ ] **Step 5: Run the tests and watch them pass**

Run: `venv/Scripts/python -m pytest -v`
Expected: `6 passed`

- [ ] **Step 6: Commit**

```bash
git add tests/test_data.py data.py TASKS.md
git commit -m "TASK-3: Add total sales and total orders calculations"
```

---

### P5 [TASK-3]: KPI cards

**Files:**
- Modify: `app.py`
- Modify: `TASKS.md` (TASK-3 → Done)

**Interfaces:**
- Consumes: `total_sales(df)`, `total_orders(df)` from P4; `sales`, `kpi_left`, `kpi_right` in `app.py` from P3
- Produces: two `st.metric` cards

- [ ] **Step 1: Update the import in `app.py`.** Replace `from data import load_sales_data` with:

```python
from data import load_sales_data, total_orders, total_sales
```

- [ ] **Step 2: Replace the KPI placeholders.** Replace these two lines:

```python
kpi_left.caption("Total Sales: coming soon")
kpi_right.caption("Total Orders: coming soon")
```

with:

```python
kpi_left.metric("Total Sales", f"${total_sales(sales):,.0f}")
kpi_right.metric("Total Orders", f"{total_orders(sales):,}")
```

- [ ] **Step 3: Check the cards show the right values**

Run:
```bash
venv/Scripts/python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py', default_timeout=30).run(); assert not at.exception, at.exception; print([(m.label, m.value) for m in at.metric])"
```
Expected output: `[('Total Sales', '$116,500'), ('Total Orders', '482')]`

- [ ] **Step 4: Run all tests**

Run: `venv/Scripts/python -m pytest -v`
Expected: `6 passed`

- [ ] **Step 5: Commit**

```bash
git add app.py
git commit -m "TASK-3: Add Total Sales and Total Orders KPI cards"
```

- [ ] **Step 6: Mark TASK-3 done in `TASKS.md` and commit** (hash = Step 5's commit).

---

### P6 [TASK-4]: Monthly sales calculation (TDD)

**Files:**
- Modify: `tests/test_data.py`
- Modify: `data.py`
- Modify: `TASKS.md` (TASK-4 → In Progress)

**Interfaces:**
- Consumes: `load_sales_data`, fixture `sales`
- Produces: `data.sales_by_month(df) -> pd.DataFrame` with columns `["month", "sales"]`. `month` is a datetime (the first day of each month); rows are in chronological order, one per month.

- [ ] **Step 1: Move TASK-4 to In Progress in `TASKS.md`.**

- [ ] **Step 2: Add failing tests.** In `tests/test_data.py`, replace the `from data import ...` line with:

```python
from data import load_sales_data, sales_by_month, total_orders, total_sales
```

and add at the end of the file:

```python
def test_sales_by_month_has_one_row_per_month_in_order(sales):
    monthly = sales_by_month(sales)
    assert list(monthly.columns) == ["month", "sales"]
    assert len(monthly) == 12
    assert monthly["month"].is_monotonic_increasing
    assert monthly["month"].iloc[0] == pd.Timestamp("2024-01-01")


def test_sales_by_month_adds_up_to_total_sales(sales):
    assert sales_by_month(sales)["sales"].sum() == pytest.approx(116500.21)
```

- [ ] **Step 3: Run the tests and watch them fail**

Run: `venv/Scripts/python -m pytest -v`
Expected: collection ERROR with `ImportError: cannot import name 'sales_by_month' from 'data'`.

- [ ] **Step 4: Add to the end of `data.py`**

```python


def sales_by_month(df):
    """Total sales per calendar month, in date order.

    "MS" groups by month start, so each month is labeled with its first day.
    """
    monthly = df.resample("MS", on="date")["total_amount"].sum()
    return monthly.reset_index().rename(columns={"date": "month", "total_amount": "sales"})
```

- [ ] **Step 5: Run the tests and watch them pass**

Run: `venv/Scripts/python -m pytest -v`
Expected: `8 passed`

- [ ] **Step 6: Commit**

```bash
git add tests/test_data.py data.py TASKS.md
git commit -m "TASK-4: Add monthly sales calculation"
```

---

### P7 [TASK-4]: Sales trend line chart

**Files:**
- Modify: `app.py`
- Modify: `TASKS.md` (TASK-4 → Done)

**Interfaces:**
- Consumes: `sales_by_month(df)` from P6; `sales` in `app.py`
- Produces: a full-width Plotly line chart under "Sales Trend Over Time"

- [ ] **Step 1: Update the imports in `app.py`.** Replace:

```python
import streamlit as st

from data import load_sales_data, total_orders, total_sales
```

with:

```python
import plotly.express as px
import streamlit as st

from data import load_sales_data, sales_by_month, total_orders, total_sales
```

- [ ] **Step 2: Replace the trend placeholder.** Replace:

```python
st.subheader("Sales Trend Over Time")
st.caption("Chart coming soon")
```

with:

```python
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
```

- [ ] **Step 3: Check the page renders the chart with no errors or warnings**

Run:
```bash
venv/Scripts/python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py', default_timeout=30).run(); assert not at.exception, at.exception; assert not at.warning, at.warning; print(len(at.get('plotly_chart')))"
```
Expected output: `1`

If this fails with `TypeError` mentioning `width`, the installed Streamlit is too old. Run `venv/Scripts/python -m pip install -U -r requirements.txt` and retry. Do not switch to `use_container_width`.

- [ ] **Step 4: Run all tests**

Run: `venv/Scripts/python -m pytest -v`
Expected: `8 passed`

- [ ] **Step 5: Commit**

```bash
git add app.py
git commit -m "TASK-4: Add monthly sales trend chart"
```

- [ ] **Step 6: Mark TASK-4 done in `TASKS.md` and commit** (hash = Step 5's commit).

---

### P8 [TASK-5]: Category and region calculations (TDD)

**Files:**
- Modify: `tests/test_data.py`
- Modify: `data.py`
- Modify: `TASKS.md` (TASK-5 → In Progress)

**Interfaces:**
- Consumes: `load_sales_data`, fixture `sales`
- Produces:
  - `data.sales_by_category(df) -> pd.DataFrame` with columns `["category", "sales"]`, sorted highest to lowest
  - `data.sales_by_region(df) -> pd.DataFrame` with columns `["region", "sales"]`, sorted highest to lowest

- [ ] **Step 1: Move TASK-5 to In Progress in `TASKS.md`.**

- [ ] **Step 2: Add failing tests.** In `tests/test_data.py`, replace the `from data import ...` line with:

```python
from data import (
    load_sales_data,
    sales_by_category,
    sales_by_month,
    sales_by_region,
    total_orders,
    total_sales,
)
```

and add at the end of the file:

```python
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
```

- [ ] **Step 3: Run the tests and watch them fail**

Run: `venv/Scripts/python -m pytest -v`
Expected: collection ERROR with `ImportError: cannot import name 'sales_by_category' from 'data'`.

- [ ] **Step 4: Add to the end of `data.py`**

```python


def _sales_by(df, column):
    """Total sales for each value in `column`, highest first."""
    totals = df.groupby(column)["total_amount"].sum().sort_values(ascending=False)
    return totals.reset_index().rename(columns={"total_amount": "sales"})


def sales_by_category(df):
    """Total sales per product category, highest first."""
    return _sales_by(df, "category")


def sales_by_region(df):
    """Total sales per region, highest first."""
    return _sales_by(df, "region")
```

- [ ] **Step 5: Run the tests and watch them pass**

Run: `venv/Scripts/python -m pytest -v`
Expected: `12 passed`

- [ ] **Step 6: Commit**

```bash
git add tests/test_data.py data.py TASKS.md
git commit -m "TASK-5: Add sales by category and region calculations"
```

---

### P9 [TASK-5]: Category and region bar charts

**Files:**
- Modify: `app.py` (full replacement below; this is the finished file)
- Modify: `TASKS.md` (TASK-5 → Done)

**Interfaces:**
- Consumes: `sales_by_category(df)`, `sales_by_region(df)` from P8; everything from P3, P5, and P7
- Produces: the complete dashboard

- [ ] **Step 1: Replace `app.py` with the finished version**

```python
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
```

- [ ] **Step 2: Check all three charts render with no errors or warnings**

Run:
```bash
venv/Scripts/python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py', default_timeout=30).run(); assert not at.exception, at.exception; assert not at.warning, at.warning; print(len(at.get('plotly_chart')), [m.value for m in at.metric])"
```
Expected output: `3 ['$116,500', '482']`

- [ ] **Step 3: Run all tests**

Run: `venv/Scripts/python -m pytest -v`
Expected: `12 passed`

- [ ] **Step 4: Commit**

```bash
git add app.py
git commit -m "TASK-5: Add sales by category and region bar charts"
```

- [ ] **Step 5: Mark TASK-5 done in `TASKS.md` and commit** (hash = Step 4's commit).

---

### P10 [TASK-6]: Verification and refinement

**Files:**
- Modify only if a check below fails: `app.py`, `data.py`
- Modify: `TASKS.md` (TASK-6 → In Progress → Done)

**Interfaces:**
- Consumes: the finished app from P9
- Produces: a verified, reviewed dashboard ready to merge

- [ ] **Step 1: Move TASK-6 to In Progress in `TASKS.md` and commit**

```bash
git add TASKS.md
git commit -m "TASK-6: Start verification"
```

- [ ] **Step 2: Run the full test suite**

Run: `venv/Scripts/python -m pytest -v`
Expected: `12 passed`, 0 failed, and no warnings summary.

- [ ] **Step 3: Cross-check the dashboard against an independent calculation**

Run:
```bash
venv/Scripts/python -c "
import csv, collections
rows = list(csv.DictReader(open('data/sales-data.csv')))
total = sum(float(r['total_amount']) for r in rows)
print('total', format(total, ',.0f'), 'orders', len({r['order_id'] for r in rows}))
for key in ['category', 'region']:
    totals = collections.Counter()
    for r in rows:
        totals[r[key]] += float(r['total_amount'])
    print(key, [name for name, _ in totals.most_common()])
"
```
Expected output:
```
total 116,500 orders 482
category ['Electronics', 'Wearables', 'Audio', 'Smart Home', 'Accessories']
region ['North', 'West', 'East', 'South']
```
These must match the KPI cards (P9 Step 2) and the bar order in the category and region tests.

- [ ] **Step 4: Check load time and warnings on the real server**

Run `venv/Scripts/streamlit run app.py --server.headless true` in the background, sending its output to a log file in the scratchpad directory. Wait until `curl -s http://localhost:8501/_stcore/health` returns `ok`.

Then time a full render with:
```bash
venv/Scripts/python -c "import time; from streamlit.testing.v1 import AppTest; t = time.perf_counter(); AppTest.from_file('app.py', default_timeout=10).run(); print(f'{time.perf_counter() - t:.2f}s')"
```
Expected: well under `5.00s`.

Search the server log for `Warning`, `Deprecat`, `Error`, and `Traceback`. Expected: no matches. Leave the server running for Step 5.

- [ ] **Step 5: Ask the user to review the page in the browser**

Ask the user to open `http://localhost:8501` and confirm:
- title, KPI cards `$116,500` and `482`
- the trend line runs Jan–Dec 2024
- the category bars run Electronics → Accessories and the region bars run North → South, top to bottom
- hovering shows exact dollar values with cents
- the look is suitable for an executive presentation

**Wait for the user's answer.** If they ask for changes, make them in `app.py`, re-run Steps 2–4, and commit each fix as `TASK-6: <what changed>`. Stop the server when the review is finished.

- [ ] **Step 6: Readability pass**

Read `data.py` and `app.py` top to bottom and confirm:
- every function has a docstring
- `data.py` has no `import streamlit`
- `app.py` has no pandas calculations (no `.sum()`, `.groupby(`, `.resample(`, or `.nunique()`)
- there's no leftover `coming soon` text or unused imports

Check with: `grep -nE "streamlit|coming soon" data.py; grep -nE "\.sum\(|groupby\(|resample\(|nunique\(|coming soon" app.py`
Expected: no output. If anything turns up, fix it, re-run Step 2, and commit as `TASK-6: Tidy code`.

- [ ] **Step 7: Mark TASK-6 done in `TASKS.md` and commit.** For the hash, use the last `TASK-6:` commit that changed code. If Steps 1–6 changed no code, use Step 1's commit.

---

### P11 [TASK-7]: Merge `feature/sales-dashboard` into `main`

**Files:** none changed; this is a git operation.

**Interfaces:**
- Consumes: the verified branch from P10
- Produces: `main` on GitHub containing the finished dashboard, ready for the user to deploy

- [ ] **Step 1: Confirm the branch is clean and green**

Run: `git status --short --branch` (expected: `## feature/sales-dashboard`, with no changes listed), then `venv/Scripts/python -m pytest -q` (expected: `12 passed`).

- [ ] **Step 2: Get the user's explicit go-ahead to merge and push.** Merging and pushing change `main` on GitHub, and GitHub is what Streamlit Cloud will deploy from. **Do not continue without a clear yes.** If the user prefers a pull request or wants to merge it themselves, do that instead and skip to P12.

- [ ] **Step 3: Merge and push**

```bash
git switch main
git pull --ff-only origin main
git merge --no-ff feature/sales-dashboard -m "Merge feature/sales-dashboard: ShopSmart sales dashboard (TASK-1 to TASK-6)"
git push origin main
```
Expected: the merge finishes with no conflicts, and the push succeeds.

- [ ] **Step 4: Move TASK-7 to In Progress in `TASKS.md` on `main`, then commit and push**

```bash
git add TASKS.md
git commit -m "TASK-7: Start deployment"
git push origin main
```

- [ ] **Step 5: Stop and hand off to the user.** Tell them `main` is ready to deploy and point them to P12. **Claude's part of the plan ends here.**

---

### P12 [TASK-7]: Deploy to Streamlit Community Cloud — 👤 USER EXECUTES

> **This step belongs to the user. Claude does not do it.** Claude may answer questions if asked.

- [ ] **Step 1:** Go to https://share.streamlit.io and sign in with GitHub.
- [ ] **Step 2:** Click **Create app**, choose "Deploy a public app from GitHub", and set:
  - Repository: this repo
  - Branch: `main`
  - Main file path: `app.py`
  - Advanced settings → Python version: the newest offered that is 3.11 or later
- [ ] **Step 3:** Click **Deploy** and wait for the build. Streamlit Cloud installs packages from `requirements.txt`.
- [ ] **Step 4:** Open the public URL. Check the KPI cards (`$116,500`, `482`) and the three charts match what you saw locally.
- [ ] **Step 5:** Add the public URL to `README.md`. In `TASKS.md`, tick TASK-7's checkboxes, set its `Commit:` line to the merge commit's short hash (from `git log --merges -1 --format=%h`), and move it to Done. Then commit and push:

```bash
git add README.md TASKS.md
git commit -m "TASK-7: Deploy to Streamlit Community Cloud"
git push origin main
```

**End of plan.**
