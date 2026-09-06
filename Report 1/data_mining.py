import pandas as pd
import pip

#load the dataset
orders = pd.read_csv('Olist-20260815T061119Z-1-001/Olist/olist_orders_dataset.csv')

# Convert the column to datetime format
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

# Inspect the timestamps
print(orders[['order_purchase_timestamp']].head())
# double square brackets are used to select a single column and return it as a DataFrame rather than a Series. This is useful when you want to maintain the DataFrame structure for further operations or when you want to select multiple columns.

# Extract date only (YYYY-MM-DD) from the timestamp
orders['order_purchase_date'] = orders['order_purchase_timestamp'].dt.date

# Extract hour of day (0 to 23)
orders['order_purchase_hour'] = orders['order_purchase_timestamp'].dt.hour

# Extract day of week (Monday=0, Sunday=6)
orders['order_purchase_DOW'] = orders['order_purchase_timestamp'].dt.dayofweek

print(orders[['order_purchase_date', 'order_purchase_hour', 'order_purchase_DOW']].head())

# Convert delivery date to datetime
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])

print(orders[['order_delivered_customer_date']].head())

# Calculate actual lead time in days (floating point)
# The difference between the delivery date and the purchase timestamp is calculated in seconds, and then converted to days by dividing by the number of seconds in a day (24 hours * 3600 seconds).
orders['actual_lead_time_days'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.total_seconds() / (24 * 3600)

print(orders[['actual_lead_time_days']].head())

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Provide the data (full sample table from initial prompt context)
data = [
    ['e481f51cbdc54678b7cc49136f2d6af7', 'delivered', '2017-10-02 10:56:33', '2017-10-02 11:07:15', '2017-10-04 19:55:00', '2017-10-10 21:25:13', '2017-10-18 00:00:00'],
    ['53cdb2fc8bc7dce0b6741e2150273451', 'delivered', '2018-07-24 20:41:37', '2018-07-26 03:24:27', '2018-07-26 14:31:00', '2018-08-07 15:27:45', '2018-08-13 00:00:00'],
    ['47770eb9100c2d0c44946d9cf07ec65d', 'delivered', '2018-08-08 08:38:49', '2018-08-08 08:55:23', '2018-08-08 13:50:00', '2018-08-17 18:06:29', '2018-09-04 00:00:00'],
    ['949d5b44dbf5de918fe9c16f97b45f8a', 'delivered', '2017-11-18 19:28:06', '2017-11-18 19:45:59', '2017-11-22 13:39:59', '2017-12-02 00:28:42', '2017-12-15 00:00:00'],
    ['ad21c59c0840e6cb83a9ceb5573f8159', 'delivered', '2018-02-13 21:18:39', '2018-02-13 22:20:29', '2018-02-14 19:46:34', '2018-02-16 18:17:02', '2018-02-26 00:00:00']
]
columns = ['order_id', 'order_status', 'order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']
orders = pd.DataFrame(data, columns=columns)

# 2. Clean and convert relevant columns to datetime
date_cols = ['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']
for col in date_cols:
    orders[col] = pd.to_datetime(orders[col])

# 3. Calculate distinct Lead Times (in days)
# Series 1: Actual Lead Time (Start: purchase, End: delivered)
orders['actual_lead_time_days'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.total_seconds() / (24 * 3600)
# Series 2: Platform Promised Lead Time (Start: purchase, End: estimated)
# This is the lead time the platform committed to at the time of purchase.
orders['platform_promised_lead_time_days'] = (orders['order_estimated_delivery_date'] - orders['order_purchase_timestamp']).dt.total_seconds() / (24 * 3600)

# 4. Filter for only delivered orders that have complete data
# (All orders in the sample table are 'delivered' and have complete timestamps).
orders_filtered = orders[orders['order_status'] == 'delivered'].copy()
    
# 5. Prepare Plot (Dual-Series Line Chart)
fig, ax = plt.subplots(figsize=(10, 6))

# X-axis index for distinct orders
x_indices = range(len(orders_filtered))
    
# Plot Actual Lead Time
ax.plot(x_indices, orders_filtered['actual_lead_time_days'], marker='o', label='Actual Lead Time (Start: Purchase, End: Delivered)', color='#1f77b4', linestyle='-', linewidth=2)
    
# Plot Platform Promised Lead Time (using dashed line for contrast)
ax.plot(x_indices, orders_filtered['platform_promised_lead_time_days'], marker='s', label='Platform Promised Lead Time (Start: Purchase, End: Estimated)', color='#ff7f0e', linestyle='--', linewidth=2)

# Styling and Labels
ax.set_title("Chart 1: Comparison of Actual vs. Platform Promised Lead Times (Days)\n(Measured from Order Purchase Timestamp)", fontsize=14, fontweight='bold')
ax.set_ylabel("Lead Time (Days)", fontsize=12)
ax.set_xlabel("Orders (Sequential from Sample Data)", fontsize=12)
ax.set_xticks(x_indices)
ax.set_xticklabels([f"Order {i+1}" for i in x_indices], rotation=45, ha='right')
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(title="Lead Time Type", loc='upper left', fontsize=10)

plt.tight_layout()
# The system handles saving and displaying the plot.
plt.show() 

# Prepare the specific output variables for the thought trace.
output_variable_actual_lead_times_days = orders_filtered['actual_lead_time_days'].tolist()
output_variable_promised_lead_times_days = orders_filtered['platform_promised_lead_time_days'].tolist()

print(f"Calculated Actual Lead Times (Days): {output_variable_actual_lead_times_days}")
print(f"Calculated Platform Promised Lead Times (Days): {output_variable_promised_lead_times_days}")

