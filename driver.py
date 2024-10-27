
from faker import Faker
import pandas as pd
import random
#finish the file (Sunday)
faker = Faker()
df = pd.read_csv('sales_modified3.csv')
#find out the number of rows in the csv 
rows=len(df)
print(rows)

df.drop(df.columns[0:],inplace=True)

latitude = round(random.uniform(37.450, 37.650), 6)  # Latitude range for Seoul
longitude = round(random.uniform(126.850, 127.100), 6)  # Longitude range for Seoul
for i in range(0, 10):
    df['Driver_id']= i
    df['Driver_name']=faker.name()
    df['avgDelivTime']=faker.time()
    df['total_deliveries']= rows
    df['driver_location']=(latitude,longitude)

df.to_csv('driver.csv', index=False)