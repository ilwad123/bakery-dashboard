import pandas as pd
import random
from datetime import datetime, timedelta
from datetime import date
from dateutil.relativedelta import relativedelta

# Load the original CSV
df = pd.read_csv('sales_modified2.csv')



df['datetime'] = pd.to_datetime(df['datetime'])
df['datetime'] = df['datetime'] +  pd.DateOffset(years=4)

df['Order status'] = 'Completed'

['Order status'] = 'Pending' last three should be pending
#go back try 


#when a new transaction is added make it as pending until changed 

df.to_csv('sales_modified3.csv', index=False)
