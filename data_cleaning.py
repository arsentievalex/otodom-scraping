import pandas as pd
import requests

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)

# change number format to show comma thousand separator and remove anything after decimal
pd.options.display.float_format = '{:,.0f}'.format

df = pd.read_excel('data July 23.xlsx')


# print shape of our data
print("There are {} rows and {} columns".format(df.shape[0], df.shape[1]))

# create and fill out currency column
df.loc[df['Price'].str.contains('$', case=False), 'Currency'] = 'USD'
df.loc[df['Price'].str.contains('zł', case=False), 'Currency'] = 'PLN'
df.loc[df['Price'].str.contains('€', case=False), 'Currency'] = 'EUR'

# check how many listings are in different currencies
print(df['Currency'].value_counts())

# clean price column of currency symbols
df.loc[df['Currency'] == 'PLN', 'Price'] = df['Price'].str[:-3]
df.loc[df['Currency'] == 'USD', 'Price'] = df['Price'].str[1:]
df.loc[df['Currency'] == 'EUR', 'Price'] = df['Price'].str[:-2]

# remove space in price column
df['Price'] = df['Price'].str.replace(" ", "")

# remove numbers after a comma
df.loc[df['Price'].str.contains(','), 'Price'] = df['Price'].str.split(',').str[0]

# convert price column to integer
df = df.astype({'Price':'int'})


# clean Price per m2 column of currency symbols
df.loc[df['Currency'] == 'PLN', 'Price per m2'] = df['Price per m2'].str[:-6]
df.loc[df['Currency'] == 'USD', 'Price per m2'] = df['Price per m2'].str[1:6]
df.loc[df['Currency'] == 'EUR', 'Price per m2'] = df['Price per m2'].str[:-5]

# remove comma in one USD entry
df.loc[df['Currency'] == 'USD', 'Price per m2'] = df['Price per m2'].str.replace(',', '')

# remove space in Price per m2 column
df['Price per m2'] = df['Price per m2'].str.replace(" ", "")

# remove numbers after a comma
df.loc[df['Price per m2'].str.contains(','), 'Price per m2'] = df['Price per m2'].str.split(',').str[0]

# convert price column to integer
df = df.astype({'Price per m2':'int'})


# define a function to get an exchange rate to PLN
def get_exchage_rate(curr):
    url = 'https://api.exchangerate.host/latest?base={}&symbols=PLN'.format(curr)
    response = requests.get(url)
    data = response.json()
    rate = data['rates']['PLN']
    return rate


# get exchange rate for usd and eur
eur_rate = get_exchage_rate('EUR')
usd_rate = get_exchage_rate('USD')

# convert USD and EUR to PLN
df.loc[df['Currency'] == 'EUR', 'Price'] = round(df['Price'] * eur_rate, 0)
df.loc[df['Currency'] == 'USD', 'Price'] = round(df['Price'] * usd_rate, 0)

df.loc[df['Currency'] == 'EUR', 'Price per m2'] = round(df['Price per m2'] * eur_rate, 0)
df.loc[df['Currency'] == 'USD', 'Price per m2'] = round(df['Price per m2'] * usd_rate, 0)


# create district column and fill out with data based on listing location
df.loc[df['Location'].str.contains('Praga-Północ', case=False), 'District'] = 'Praga-Północ'
df.loc[df['Location'].str.contains('Bemowo', case=False), 'District'] = 'Bemowo'
df.loc[df['Location'].str.contains('Wilanów', case=False), 'District'] = 'Wilanów'
df.loc[df['Location'].str.contains('Białołęka', case=False), 'District'] = 'Białołęka'
df.loc[df['Location'].str.contains('Śródmieście', case=False), 'District'] = 'Śródmieście'
df.loc[df['Location'].str.contains('Ursynów', case=False), 'District'] = 'Ursynów'
df.loc[df['Location'].str.contains('Mokotów', case=False), 'District'] = 'Mokotów'
df.loc[df['Location'].str.contains('Bielany', case=False), 'District'] = 'Bielany'
df.loc[df['Location'].str.contains('Wola', case=False), 'District'] = 'Wola'
df.loc[df['Location'].str.contains('Ursus', case=False), 'District'] = 'Ursus'
df.loc[df['Location'].str.contains('Targówek', case=False), 'District'] = 'Targówek'
df.loc[df['Location'].str.contains('Ochota', case=False), 'District'] = 'Ochota'
df.loc[df['Location'].str.contains('Praga-Południe', case=False), 'District'] = 'Praga-Południe'
df.loc[df['Location'].str.contains('Żoliborz', case=False), 'District'] = 'Żoliborz'
df.loc[df['Location'].str.contains('Rembertów', case=False), 'District'] = 'Rembertów'
df.loc[df['Location'].str.contains('Włochy', case=False), 'District'] = 'Włochy'
df.loc[df['Location'].str.contains('Wawer', case=False), 'District'] = 'Wawer'
df.loc[df['Location'].str.contains('Wesoła', case=False), 'District'] = 'Wesoła'


# export cleaned data to excel
df.to_excel('cleaned_df_July.xlsx')
