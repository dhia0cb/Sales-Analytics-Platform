
import streamlit as st
import pandas as pd
import plotly.express as px

from src.database import load_sales_data


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Sales Analytics Platform",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def get_data():

    return load_sales_data()


st.title("Sales Analytics Platform")

st.markdown(
    "Interactive business intelligence dashboard "
    "for analyzing sales performance."
)

try:

    df = get_data()

except Exception as error:

    st.error(
        "Database not found. "
        "Run python prepare_data.py first."
    )

    st.exception(error)

    st.stop()


if df.empty:

    st.warning("No sales data available.")

    st.stop()


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("Dashboard Filters")

min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()

date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

regions = sorted(df["region"].unique())

selected_regions = st.sidebar.multiselect(
    "Select regions",
    regions,
    default=regions
)

categories = sorted(df["category"].unique())

selected_categories = st.sidebar.multiselect(
    "Select categories",
    categories,
    default=categories
)


# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------

if len(date_range) != 2:

    st.warning("Select both start and end dates.")

    st.stop()

start_date, end_date = date_range

filtered_df = df[
    (df["order_date"].dt.date >= start_date)
    & (df["order_date"].dt.date <= end_date)
    & (df["region"].isin(selected_regions))
    & (df["category"].isin(selected_categories))
].copy()


if filtered_df.empty:

    st.warning(
        "No records found for selected filters."
    )

    st.stop()


# --------------------------------------------------
# CALCULATE KPIs
# --------------------------------------------------

total_revenue = filtered_df["revenue"].sum()

total_profit = filtered_df["profit"].sum()

total_orders = filtered_df["order_id"].nunique()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)


# --------------------------------------------------
# DISPLAY KPI CARDS
# --------------------------------------------------

st.subheader("Business Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"${total_revenue:,.2f}"
)

col2.metric(
    "Total Profit",
    f"${total_profit:,.2f}"
)

col3.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col4.metric(
    "Average Order Value",
    f"${average_order_value:,.2f}"
)


st.divider()


# --------------------------------------------------
# MONTHLY SALES ANALYSIS
# --------------------------------------------------

st.subheader("Monthly Sales Performance")

monthly_sales = (
    filtered_df.groupby("order_month")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
)

fig_monthly = px.line(
    monthly_sales,
    x="order_month",
    y=["revenue", "profit"],
    markers=True,
    title="Monthly Revenue and Profit",
    labels={
        "order_month": "Month",
        "value": "Amount ($)",
        "variable": "Metric"
    }
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)


# --------------------------------------------------
# CATEGORY AND REGION ANALYSIS
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("Revenue by Category")

    category_sales = (
        filtered_df.groupby("category")["revenue"]
        .sum()
        .reset_index()
        .sort_values("revenue", ascending=False)
    )

    fig_category = px.bar(
        category_sales,
        x="category",
        y="revenue",
        color="category",
        title="Category Revenue"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


with col2:

    st.subheader("Revenue by Region")

    region_sales = (
        filtered_df.groupby("region")["revenue"]
        .sum()
        .reset_index()
        .sort_values("revenue", ascending=False)
    )

    fig_region = px.bar(
        region_sales,
        x="region",
        y="revenue",
        color="region",
        title="Regional Revenue"
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )


# --------------------------------------------------
# TOP PRODUCTS
# --------------------------------------------------

st.subheader("Top 10 Products")

top_products = (
    filtered_df.groupby("product")["revenue"]
    .sum()
    .reset_index()
    .sort_values("revenue", ascending=False)
    .head(10)
)

fig_products = px.bar(
    top_products,
    x="revenue",
    y="product",
    orientation="h",
    title="Top Products by Revenue"
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)


# --------------------------------------------------
# PAYMENT METHOD ANALYSIS
# --------------------------------------------------

st.subheader("Payment Method Distribution")

payment_sales = (
    filtered_df.groupby("payment_method")
    .size()
    .reset_index(name="orders")
)

fig_payment = px.pie(
    payment_sales,
    names="payment_method",
    values="orders",
    title="Orders by Payment Method"
)

st.plotly_chart(
    fig_payment,
    use_container_width=True
)


# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

st.divider()

st.subheader("Business Insights")

best_product = (
    filtered_df.groupby("product")["revenue"]
    .sum()
    .idxmax()
)

best_region = (
    filtered_df.groupby("region")["revenue"]
    .sum()
    .idxmax()
)

best_category = (
    filtered_df.groupby("category")["revenue"]
    .sum()
    .idxmax()
)

st.write(
    f"Best-performing product: **{best_product}**"
)

st.write(
    f"Best-performing region: **{best_region}**"
)

st.write(
    f"Best-performing category: **{best_category}**"
)


# --------------------------------------------------
# RAW DATA EXPLORER
# --------------------------------------------------

st.divider()

st.subheader("Sales Data Explorer")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# EXPORT DATA
# --------------------------------------------------

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download filtered sales data",
    data=csv_data,
    file_name="sales_report.csv",
    mime="text/csv"
)


st.caption(
    "Sales Analytics Platform | Built with Python, "
    "Pandas, SQLite and Streamlit"
)
