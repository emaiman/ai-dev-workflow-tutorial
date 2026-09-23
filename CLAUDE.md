# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A tutorial repo (see `README.md`) in which a student builds the **ShopSmart Sales Dashboard**: a one-page Streamlit app over `data/sales-data.csv`. The tutorial docs (`README.md`, `pre-work-setup.md`, `workshop-build-deploy.md`, `codex-companion.md`, `capstone-tools.md`) are course material, not app code. Leave them alone unless asked.

Requirements come from `prd/ecommerce-analytics.md` (**Phase 1 only**). Filters, date pickers, auth, export, alerts, drill-down, databases, and custom themes are Phase 2 and out of scope.

## Commands

Use the plain virtual environment in `venv/`. Don't use uv, conda, or Poetry. Paths below are for Windows; on macOS/Linux use `venv/bin/`.

```bash
venv/Scripts/python -m pip install -r requirements.txt    # install deps
venv/Scripts/python -m pytest -v                          # all tests (pytest.ini sets testpaths + pythonpath)
venv/Scripts/python -m pytest tests/test_data.py::test_total_sales_matches_csv   # one test
venv/Scripts/streamlit run app.py                         # run the app (http://localhost:8501)
```

Smoke-test the whole page without a browser (Streamlit's `AppTest`):

```bash
venv/Scripts/python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py', default_timeout=10).run(); print([(m.label, m.value) for m in at.metric], len(at.exception))"
```

A benign `missing ScriptRunContext` log line appears in bare `AppTest` runs. It is not an `st.warning`.

There is no linter or build step.

## Architecture

Two modules with a strict split:

- **`data.py`**: pandas only, and **must never import Streamlit**. It holds CSV loading (`load_sales_data` checks `REQUIRED_COLUMNS` and raises `ValueError` naming any that are missing, then parses `date`) and every calculation. It returns raw numbers and DataFrames with fixed column names: `sales_by_month` → `month`/`sales`; `sales_by_category`/`sales_by_region` → `category|region`/`sales`, already sorted highest first.
- **`app.py`**: display only. It does no pandas math (no `.sum()`, `groupby`, `resample`, `nunique` here). It loads through a `@st.cache_data` wrapper, catches `FileNotFoundError`/`ValueError` to show `st.error` + `st.stop()`, and does all number formatting at display time.

`tests/test_data.py` covers `data.py` only and runs against the **real CSV** through a `sales` fixture. There are no app/UI tests.

Display conventions the code and tests rely on:
- Page title is exactly `ShopSmart Sales Dashboard`.
- Total Sales `f"${value:,.0f}"` → `$116,500`; Total Orders `f"{value:,}"` → `482`. Orders count unique `order_id`s, not rows.
- Tooltips show exact dollars with cents (`$,.2f`); axis ticks use whole dollars (`$,.0f`).
- Bar charts are horizontal. `data.py` sorts highest first, so `app.py` reverses the y-axis (`autorange="reversed"`) to put the largest bar on top.
- Use `st.plotly_chart(fig, width="stretch")`. `use_container_width` is deprecated and prints a warning.

Reference values from the CSV, for checking any change: 482 rows / 482 orders, total $116,500.21, Jan–Dec 2024 (12 months). Category order: Electronics, Wearables, Audio, Smart Home, Accessories. Region order: North, West, East, South.

## Workflow conventions

- Work happens on `feature/sales-dashboard`. The plan says no git worktree and no extra branches.
- The design spec and implementation plan live in `docs/superpowers/specs/` and `docs/superpowers/plans/` (the 2026-09-22 files). The plan's tasks are numbered `P1`–`P12` and each is tagged with its milestone (`[TASK-N]`).
- **Every commit message starts with the milestone ID**, e.g. `TASK-3: Add KPI cards`.
- `TASKS.md` is the milestone board (To Do / In Progress / Done). When starting a milestone, move its block to In Progress and include that in the first commit. When finishing, check its criteria, set `Commit:` to the short hash of the milestone's last code commit (or its start commit if no code changed), add a `Notes:` line ("clean", or what went wrong or what the user changed), move it to Done, and commit that on its own as `TASK-N: Mark TASK-N done in TASKS.md`.
- `.superpowers/sdd/<plan>/progress.md` is the git-ignored execution ledger. Check it before resuming plan work, since tasks marked complete there are already committed.

## Environment gotchas (Windows)

- The Bash tool's shell lacks `which` and `uname`. `source venv/Scripts/activate` prints harmless errors about them. To confirm the venv is in use, check the running process's command line instead.

## Lessons

From the `Notes:` lines in `TASKS.md` (TASK-1 to TASK-5 were clean; these come from TASK-6):

- **Check for running Streamlit servers before starting one.** A server left over from an earlier session held 8501, the new one quietly moved to 8502, and the health check on 8501 passed against the wrong process. Before trusting any server check, confirm which process owns the port and that it's the one you started.
- **Stop the servers you start when the work is done.** Leftovers carry into later sessions and cause the problem above. Don't stop a server you didn't start without asking the user.
- **Check the server log only after a real page load.** Streamlit runs `app.py` only when a browser session connects, so a warning scan of a server nobody has opened proves nothing.
- **A verification-only milestone still gets a `Commit:` hash.** If no code changed, use the milestone's start commit and say so in `Notes:`, rather than borrowing an earlier milestone's code commit.
