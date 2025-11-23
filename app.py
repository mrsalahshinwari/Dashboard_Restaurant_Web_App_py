import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# -------------------- Load Data --------------------
df = pd.read_excel('sale.xlsx')
df['date'] = pd.to_datetime(df['date'])

# -------------------- Page Config --------------------
st.set_page_config(page_title="Salah Fast Food Point", layout="wide", initial_sidebar_state="expanded")

# -------------------- Custom CSS --------------------
# -------------------- Remove Top Padding --------------------
st.markdown("""
<style>
/* Reduce top padding/margin */
.css-18e3th9 {
    padding-top: 0rem;
    padding-bottom: 0rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Background color */
body {
    background-color: #crimson;
}

/* Title */
h1 {
    font-size: 1.8rem !important;
    color: #2c3e50;
}

/* Subheaders */
h2, h3, h4 {
    font-size: 1.1rem !important;
    color: #34495e;
}

/* Sidebar */
.css-1d391kg {
    background-color: #ecf0f1;
}

/* Metrics font size */
[data-testid="stMetricValue"] {
    font-size: 1.5rem !important;
}
[data-testid="stMetricLabel"] {
    font-size: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------- Sidebar Filters --------------------
st.sidebar.header("Filters")
item_type = st.sidebar.multiselect("Select Item Type", df['item_type'].unique(), df['item_type'].unique())
transaction_type = st.sidebar.multiselect("Transaction Type", df['transaction_type'].unique(), df['transaction_type'].unique())
item_name = st.sidebar.multiselect("Select Item Name", df['item_name'].unique(), df['item_name'].unique())
received_by = st.sidebar.multiselect("Received By", df['received_by'].unique(), df['received_by'].unique())
time_of_sale = st.sidebar.multiselect("Time of Sale", df['time_of_sale'].unique(), df['time_of_sale'].unique())

# -------------------- Apply Filters --------------------
filtered_df = df[
    (df['item_type'].isin(item_type)) &
    (df['transaction_type'].isin(transaction_type)) &
    (df['item_name'].isin(item_name)) &
    (df['received_by'].isin(received_by)) &
    (df['time_of_sale'].isin(time_of_sale))
]

# -------------------- KPIs --------------------
st.title("📊 Salah Fast food point")
st.subheader("Dataset Overview")

total_sales = filtered_df['transaction_amount'].sum()
total_orders = len(filtered_df)
avg_order_value = filtered_df['transaction_amount'].mean()
total_quantity = filtered_df['quantity'].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"₹{total_sales:,.0f}")
col2.metric("Total Orders", total_orders)
col3.metric("Avg Order Value", f"₹{avg_order_value:,.2f}")
col4.metric("Total Quantity", total_quantity)

# -------------------- Charts in Grid Layout --------------------
st.subheader("Sales & Analytics")

# Row 1: Sales by Item & Sales by Category
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown("💰 **Sales by Item**")
    item_sales = filtered_df.groupby('item_name')['transaction_amount'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6,3))
    item_sales.plot(kind='bar', color="#e21717", ax=ax)
    ax.set_ylabel('Sales Amount')
    ax.set_xlabel('')
    ax.set_xticklabels(item_sales.index, rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

with row1_col2:
    st.markdown("🍔 **Sales by Category**")
    category_sales = filtered_df.groupby('item_type')['transaction_amount'].sum()
    fig, ax = plt.subplots(figsize=(6,3))
    colors = ['#FF9999','#66B2FF','#99FF99','#FFCC99']
    ax.pie(category_sales, labels=category_sales.index, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')
    st.pyplot(fig)

# Row 2: Transaction Type & Daily Sales Trend
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown("💳 **Transaction Type**")
    transaction_counts = filtered_df['transaction_type'].value_counts()
    fig, ax = plt.subplots(figsize=(6,3))
    transaction_counts.plot(kind='bar', color='#ff7f0e', ax=ax)
    ax.set_ylabel('Count')
    ax.set_xlabel('')
    ax.set_xticklabels(transaction_counts.index, rotation=0)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

with row2_col2:
    st.markdown("📈 **Daily Sales Trend**")
    daily_sales = filtered_df.groupby('date')['transaction_amount'].sum()
    fig, ax = plt.subplots(figsize=(6,3))
    daily_sales.plot(kind='line', marker='o', color='#2ca02c', ax=ax)
    ax.set_ylabel('Sales Amount')
    ax.set_xlabel('')
    ax.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)

# Row 3: Top 5 Items by Revenue & Top 5 Items by Quantity
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    st.markdown("🏆 **Top 5 Items by Revenue**")
    top5_revenue = filtered_df.groupby('item_name')['transaction_amount'].sum().sort_values(ascending=False).head(5)
    fig, ax = plt.subplots(figsize=(6,3))
    top5_revenue.plot(kind='bar', color='#d62728', ax=ax)
    ax.set_ylabel('Revenue')
    ax.set_xlabel('')
    ax.set_xticklabels(top5_revenue.index, rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

with row3_col2:
    st.markdown("📦 **Top 5 Items by Quantity Sold**")
    top5_quantity = filtered_df.groupby('item_name')['quantity'].sum().sort_values(ascending=False).head(5)
    fig, ax = plt.subplots(figsize=(6,3))
    top5_quantity.plot(kind='bar', color='#9467bd', ax=ax)
    ax.set_ylabel('Quantity')
    ax.set_xlabel('')
    ax.set_xticklabels(top5_quantity.index, rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

# Row 4: Staff Performance & Quantity by Category
row4_col1, row4_col2 = st.columns(2)

with row4_col1:
    st.markdown("👨‍🍳 **Staff Performance**")
    staff_sales = filtered_df.groupby('received_by')['transaction_amount'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6,3))
    staff_sales.plot(kind='bar', color='#17becf', ax=ax)
    ax.set_ylabel('Sales Amount')
    ax.set_xlabel('')
    ax.set_xticklabels(staff_sales.index, rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

with row4_col2:
    st.markdown("🍹 **Quantity by Item Type**")
    quantity_category = filtered_df.groupby('item_type')['quantity'].sum()
    fig, ax = plt.subplots(figsize=(6,3))
    quantity_category.plot(kind='bar', color='#bcbd22', ax=ax)
    ax.set_ylabel('Quantity')
    ax.set_xlabel('')
    ax.set_xticklabels(quantity_category.index, rotation=0)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

# Row 5: Correlation Heatmap
st.subheader("🔍 Correlation Heatmap")
corr = filtered_df[['item_price', 'quantity', 'transaction_amount']].corr()
fig, ax = plt.subplots(figsize=(6,3))
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)



