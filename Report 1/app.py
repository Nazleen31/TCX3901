import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



# Page layout setup
st.set_page_config(page_title="Delivery Performance Dashboard", layout="wide")

st.title("🚚 Olist Logistics & Delivery Performance Dashboard")
st.markdown("Real-time operational monitoring for checkout lead times and lateness risks.")

# 1. Load Data
@st.cache_data
def load_data():
    orders = pd.read_csv('Olist-20260815T061119Z-1-001/Olist/olist_orders_dataset.csv')
    customers = pd.read_csv('Olist-20260815T061119Z-1-001/Olist/olist_customers_dataset.csv')
    df = pd.merge(orders, customers, on='customer_id', how='inner')
    
    # Clean datetime fields
    date_cols = ['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col])
        
    df = df[df['order_status'] == 'delivered'].dropna(subset=date_cols).copy()
    
    # Calculate Lead Times and Lateness
    df['actual_lead_time'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.total_seconds() / 86400.0
    df['promised_lead_time'] = (df['order_estimated_delivery_date'] - df['order_purchase_timestamp']).dt.total_seconds() / 86400.0
    df['is_late'] = (df['order_delivered_customer_date'] > df['order_estimated_delivery_date']).astype(int)
    return df

df = load_data()

# 2. Key Metrics Summary (KPI Cards)
st.subheader("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

total_orders = len(df)
late_orders = df['is_late'].sum()
late_pct = (late_orders / total_orders) * 100
avg_lead = df['actual_lead_time'].mean()

col1.metric("Total Delivered Orders", f"{total_orders:,}")
col2.metric("Late Deliveries", f"{late_orders:,}")
col3.metric("Late Order Rate", f"{late_pct:.2f}%")
col4.metric("Avg Actual Lead Time", f"{avg_lead:.1f} days")

st.divider()

# 3. Interactive State Filter
st.subheader("Geographic Delay Risk Explorer")
selected_states = st.multiselect("Filter by Customer State:", options=sorted(df['customer_state'].unique()), default=['SP', 'RJ', 'AM', 'PA'])

if selected_states:
    filtered_df = df[df['customer_state'].isin(selected_states)]
else:
    filtered_df = df

# 4. Chart View: State Late Rate Comparison
state_metrics = filtered_df.groupby('customer_state')['is_late'].mean().reset_index()
state_metrics['late_rate_pct'] = state_metrics['is_late'] * 100

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(state_metrics['customer_state'], state_metrics['late_rate_pct'], color='#0072BD')
ax.axhline(late_pct, color='#D9531E', linestyle='--', label=f'Overall Avg ({late_pct:.1f}%)')
ax.set_ylabel("Late Order Rate (%)")
ax.set_title("Lateness Rate by Customer State")
ax.legend()

st.pyplot(fig)