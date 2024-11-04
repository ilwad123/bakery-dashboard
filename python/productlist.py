import pandas as pd

# Load the original CSV
df = pd.read_csv('sales_modified.csv')

# Create lists to store the product names and quantities for each row
product_names_list = []
quantities_product_list = []

# Iterate through each row
for index, row in df.iterrows():
    # Initialize lists to collect product names and quantities for the current row
    product_names = []
    quantities_product = []
    for column in df.columns[4:]: 
        if row[column]  > 0:
            product_names.append(column)
            quantities_product.append(row[column])
    # Append the collected data to the main lists
    product_names_list.append(product_names)
    quantities_product_list.append(quantities_product)

# Add the new columns to the DataFrame
df['product_names'] = product_names_list
df['quantities_product'] = quantities_product_list

# Drop the original product columns
df = df.drop(columns=df.columns[4:-2])

#rename place as location 
df = df.rename(columns={'location': 'place'})
df.columns = df.columns.str.strip()
# Save the modified DataFrame to a new CSV file
df.to_csv('sales_modified2.csv', index=False)

print("file")
