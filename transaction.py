import pandas as pd
import numpy as np 

df = pd.read_csv('sales_modified4.csv')

data=pd.read_csv('driver.csv')

df['Driver_id'] = data['total_deliveries']
np.random.randint(1, 11, size=len(df))

df.to_csv('sales_modified4.csv', index=False)