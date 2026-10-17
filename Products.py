
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data, apply_shared_filters, apply_net_mode, style, page_header

df_all = load_data()
base, sel_years, net_mode = apply_shared_filters(df_all)
df = apply_net_mode(base, net_mode)

page_header("Product Analysis", "Product profitability, sales volume, and Pareto analysis", base, net_mode)

p = df.groupby("Product_Name", as_index=False).agg(
    Sales=("Sales_Amount", "sum"),
    Profit=("Profit", "sum"),
    Quantity=("Quantity", "sum"),
    Avg_Discount=("Discount_Percentage", "mean")
)
p["Margin_%"] = p["Profit"].div(p["Sales"].where(p["Sales"].ne(0))) * 100

st.subheader(":material/monitoring: Product Portfolio")
with st.container(border=True):
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Products in Selection", f"{p['Product_Name'].nunique():,}")
    m2.metric("Product Sales", f"{p['Sales'].sum():,.0f}")
    m3.metric("Product Profit", f"{p['Profit'].sum():,.0f}")
    m4.metric(
        "Overall Product Margin",
        f"{(p['Profit'].sum() / p['Sales'].sum() * 100) if p['Sales'].sum() else 0:.1f}%"
    )

st.subheader(":material/star: Top & Bottom Performers")
c1, c2 = st.columns(2)

top = p.nlargest(10, "Profit").sort_values("Profit", ascending=True)
fig_top = px.bar(
    top, x="Profit", y="Product_Name", orientation="h",
    text_auto=".3s", title="Top 10 Products by Profit",
    color_discrete_sequence=["#8B654A"]
)
c1.plotly_chart(style(fig_top), width="stretch")

bot = p.nsmallest(10, "Profit").sort_values("Profit", ascending=False)
fig_bot = px.bar(
    bot, x="Profit", y="Product_Name", orientation="h",
    text_auto=".3s", title="Bottom 10 Products by Profit",
    color_discrete_sequence=["#B89A7A"]
)
c2.plotly_chart(style(fig_bot), width="stretch")

st.subheader(":material/bubble_chart: Quantity vs Margin")
prod = df.groupby(["Product_Name", "Product_Category"], as_index=False).agg(
    Quantity=("Quantity", "sum"),
    Sales=("Sales_Amount", "sum"),
    Profit=("Profit", "sum"),
    Avg_Discount=("Discount_Percentage", "mean")
)
prod["Margin_%"] = prod["Profit"].div(prod["Sales"].where(prod["Sales"].ne(0))) * 100

fig_bubble = px.scatter(
    prod,
    x="Quantity",
    y="Margin_%",
    size="Sales",
    color="Product_Category",
    hover_name="Product_Name",
    hover_data={"Avg_Discount": ":.1f", "Profit": ":,.0f", "Sales": ":,.0f"},
    size_max=55,
    title="Volume vs Profit Margin per Product (bubble = sales)",
    color_discrete_sequence=[
        "#5C4033", "#8B654A", "#B89A7A", "#DCC8AE",
        "#A47551", "#C4A484", "#6F5140", "#E8DCCB"
    ]
)
if not prod.empty:
    fig_bubble.add_hline(y=prod["Margin_%"].mean(), line_dash="dash", line_color="#8B654A")
    fig_bubble.add_vline(x=prod["Quantity"].mean(), line_dash="dash", line_color="#8B654A")
st.plotly_chart(style(fig_bubble, 600), width="stretch")

st.subheader(":material/pie_chart: Pareto Analysis (Cumulative Sales)")
p_sort = p.sort_values("Sales", ascending=False).reset_index(drop=True)
p_sort["Cumulative_Sales"] = p_sort["Sales"].cumsum()
sales_total = p_sort["Sales"].sum()
p_sort["Cumulative_Pct"] = (
    p_sort["Cumulative_Sales"] / sales_total * 100 if sales_total else 0
)
top = p_sort.head(50)

fig_pareto = go.Figure()
fig_pareto.add_trace(go.Bar(
    x=top["Product_Name"], y=top["Sales"], name="Sales",
    marker_color="#8B654A"
))
fig_pareto.add_trace(go.Scatter(
    x=top["Product_Name"], y=top["Cumulative_Pct"],
    name="Cumulative %", yaxis="y2",
    line=dict(color="#5C4033", width=2)
))
fig_pareto.update_layout(
    title=f"Pareto Chart of Top {len(top)} Products",
    xaxis=dict(type="category", tickangle=-45),
    yaxis=dict(title="Sales Amount"),
    yaxis2=dict(title="Cumulative %", overlaying="y", side="right", range=[0, 105]),
    showlegend=False
)
st.plotly_chart(style(fig_pareto), width="stretch")

st.subheader(":material/reviews: Average Rating by Category")
rating_cat = df.groupby("Product_Category", as_index=False).agg(
    Avg_Rating=("Customer_Rating", "mean")
).sort_values("Avg_Rating")

fig_rating = px.bar(
    rating_cat, x="Avg_Rating", y="Product_Category",
    orientation="h", text_auto=".2f",
    title="Average Rating by Category",
    color_discrete_sequence=["#A47551"]
)
st.plotly_chart(style(fig_rating), width="stretch")
