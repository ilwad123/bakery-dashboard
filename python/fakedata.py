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

#last three orders left them as pending
df.loc[df.index[-3:], 'Order status'] ='Pending'

#when a new transaction is added make it as pending until changed 

df.to_csv('sales_modified3.csv', index=False)
