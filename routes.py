import googlemaps
import pandas as pd

# Initialize Google Maps client
api_key = "AIzaSyCxu5RB-Bc-gW771Z7Zn1lXOmoUcZoDdik"  # Replace with your API key
gmaps = googlemaps.Client(key=api_key)

transactions = pd.read_csv('sales_modified5.csv')

