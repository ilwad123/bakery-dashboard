import pandas as pd
import googlemaps
import random

#finish this file to generate random location for the column
#there are neighbourhoods?
# Load the original CSV
df = pd.read_csv('sales.csv')
list1=df['place'].unique()
print(list1)