import numpy as np
import pandas as pd
import plotly.express as px


df1 = pd.read_excel('map_test.xlsx')
df2 = pd.read_csv('geo.csv')


# check how many listings are in each district
#print(df['District'].value_counts())

# see the average price per district
# df_grouped = df.groupby('District')['Price per m2'].mean().sort_values(ascending=False).round(2)
#
# print(df_grouped)


# fig = px.scatter_mapbox(df, lat='Lat', lon='Lon', color="District", size="Price")
# fig.update_layout(mapbox_style="open-street-map")
#
# fig.show()

merged = df1.merge(df2, on='District', how='left')

print(merged)