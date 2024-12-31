import pandas as pd

# Load the original CSV
df = pd.read_csv('sales_modified4.csv')

neighborhoods = {
    'Dongmyeon': 'City Centre',
    'Hyoja 3-dong': 'Clifton',
    'Hupyeong 1-dong': 'Cotham',
    'Hupyeong 2-dong': 'Montpelier',
    'Seoksa-dong': 'Stokes Croft',
    'Soyang-dong': 'Gloucester Road',
    'Toegye-dong': 'Bedminster',
    'Hupyeong 3-dong': 'Southville',
    'Shin Sa Udon': 'Easton',
    'Gangnam-dong': 'St George',
    'Hyoja 1-dong': 'Barton Hill',
    'Jo-un-dong': 'Lawrence Hill',
    'Kyodong': 'Redfield',
    'Hyoja 2-dong': 'Totterdown',
    'Yagsamyeongdong': 'Kingsdown',
    'Geunhwa-dong': 'Ashley Down',
    'Dongnae-myeon': 'Old Market',
    'Sindong-myeon': 'Brislington'
}
#replace the names in the columns with the right neighborhoods
df['place'] = df['place'].replace(neighborhoods)

for index,row in df.iterrows():
    total=row['total']
    df.at[index, 'total'] = total / 1000


df.to_csv('sales_modified4.csv', index=False)
