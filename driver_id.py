import pandas as pd
import numpy as np
import random

# Load the data
driver = pd.read_csv("driver.csv")
sales = pd.read_csv('sales_modified4.csv')

#randomly allocate drivers 
num_of_driver=5
#based on the number of sales
#loop through each driver then add one 
sales['Driver_id'] = np.random.choice(range(1,num_of_driver+1),len(sales),replace=True)

#use this to add to the driver total_deliveries 
delivery_counts = sales['Driver_id'].value_counts().sort_index()

print(delivery_counts)
sales.to_csv('sales_modified4.csv', index=False)
print("column added")