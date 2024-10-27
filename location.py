import pandas as pd
import googlemaps
import random

#finish this file to generate random location for the column
#there are neighbourhoods?
# Load the original CSV
df = pd.read_csv('sales_modified3.csv')

df.to_csv('sales_modified4.csv', index=False)
