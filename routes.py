from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import folium
from folium.plugins import HeatMap
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create the folium map
data = "sales_modified5.csv"
df = pd.read_csv(data)
df[['latitude', 'longitude']] = df['location'].str.split(',', expand=True)
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)

m = folium.Map(location=[51.441461742245764, -2.6068282186166774], zoom_start=12)
HeatMap(df[['latitude', 'longitude']].values, radius=15).add_to(m)

# Save the map as an HTML file
m.save("geospatial_heatmap.html")


