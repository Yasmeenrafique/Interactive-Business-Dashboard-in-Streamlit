import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Superstore Sales Analysis Dashboard")

# Load Data
@st.cache_data
def load_data():
    # Try Excel first, fallback to CSV if Excel not available
    try:
        df = pd.read_excel("data/train.xlsx")
    except FileNotFoundError:
        df = pd.read_csv("data/train.csv")
    
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
    df['Profit'] = pd.to_numeric(df.get('Profit', 0), errors='coerce')  # if Profit column exists
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
region = st.sidebar.multiselect("Select Region:", df['Region'].dropna().unique())
category = st.sidebar.multiselect("Select Category:", df['Category'].dropna().unique())
sub_category = st.sidebar.multiselect("Select Sub-Category:", df['Sub-Category'].dropna().unique())

# Apply filters
filtered_df = df.copy()
if region:
    filtered_df = filtered_df[filtered_df['Region'].isin(region)]
if category:
    filtered_df = filtered_df[filtered_df['Category'].isin(category)]
if sub_category:
    filtered_df = filtered_df[filtered_df['Sub-Category'].isin(sub_category)]

# KPI Metrics
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum() if "Profit" in filtered_df else 0
top_customers = filtered_df.groupby('Customer Name')['Sales'].sum().nlargest(5)

col1, col2 = st.columns(2)
col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")

# Top 5 Customers
st.subheader("🏆 Top 5 Customers by Sales")
st.table(top_customers)

# Sales by Category
fig1 = px.bar(filtered_df.groupby('Category')['Sales'].sum().reset_index(),
              x="Category", y="Sales", title="Sales by Category")
st.plotly_chart(fig1, use_container_width=True)

# Sales by Region
fig2 = px.bar(filtered_df.groupby('Region')['Sales'].sum().reset_index(),
              x="Region", y="Sales", title="Sales by Region")
st.plotly_chart(fig2, use_container_width=True)

# Sales Trend
fig3 = px.line(filtered_df.groupby('Order Date')['Sales'].sum().reset_index(),
               x="Order Date", y="Sales", title="Sales Over Time")
st.plotly_chart(fig3, use_container_width=True)

