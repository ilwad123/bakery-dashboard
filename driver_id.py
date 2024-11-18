import pandas as pd
import numpy as np

# Load data
driver = pd.read_csv("driver.csv")
sales = pd.read_csv('sales_modified4.csv')

# Ensure datetime is properly parsed
sales['datetime'] = pd.to_datetime(sales['datetime'])

# Unique driver IDs
available_driver_ids = driver['Driver_id'].unique()

# Number of drivers to assign per day
num_of_drivers_per_day = 3

# Create a dictionary to store driver pools for each date
driver_pools = {}

# Assign drivers in one loop through unique dates
for date in sales['datetime'].dt.date.unique():
    # Select a pool of drivers for the date if not already selected
    driver_pools[date] = np.random.choice(available_driver_ids, num_of_drivers_per_day, replace=False)

    # Get rows corresponding to the current date
    date_rows = sales[sales['datetime'].dt.date == date].index

    # Assign drivers from the pool
    sales.loc[date_rows, 'Driver_id'] = np.random.choice(driver_pools[date], size=len(date_rows), replace=True)

# Calculate delivery counts for each driver
delivery_counts = sales['Driver_id'].value_counts().sort_index()

# Save the updated sales data
sales.to_csv('sales_modified4.csv', index=False)

print("Drivers assigned for each day with at least 3 different drivers per day.")
print("\nDelivery counts for all drivers:")
print(delivery_counts)
