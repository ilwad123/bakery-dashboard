import requests

# URL for the Django view, e.g., http://localhost:8000/get_data/
url = 'http://localhost:8000/get_data/'

# Send a GET request to the Django view
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response from Django
    data = response.json()
    
    # Access the data returned by the Django view
    print("Week Day:", data['week_day'])
    print("Hour:", data['hour'])
    print("Volume of Sales:", data['volume_of_sales'])
else:
    print("Error: Unable to fetch data. Status code:", response.status_code)
