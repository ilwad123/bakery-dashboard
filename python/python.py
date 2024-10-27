import pandas as pd
from deep_translator import GoogleTranslator

data = "sales.csv"
df = pd.read_csv(data)

#replace the missing place name with the store location being dongmyeon
df['place'].fillna('Dongmyeon', inplace=True)

# Initialize the translator
translator = GoogleTranslator(source='ko', target='en')

unique_places = df['place'].unique()

# Translate unique values only
def translate(text):
    return translator.translate(text)

translation_dict = {place: translator.translate(place)
                    #using a dictionary,place is used as a key with the the translated value being the equivalent 
                    for place in unique_places
                    #go over each place in the column to be translated 
                    #place would need to be defined to make the for loop 
                    }

# Replace original 'place' values with the translated values in the dictionary 
df['place'] = df['place'].map(translation_dict)


# Fill missing values for other columns 
for column in df.columns:
    if column != "place":
        # Replace empty values with zero
        df[column].fillna(0, inplace=True)

# Drop rows with all missing values
df.dropna(how='all', inplace=True)

# Strip whitespace from column names
df.columns = df.columns.str.strip()

# Drop duplicate rows
df = df.drop_duplicates()

# Remove rows where 'total' is 0 or missing
df = df[df['total'] != 0]
df = df.dropna(subset=['total'])

# Remove specific not needed  columns
wrong_items = ['croque monsieur', 'mad garlic']
df.drop(columns=wrong_items, inplace=True)

#dongmyeon place of bakery
wrong_translated_names = {
    'hibernation': 'Dongmyeon',  
    'Postscript 1': 'Hupyeong 1-dong',
    'Postscript 2nd floor': 'Hupyeong 2-dong',
    'Pharmacist Myeongdong': 'Yagsamyeongdong',
    'Postscript 3-dong':'Hupyeong 3-dong'
}

df['place'] = df['place'].replace(wrong_translated_names)

df.columns = df.columns.str.strip()
df.to_csv('sales_modified.csv', index=False)
