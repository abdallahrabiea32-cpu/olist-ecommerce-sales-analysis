# Retail Sales Analytics Dashboard

An interactive retail analytics project built with **Python, Pandas, Plotly, and Streamlit**. It explores transaction-level sales performance, profitability, product performance, sales channels, customer segments, delivery operations, and return-related risk.

The project includes a Jupyter Notebook for the analysis workflow and a multi-page Streamlit dashboard for exploring the cleaned data.

## Dashboard pages

- **Business Overview** — headline performance KPIs, monthly and yearly trends, category profitability, channel mix, and geographic performance.
- **Sales Insights** — yearly growth, monthly margin trends, category and channel comparisons, discount/profit association, and calendar-month patterns.
- **Product Analysis** — top and bottom products by profit, quantity versus margin, cumulative sales (Pareto-style) analysis, and ratings by category.
- **Risk and Team** — order-status mix, margin by discount band, loss-making transaction records, delivery time by shipping method, and sales representative performance.

## Project structure

```text
Project Olist E-commerce/
├── app.py                       # Streamlit entry point and page navigation
├── utils.py                     # Shared loading, filters, KPI calculations, chart styling
├── cleaned_data.csv             # Prepared dataset used by the dashboard
├── cleaned_data.parquet         # Prepared data in Parquet format
├── Database/
│   └── Sales_transactions_2022_2025.csv
├── pages/
│   ├── Overview.py
│   ├── Sales_Insights.py
│   ├── Products.py
│   └── Risk_and_Team.py
├── assets/
│   └── styles.css               # Existing brown/cream theme and subtle motion
├── .streamlit/
│   └── config.toml              # Streamlit theme settings
├── Retail_Project.ipynb         # Data cleaning and analysis notebook
├── Streamlit_Launcher.ipynb     # Optional notebook to launch the app locally
├── cleaning_notes.txt
├── requirements.txt
└── .gitignore
```

## Run locally

Use Python 3.10 or newer where possible.

### Option 1 — Terminal (recommended)

Open a terminal in the project root and run:

```bash
python -m venv .venv
```

Activate the environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Start the dashboard:

```bash
python -m streamlit run app.py
```

Open the local URL printed in the terminal, usually `http://localhost:8501`.

### Option 2 — Jupyter Notebook

Open `Streamlit_Launcher.ipynb` from the project root. Run the file-check cell, install dependencies if needed, and then run the final `streamlit run app.py` cell. Keep that cell running while using the dashboard.

## Analysis workflow

`Retail_Project.ipynb` contains data inspection, cleaning, feature engineering, exploratory analysis, and additional validation/business-analysis sections. The Streamlit dashboard reads the prepared `cleaned_data.csv` file.

The dashboard's data loading, common filters, reporting basis, KPI calculations, and chart styling are centralized in `utils.py` to reduce duplication across pages.

## KPI definitions and interpretation

- **Total Sales** and **Total Profit** are sums over the selected records.
- **Profit Margin** is total profit divided by total sales, multiplied by 100.
- **Units Sold** is the sum of the `Quantity` field.
- **Average Transaction Sales** is the mean `Sales_Amount` per row in the cleaned dataset.
- **Return Rate (status)** is the share of selected rows whose `Order_Status` is `Returned`.
- **Net basis** excludes records marked `Cancelled` or `Returned` from financial charts and KPIs. The Risk and Team page keeps the full selected status mix visible for context.

**Data limitation:** the cleaned dataset does not include `Order_ID`, so the dashboard cannot reliably calculate unique order counts or true average order value from this file. Transaction-level language is used instead. The dashboard is intended for exploratory and educational analysis; validate data definitions and currency assumptions before using results for real financial decisions.

## Dependencies

Main packages are listed in `requirements.txt`:

- Streamlit
- Pandas
- NumPy
- Plotly
- Statsmodels
- PyArrow

## Before publishing

- Run the dashboard and verify every page.
- Test filters and the net/gross reporting toggle.
- Confirm the analysis notebook runs from top to bottom in the intended environment.
- Do not commit `.venv/`, Python cache files, notebook checkpoints, or `.streamlit/secrets.toml`.
- Review dataset licensing and remove any personal or sensitive data before making the repository public.
