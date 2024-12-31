import pandas as pd
import numpy as np

sales = pd.read_csv('sales_modified5.csv')

delivery_counts = sales['Driver_id'].value_counts().sort_index()

missing_count = sales['Driver_id'].isnull().sum()
print("Number of missing Driver_id values:", missing_count)

print("Drivers assigned for each day with at least 3 different drivers per day.")
print("\nDelivery counts for all drivers:")
print(delivery_counts)