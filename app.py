import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Online Retail Dashboard", layout="wide")

@st.cache_resource
def init_database():
    df = pd.read_excel('online_retail_II.xlsx')
    
    df['amount'] = df['Quantity'] * df['Price']
    
    conn = sqlite3.connect('retail_database.db', check_same_thread=False)
    df.to_sql('sales', conn, if_exists='replace', index=False)
    return conn

conn = init_database()

@st.cache_data
def load_dashboard_data():
    query_kpi = "SELECT SUM(amount) AS total FROM sales;"
    total_revenue = pd.read_sql_query(query_kpi, conn)['total'].iloc[0]
    
    query_trend = """
    SELECT 
        strftime('%Y-%m', InvoiceDate) AS Month,
        SUM(amount) AS TotalSales
    FROM sales
    GROUP BY Month
    ORDER BY Month ASC;
    """
    df_trend = pd.read_sql_query(query_trend, conn)
    
    query_top_products = """
    SELECT 
        Description,
        SUM(amount) AS TotalRevenue
    FROM sales
    WHERE Description IS NOT NULL
    GROUP BY Description
    ORDER BY TotalRevenue DESC
    LIMIT 5;
    """
    df_top_products = pd.read_sql_query(query_top_products, conn)
    
    return total_revenue, df_trend, df_top_products

total_revenue, df_trend, df_top_products = load_dashboard_data()


st.title("📊 Ultimate Online Sales Management Dashboard")
st.markdown("---")

st.metric(
    label="Total Revenue of Sales from Real Data", 
    value=f"${total_revenue:,.2f}"
)

st.markdown("### Visualizations")

col1, col2 = st.columns(2)

with col1:
    fig_trend = px.line(
        df_trend, x='Month', y='TotalSales', 
        title='Sale of Company Monthly', markers=True
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    fig_products = px.bar(
        df_top_products, x='TotalRevenue', y='Description', 
        orientation='h', title='5 Profitable Best-Selling Product',
        color='TotalRevenue', color_continuous_scale='Blues'
    )
    fig_products.update_layout(yaxis={'categoryorder':'total ascending'}) 
    st.plotly_chart(fig_products, use_container_width=True)
