# TASKS

This file tracks all work for the ShopSmart Sales Dashboard (see `prd/ecommerce-analytics.md`).

## Definition of Done

A milestone moves to **Done** only when:

- All of its acceptance criteria are met
- The app runs locally with `streamlit run app.py`
- Changes are committed with the milestone ID in the commit message (e.g., `TASK-3: Add KPI cards`)

## To Do

### TASK-2: Data loading and basic structure
Load `data/sales-data.csv` with Pandas and lay out the page structure for KPIs and charts.
- [ ] CSV loads with `date` parsed as a date and numeric columns as numbers
- [ ] Loaded data has 482 rows, 5 categories, and 4 regions
- [ ] Page layout has placeholder sections for KPIs, trend chart, and breakdown charts

Commit:

### TASK-3: KPI cards
Display Total Sales and Total Orders prominently at the top of the dashboard (FR-1).
- [ ] Total Sales shown as currency (`$X,XXX,XXX`), approximately $116,500
- [ ] Total Orders shown with thousands separators, equal to 482

Commit:

### TASK-4: Sales trend chart
Add an interactive Plotly line chart of sales over time (FR-2).
- [ ] Line chart shows sales by month (or day) across the 12-month range
- [ ] Axes are labeled and tooltips show exact sales values

Commit:

### TASK-5: Category and region breakdowns
Add side-by-side bar charts for sales by category and by region (FR-3, FR-4).
- [ ] Category chart shows all 5 categories sorted highest to lowest, with Electronics on top
- [ ] Region chart shows all 4 regions sorted highest to lowest
- [ ] Both charts have clear labels and tooltips with exact values

Commit:

### TASK-6: Testing and refinement
Verify figures against the CSV and polish the dashboard for executive presentation.
- [ ] KPI and chart values match independent calculations from the CSV
- [ ] Dashboard runs with no errors or warnings and loads within 5 seconds
- [ ] Code is commented and organized into clear functions (NFR-3)

Commit:

### TASK-7: Deploy to Streamlit Community Cloud
Publish the dashboard to Streamlit Community Cloud with a shareable public URL (NFR-5).
- [ ] App is deployed and loads successfully at a public URL
- [ ] Public URL is recorded in the README

Commit:

## In Progress

### TASK-1: Environment setup and project initialization
Set up the Python environment, dependencies, and a minimal Streamlit app skeleton.
- [ ] `requirements.txt` lists `streamlit`, `pandas`, and `plotly`
- [ ] `app.py` exists and launches with `streamlit run app.py` showing the dashboard title

Commit:

## Done
