import googlemaps
import pandas as pd

# Initialize Google Maps client
api_key = "AIzaSyCxu5RB-Bc-gW771Z7Zn1lXOmoUcZoDdik"  # Replace with your API key
gmaps = googlemaps.Client(key=api_key)

transactions = pd.read_csv('sales_modified4.csv')

# Function to geocode place names if needed
def geocode_address(address):
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        print(f"Geocode failed for address: {address}")
        return None

# Function to get distance between origin and destination
def get_distance(origin, destination):
    # Convert origin to a tuple if it is a string in "lat, lng" format
    if isinstance(origin, str):
        origin = tuple(map(float, origin.split(',')))  # Convert "lat, lng" string to (lat, lng) tuple

    # Geocode the destination if it’s a place name
    if isinstance(destination, str) and not ',' in destination:
        destination = geocode_address(destination)
    
    # Skip if coordinates are missing
    if origin is None or destination is None:
        print(f"Skipping due to missing coordinates: Origin={origin}, Destination={destination}")
        return 0

    # Make the request to the Google Maps Distance Matrix API
    result = gmaps.distance_matrix(origins=origin, destinations=destination, mode='driving')
    row_status = result.get('status')
    element = result['rows'][0]['elements'][0]
    element_status = element.get('status')

    if row_status == "OK" and element_status == "OK":
        return element['distance']['value']
    else:
        print(f"Error for origin: {origin}, destination: {destination}")
        return 0

# Calculate total distance for each driver
driver_distances = {}
for driver_id, group in transactions.groupby('Driver_id'):
    total_distance = 0
    for _, row in group.iterrows():
        origin = row['location']  # Origin coordinates
        destination = row['place']  # Place name to be geocoded
        distance = get_distance(origin, destination)
        if distance:
            total_distance += distance
    driver_distances[driver_id] = total_distance

# Output results
print("Driver Distances:", driver_distances)