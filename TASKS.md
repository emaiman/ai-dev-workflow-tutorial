# TASKS

This file tracks all work for the ShopSmart Sales Dashboard (see `prd/ecommerce-analytics.md`).

## Definition of Done

A milestone moves to **Done** only when:

- All of its acceptance criteria are met
- The app runs locally with `streamlit run app.py`
- Changes are committed with the milestone ID in the commit message (e.g., `TASK-3: Add KPI cards`)

## To Do

### TASK-7: Deploy to Streamlit Community Cloud
Publish the dashboard to Streamlit Community Cloud with a shareable public URL (NFR-5).
- [ ] App is deployed and loads successfully at a public URL
- [ ] Public URL is recorded in the README

Commit:

## In Progress

## Done

### TASK-1: Environment setup and project initialization
Set up the Python environment, dependencies, and a minimal Streamlit app skeleton.
- [x] `requirements.txt` lists `streamlit`, `pandas`, and `plotly`
- [x] `app.py` exists and launches with `streamlit run app.py` showing the dashboard title

Commit: 4860c1b
Notes: clean

### TASK-2: Data loading and basic structure
Load `data/sales-data.csv` with Pandas and lay out the page structure for KPIs and charts.
- [x] CSV loads with `date` parsed as a date and numeric columns as numbers
- [x] Loaded data has 482 rows, 5 categories, and 4 regions
- [x] Page layout has placeholder sections for KPIs, trend chart, and breakdown charts

Commit: e7037cf
Notes: clean

### TASK-3: KPI cards
Display Total Sales and Total Orders prominently at the top of the dashboard (FR-1).
- [x] Total Sales shown as currency (`$X,XXX,XXX`), approximately $116,500
- [x] Total Orders shown with thousands separators, equal to 482

Commit: dab94dc
Notes: clean

### TASK-4: Sales trend chart
Add an interactive Plotly line chart of sales over time (FR-2).
- [x] Line chart shows sales by month (or day) across the 12-month range
- [x] Axes are labeled and tooltips show exact sales values

Commit: 4f1f25b
Notes: clean

### TASK-5: Category and region breakdowns
Add side-by-side bar charts for sales by category and by region (FR-3, FR-4).
- [x] Category chart shows all 5 categories sorted highest to lowest, with Electronics on top
- [x] Region chart shows all 4 regions sorted highest to lowest
- [x] Both charts have clear labels and tooltips with exact values

Commit: b569de2
Notes: clean

### TASK-6: Testing and refinement
Verify figures against the CSV and polish the dashboard for executive presentation.
- [x] KPI and chart values match independent calculations from the CSV
- [x] Dashboard runs with no errors or warnings and loads within 5 seconds
- [x] Code is commented and organized into clear functions (NFR-3)

Commit: 1e33538
Notes: No code changes needed (all checks passed), so Commit is the TASK-6 start commit. Claude's first server health check hit a leftover server from an earlier session on port 8501; caught, and the review and log scan were redone on a fresh server (8502). Leftover server later stopped.
