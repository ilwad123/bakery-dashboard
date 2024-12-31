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

# just add the total_distance for each driver 
#double check the driver total_sales right in the neo4j when u add it in 
#based on the transaction node

# total_distances = {}

# # # Calculate total distance for each driver per day
# for (driver_id, date), group in grouped:
#     group = group.sort_values(transactions['datetime'])  # Sort transactions by time
#     locations = [bakery_location]  # Start from the bakery

#     # Add transaction locations to the list
# #     for loc in group['location']:
# #         if pd.notna(loc):  # Ensure location is valid
# #             lat, lon = map(float, loc.split(','))
# #             locations.append((lat, lon))

# #     # Calculate total distance for the run
#     total_distance = 0
#     for i in range(len(locations) - 1):
#         total_distance += geodesic(locations[i], locations[i + 1]).meters

# #     # Add to the total_distances dictionary
# #     if driver_id not in total_distances:
# #         total_distances[driver_id] = 0
# #     total_distances[driver_id] += total_distance

# # # Convert the results to a DataFrame
# # distance_df = pd.DataFrame(
# #     [{'Driver_id': driver_id, 'total_distance': dist} for driver_id, dist in total_distances.items()]
# # )

# # # Save to CSV
# # distance_df.to_csv('performance.csv', index=False)

# # print("Total distances calculated and saved to driver_total_distances.csv.")
