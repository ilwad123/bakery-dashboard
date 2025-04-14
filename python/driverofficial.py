import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('sales_modified4.csv')
data = pd.read_csv("driver.csv")

df['datetime'] = pd.to_datetime(df['datetime'])

time_threshold = pd.Timedelta(minutes=15)  
driver_per_day = 3  

# Unique driver IDs
driver_id = data['Driver_id'].unique()
df['Driver_id'] = None

# Group transactions by date
date = df.groupby(df['datetime'].dt.date)

# Process each date and its transactions
for date1, day_transactions in date:
    # Select 3 random drivers for the day
    driver_pool = np.random.choice(driver_id, driver_per_day, replace=False)
    assigned = {driver: None for driver in driver_pool} 
    # Initialise driver availability

    # Process each transaction
    for index, row in day_transactions.iterrows():
        time = row['datetime']
        place = row['place']
        available_driver = None

        # Check driver availability
        for driver in driver_pool:
            details = assigned.get(driver)
            if details is None or details['end-time'] <= time:
                available_driver = driver
                # Update driver's availability
                assigned[driver] = {'end-time': time + time_threshold, 'place': place}
                break

        # Fallback: Assign the first driver if none is available
        if available_driver is None:
            available_driver = driver_pool[0]
            assigned[available_driver] = {'end-time': time + time_threshold, 'place': place}

        # Assign driver to the transaction
        df.loc[index, 'Driver_id'] = available_driver

#orders the driver_ids
delivery_counts = df['Driver_id'].value_counts().sort_index()
#use of map to align with the correct driver_id
data['total_deliveries']=data['Driver_id'].map(delivery_counts)
print("Drivers assigned for each day with at least 3 different drivers per day.")
print("\nDelivery counts for all drivers:")
print(delivery_counts)

# Save the updated DataFrame
df.to_csv('sales_modified5.csv', index=False)
# Calculate delivery counts for each driver
data.to_csv('driver.csv', index=False)
