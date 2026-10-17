
import streamlit as st

st.set_page_config(
    page_title="Retail Dashboard",
    layout="wide",
    page_icon=":material/analytics:"
)

pg = st.navigation([
    st.Page("Overview.py", title="Overview", icon=":material/dashboard:"),
    st.Page("Sales_Insights.py", title="Sales Insights", icon=":material/insights:"),
    st.Page("Products.py", title="Products", icon=":material/inventory_2:"),
    st.Page("Risk_and_Team.py", title="Risk and Team", icon=":material/groups:")
])

pg.run()
