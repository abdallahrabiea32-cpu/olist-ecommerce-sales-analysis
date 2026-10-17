from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_DIR = Path(__file__).resolve().parent
DATA_PATH = PROJECT_DIR / "cleaned_data.csv"
STYLES_PATH = PROJECT_DIR / "assets" / "styles.css"

BROWN_CAFE_PALETTE = [
    "#5C4033",
    "#8B654A",
    "#B89A7A",
    "#DCC8AE",
    "#A47551",
    "#C4A484",
    "#6F5140",
    "#E8DCCB",
]


@st.cache_data(show_spinner="Loading retail transaction data...")
def load_data():
    """Load the cleaned dataset and prepare reusable date fields."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. "
            "Make sure cleaned_data.csv is included in the project folder."
        )

    df = pd.read_csv(DATA_PATH, parse_dates=["Order_Date"])

    required_columns = {
        "Order_Date", "Order_Year", "Country", "Product_Category",
        "Sales_Channel", "Order_Status", "Sales_Amount", "Profit",
        "Quantity", "Customer_ID", "Unit_Price", "Customer_Rating",
        "Delivery_Days", "Return_Flag",
    }
    missing = sorted(required_columns.difference(df.columns))
    if missing:
        raise ValueError(
            "The cleaned dataset is missing required columns: "
            + ", ".join(missing)
        )

    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    if "Month_Year" not in df.columns:
        df["Month_Year"] = df["Order_Date"].dt.to_period("M").dt.to_timestamp()
    else:
        df["Month_Year"] = pd.to_datetime(df["Order_Date"], errors="coerce").dt.to_period("M").dt.to_timestamp()

    if "month_name" not in df.columns:
        df["month_name"] = df["Order_Date"].dt.month_name()

    return df


def apply_shared_filters(df):
    """Render shared sidebar filters and return the filtered records."""
    st.sidebar.header("Filters")

    if df.empty:
        st.warning("The dataset contains no records to display.")
        st.stop()

    def pick(label, col):
        options = sorted(df[col].dropna().unique().tolist())
        key_suffix = col.lower()
        with st.sidebar.expander(label, expanded=False):
            select_all = st.checkbox(
                "Select all",
                value=True,
                key=f"all_{key_suffix}",
            )
            chosen = st.multiselect(
                label,
                options,
                default=options,
                key=f"ms_{key_suffix}",
                disabled=select_all,
                label_visibility="collapsed",
            )
        return options if select_all else chosen

    sel_years = pick("Year", "Order_Year")
    sel_country = pick("Country", "Country")
    sel_cat = pick("Category", "Product_Category")
    sel_channel = pick("Channel", "Sales_Channel")

    net_mode = st.sidebar.toggle(
        "Net basis (exclude Cancelled & Returned)",
        value=True,
        help=(
            "When enabled, financial KPIs and charts exclude records whose "
            "Order_Status is Cancelled or Returned. The Risk and Team page "
            "still shows the full selected order-status mix."
        ),
    )

    base = df[
        df["Order_Year"].isin(sel_years)
        & df["Country"].isin(sel_country)
        & df["Product_Category"].isin(sel_cat)
        & df["Sales_Channel"].isin(sel_channel)
    ].copy()

    if base.empty:
        st.warning("No records match the selected filters. Adjust the filters in the sidebar.")
        st.stop()

    return base, sel_years, net_mode


def apply_net_mode(df, net_mode):
    """Apply the selected gross/net reporting basis."""
    if not net_mode:
        return df.copy()

    result = df[~df["Order_Status"].isin(["Cancelled", "Returned"])].copy()
    if result.empty:
        st.warning(
            "The selected filters contain no records after excluding Cancelled "
            "and Returned statuses. Turn off the net-basis toggle or change filters."
        )
        st.stop()
    return result


def style(fig, height=400):
    """Apply the project's existing brown-and-cream visualization theme."""
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=50, b=10),
        legend_title=None,
        template="plotly_white",
        colorway=BROWN_CAFE_PALETTE,
        font=dict(size=13, color="#30251F", family="sans serif"),
        title_font=dict(size=16, color="#5C4033", family="sans serif"),
        paper_bgcolor="#F5F0E8",
        plot_bgcolor="#F5F0E8",
        title_x=0.0,
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="#E3D7C7",
        zeroline=False,
        linecolor="#C4A484",
        tickfont=dict(color="#5C4033"),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E3D7C7",
        zeroline=False,
        linecolor="#C4A484",
        tickfont=dict(color="#5C4033"),
    )
    return fig


def inject_styles():
    """Load local CSS using a path independent of the current working directory."""
    if STYLES_PATH.exists():
        st.markdown(
            f"<style>{STYLES_PATH.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


def page_header(title, description, base_df, net_mode):
    inject_styles()
    st.markdown(
        f"""
        <div class="page-header">
            <h1>{title}</h1>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    basis = (
        "Net basis: Cancelled and Returned records excluded from financial analysis"
        if net_mode
        else "Gross basis: all selected statuses included"
    )
    st.caption(f"Filtered records: {len(base_df):,} | {basis}")


def kpis(d):
    """Calculate dashboard KPIs safely for the selected records."""
    sales = d["Sales_Amount"].sum() if not d.empty else 0.0
    profit = d["Profit"].sum() if not d.empty else 0.0

    return {
        "sales": sales,
        "profit": profit,
        "margin": profit / sales * 100 if sales else 0.0,
        "units": d["Quantity"].sum() if not d.empty else 0.0,
        # The cleaned dataset has transaction rows but no Order_ID column.
        "avg_transaction_sales": d["Sales_Amount"].mean() if not d.empty else 0.0,
        "returns": (d["Order_Status"] == "Returned").mean() * 100 if not d.empty else 0.0,
        "rating": d["Customer_Rating"].mean() if not d.empty else 0.0,
        "delivery": d["Delivery_Days"].mean() if not d.empty else 0.0,
    }
