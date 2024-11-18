import pandas as pd
#correct the menu names with the sales csv DONEEE
# Reads the csv file add validation add n in the columns DONEEE
df = pd.read_csv("price.csv")



drinks_list = ['americano', 'caffe latte', 'milk tea', 'lemon ade', 'vanilla latte', 'berry ade']
pastry_list = ['plain bread', 'croissant', 'tiramisu croissant', 'pain au chocolat', 'almond croissant', 'pandoro', 'angbutter']
desserts_list = ['gateau chocolat', 'cheese cake', 'orange pound', 'tiramisu', 'merinque cookies']

other_foods_list = ['butter', 'jam', 'cacao deep', 'wiener']

for column in df.columns:
    #if column not place 
    if column != "place":
        #replaces empty values with zero to make it clearer 
        df[column].fillna(0, inplace=True)
    else:
        #where the column place is if empty write instead unknwn (should be the one with the most basically) 
        df['place'].fillna('unknown', inplace=True)
        
wrong_spelt_items = {
    'ice coffe': 'americano',  
    'ice coffe latter': 'caffe latte',
    'ice milk tea': 'milk tea',
    'valina latte': 'vanilla latte'
}
#replace the names in the columns with the right way 
df['Name'] = df['Name'].replace(wrong_spelt_items)


#drop the last row the delivery fee 
df.drop(df.index[-1], inplace=True)
# #make the price integer 
df['price']=df['price'].astype(int)

#validate the price is more than zero 
valid_prices= df['price']>0
invalid_prices=df['price']<=0

if valid_prices.all() :
    print("prices are all valid ")
else:
    print("WRONG PRICES:")
    print(df[invalid_prices]['Name'])
    
# Loop through each row 
#categorise each product in a new column 'Category' using the lists
for index, row in df.iterrows():
    product_name = row['Name'].strip().lower() 
    if product_name in drinks_list:
        df.at[index, 'Category'] = 'Drinks'
    elif product_name in pastry_list:
        df.at[index, 'Category'] = 'Pastry'
    elif product_name in desserts_list:
        df.at[index, 'Category'] = 'Desserts'
    elif product_name in other_foods_list:
        df.at[index, 'Category'] = 'Other Foods'
        
for index,row in df.iterrows():
    df['price'] = df['price'].astype(float) / 1000

df.columns = df.columns.str.strip()
df.to_csv('product_modified2.csv', index=False)
print("file updated")
