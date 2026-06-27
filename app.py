import pandas as pd
df = pd.read_excel('online_retail_II.xlsx')
missing_count = df.isnull().sum()
missing_percentage = (df.isnull().sum() / len(df)) * 100
missing_table = pd.DataFrame({
    'count of missing values' : missing_count , 
    'percentage of missing value' : missing_percentage
})
missing_table = missing_table[missing_table['count of missing values'] > 0].sort_values(by='percentage of missing value', ascending=False)

import sqlite3
import pandas as pd

df['amount'] = df['Quantity'] * df['Price']

conn = sqlite3.connect('retail_database.db')
df.to_sql('sales', conn, if_exists='replace', index=False)

# sales monthly based on region 
query = """SELECT 
    strftime('%Y-%m', InvoiceDate) AS month,
    Country,
    SUM(amount) AS total_sales
FROM sales
GROUP BY strftime('%Y-%m', InvoiceDate), Country
ORDER BY month ASC, total_sales DESC; """
mounthly_sales = pd.read_sql_query(query,conn)


# 5 TOP product
query = """SELECT 
    Description,
    SUM(Quantity) AS total_quantity
FROM sales
WHERE Description IS NOT NULL
GROUP BY Description
ORDER BY total_quantity DESC
LIMIT 5;"""
total_quantity = pd.read_sql_query(query,conn)


# 5 top profitable product
query = """SELECT 
    Description,
    SUM(amount) AS total_revenue
FROM sales
WHERE Description IS NOT NULL
GROUP BY Description
ORDER BY total_revenue DESC
LIMIT 5;"""
total_revenue = pd.read_sql_query(query,conn)

# top customers
query = """SELECT 
    `Customer ID`,
    SUM(amount) AS total_spent,
    COUNT(DISTINCT Invoice) AS total_orders
FROM sales
WHERE `Customer ID` IS NOT NULL
GROUP BY `Customer ID`
ORDER BY total_spent DESC
LIMIT 5;"""
top_customers = pd.read_sql_query(query,conn)

# status of sales in different hours 
query = """SELECT 
    strftime('%H:00', InvoiceDate) AS hour_of_day,
    COUNT(DISTINCT Invoice) AS number_of_invoices,
    SUM(amount) AS total_sales
FROM sales
GROUP BY strftime('%H', InvoiceDate)
ORDER BY total_sales DESC;"""
status_sales = pd.read_sql_query(query,conn)
conn.close()

import plotly.express as px
import panel as pn
pn.extension('plotly')
conn = sqlite3.connect('retail_database.db')
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

conn.close()

kpi_card = pn.indicators.Number(
    name='Total revenue of sales from real data', 
    value=total_revenue, 
    format='${value:,.2f}',
    font_size='26pt',
    title_size='12pt'
)

fig_trend = px.line(
    df_trend, x='Month', y='TotalSales', 
    title='sale of company monthly', markers=True
)
pane_trend = pn.pane.Plotly(fig_trend)

fig_products = px.bar(
    df_top_products, x='TotalRevenue', y='Description', 
    orientation='h', title='5 Profitable best-selling product',
    color='TotalRevenue', color_continuous_scale='Blues'
)
fig_products.update_layout(yaxis={'categoryorder':'total ascending'}) 
pane_products = pn.pane.Plotly(fig_products)

dashboard = pn.Column(
    pn.pane.Markdown("Ultimate online sales management dashboard", styles={'font-family': 'tahoma'}),
    kpi_card,
    pn.Spacer(height=15),
    pn.Row(pane_trend, pane_products) 
)
