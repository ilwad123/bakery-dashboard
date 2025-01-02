import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#its in json format
heatmap_data = 
# Plot the heatmap for the date and time of the total sales from django views.py
plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt="d")
plt.title('Heatmap of Login Activity for HR Role Users by Hour')
plt.xlabel('Hour of the Day (0-23)')
plt.ylabel('User')
plt.show()