import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime

# Setup API client with caching and retrying
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Load CSV file
df = pd.read_csv("sales_modified5.csv")  # Change to your actual file name

# Extract Latitude & Longitude from the "Location" column
df['Longitude'] = df['location'].apply(lambda x: float(x.split(',')[0].strip()))
df['Latitude'] = df['location'].apply(lambda x: float(x.split(',')[1].strip()))


# Convert "Datetime" column to proper format
df['Datetime'] = pd.to_datetime(df['datetime'])

# Initialize new column for weather data
df["Temperature"] = None

# Loop through each row to fetch weather data
for index, row in df.iterrows():
    lat, lon, timestamp = row["Latitude"], row["Longitude"], row["Datetime"]
    
    # Format the date for API request
    date_str = timestamp.strftime("%Y-%m-%d")

    # Open-Meteo API parameters
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": date_str,
        "end_date": date_str,
        "hourly": "temperature_2m"
    }
    
    # Fetch weather data
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    
    # Get hourly weather data
    hourly = response.Hourly()
    time_values = pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )
    
    temp_values = hourly.Variables(0).ValuesAsNumpy()
    
    # Find closest matching time
    closest_idx = (time_values - timestamp).abs().argmin()
    
    # Store the temperature at the closest hour
    df.at[index, "Temperature"] = temp_values[closest_idx]

# Save updated CSV
df.to_csv("updated_file.csv", index=False)
print("Weather data added successfully!")
