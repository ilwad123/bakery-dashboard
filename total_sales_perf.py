import pandas as pd
from geopy.distance import geodesic
from numpy import random

# Load the transaction data
transactions = pd.read_csv('sales_modified5.csv')

bakery_location = (51.455084, -2.591765) 
transactions['datetime'] = pd.to_datetime(transactions['datetime'])
transactions['date'] = transactions['datetime'].dt.date
grouped = transactions.groupby(['Driver_id', 'date'])
total_sales = transactions.groupby('Driver_id')['total'].sum().reset_index()
performance_id = ["P0", "P1", "P2", "P3", "P4"]
total_sales['performance_id']=performance_id
total_sales.columns = ["Driver_id", "total_sales","performance_id"]
print(total_sales)

total_sales.to_csv('performance.csv', index=False)


