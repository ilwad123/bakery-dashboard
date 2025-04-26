import googlemaps
import pandas as pd

api_key = "AIzaSyCxu5RB-Bc-gW771Z7Zn1lXOmoUcZoDdik"  
gmaps = googlemaps.Client(key=api_key)

df = pd.read_csv("sales_modified5.csv")
total_distances = {}
bakery_location = (51.441461742245764, -2.6068282186166774)
df['datetime'] = pd.to_datetime(df['datetime'])
time_window = pd.Timedelta(minutes=15)

# Function to calculate distance using Google Maps Directions API
def get_distance_google(start, end, mode='driving'):
    try:
        print(f"Requesting distance from {start} to {end} using mode: {mode}")
        # Request directions between start and end coordinates for the specified mode
        directions = gmaps.directions(start, end, mode=mode)
        
        if directions:
            #calculation to get distance in km
            distance = directions[0]['legs'][0]['distance']['value'] / 1000
            print(f"Distance: {distance} km")
            return distance
        else:
            print(f"No directions found for {start} to {end}")
            return 0
    except Exception as e:
        print(f"Error calculating distance with Google Maps: {e}")
        return 0

# Group the data by driver_id
for driver_id, driver_data in df.groupby('Driver_id'):
    print(f"Processing driver {driver_id}")
    batch = []
    # Go through each transaction
    for i, row in driver_data.iterrows():
        print(f"Processing row {i} for driver {driver_id}")
        #check if batch is empty 
        if len(batch) == 0:
            #add datarow to batch list
            batch.append(row)
        else:
             #get the datarow's datatime and get the latest batch datetime and 
            #check the difference between them 
            #compare with the time window [should be within]
            if row['datetime'] - batch[-1]['datetime'] <= time_window:
                batch.append(row)
            else:
                # Use the bakery location as the starting point
                location = [bakery_location]
                # Go through each location in the batch
                for loc in batch:
                    #normalise the coordinate data
                    coordinate = loc['location']
                    coordinate = coordinate.split(",")
                    lat_coordinate = float(coordinate[0])
                    long_coordinate = float(coordinate[1])
                    location.append((lat_coordinate, long_coordinate))
                location.append(bakery_location)  # Adds bakery location at the end as the endpoint
                
                total_distances_driver = 0
                mode = 'driving'  #mode as driving
                
                # Calculate the total distance for the batch
                for i in range(len(location) - 1):
                    #dont access the last index as it is the bakery 
                    #calculates the difference between each location 
                    total_distances_driver += get_distance_google(location[i], location[i + 1], mode)
                
                # Add the total distance to the driver's total distances
                if driver_id in total_distances:
                    total_distances[driver_id] += total_distances_driver
                else:
                    total_distances[driver_id] = total_distances_driver

                # Reset the batch and move to the next row
                batch = [row]

    # After processing all transactions for the driver, print the total distance
    print(f"Driver {driver_id}: {total_distances.get(driver_id, 0):.2f} km")

# Print all drivers' total distances after the loop ends
print("Total distances for all drivers:")
for driver_id, total_distance in total_distances.items():
    print(f"Driver {driver_id}: {total_distance:.2f} km")

transactions = pd.read_csv('performance.csv')
#make a column for total distance for each driver_id
transactions['total_distance'] = transactions['Driver_id'].map(total_distances)
transactions.to_csv('./static/data_files/performance.csv', index=False)