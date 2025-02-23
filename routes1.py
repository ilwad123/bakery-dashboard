import time
import folium
from folium.plugins import HeatMap
import pandas as pd
from selenium import webdriver
from PIL import Image

# Load the dataset
data = "sales_modified5.csv"
df = pd.read_csv(data)
df[['latitude', 'longitude']] = df['location'].str.split(',', expand=True)
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)

# Create the heatmap
m = folium.Map(location=[51.441461742245764, -2.6068282186166774], zoom_start=12)
HeatMap(df[['latitude', 'longitude']].values, radius=15).add_to(m)

# Save the map as an HTML file
html_file = "geospatial_heatmap.html"
m.save(html_file)

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no GUI)
options.add_argument("--window-size=1200x800")  # Set window size

driver = webdriver.Chrome(options=options)
driver.get(f"file://{html_file}")

# Wait for the map to fully load
time.sleep(5)

# Take a screenshot
screenshot_path = "heatmap_screenshot.png"
driver.save_screenshot(screenshot_path)

# Close the browser
driver.quit()

print(f"Heatmap saved as {screenshot_path}")
