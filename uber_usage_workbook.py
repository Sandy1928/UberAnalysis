# -*- coding: utf-8 -*-
"""Uber usage workbook.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EM2c11SVexi5PlP2CzGLyb53sx4xM_Qp
"""

import pandas
import openpyxl
import pandas as pd

from google.colab import drive
drive.mount('/content/drive')
file_path = '/content/drive/MyDrive/Ubers may-july 24.xlsx'
excel_file = pd.read_excel(file_path)
df = pd.DataFrame(excel_file)

monthOrder = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
month_category = pd.CategoricalDtype(categories=monthOrder, ordered=True)

year_2024_data = df[df['Request Date (Local)'].dt.year == 2024]
monthly_trips_2024 = df.groupby([df['Request Date (Local)'].dt.strftime('%B').astype(month_category), year_2024_data['Request Date (Local)'].dt.year],observed=False)['Trip/Eats ID'].count()
print("Trips by month on 2024 \n", + monthly_trips_2024)

expenses_by_month_2024 = df.groupby([df['Request Date (Local)'].dt.strftime('%B').astype(month_category), year_2024_data['Request Date (Local)'].dt.year],observed=False)['Transaction Amount in Local Currency (incl. Taxes)'].sum()
print("Total expenses by month in 2024 \n", + expenses_by_month_2024)

expenses_by_year = df.groupby(df['Request Date (Local)'].dt.year)['Transaction Amount in Local Currency (incl. Taxes)'].sum()
print("Total expenses by year \n", + expenses_by_year)

year_2024_data = df[df['Request Date (Local)'].dt.year == 2024]
trip_counts_2024 = year_2024_data.groupby(['First Name', year_2024_data['Request Date (Local)'].dt.year,
                                      year_2024_data['Request Date (Local)'].dt.strftime('%B').astype(month_category)],observed=False)['Trip/Eats ID'].count()

trip_counts_2024.columns = {'First Name', 'Year', 'Month', 'Trip Count', 'Total amount'}

print(trip_counts_2024)

program_mor = df[df['Program'] == 'MORNING']
program_aft = df[df['Program'] == 'AFTERNOON']

monthly_trips_2024_mor = year_2024_data.groupby([df['Request Date (Local)'].dt.strftime('%B').astype(month_category),
                                             year_2024_data['Request Date (Local)'].dt.year,
                                             program_mor['Program']],observed=False)['Trip/Eats ID'].count()
monthly_trips_2024_aft = year_2024_data.groupby([df['Request Date (Local)'].dt.strftime('%B').astype(month_category),
                                             year_2024_data['Request Date (Local)'].dt.year,
                                             program_aft['Program']],observed=False)['Trip/Eats ID'].count()

print("Trips by program on 2023 \n", + monthly_trips_2024_mor)
print("Trips by program on 2023 \n", + monthly_trips_2024_aft)

#bar graph of trips taken by month
import matplotlib.pyplot as plt

x = monthOrder
y = monthly_trips_2024

plt.bar(x,y)
plt.show()

#data frame of trips taken by person by month
year_2024_data = df[df['Request Date (Local)'].dt.year == 2024]
trip_counts_2024 = year_2024_data.groupby(['First Name', year_2024_data['Request Date (Local)'].dt.year,
                                      year_2024_data['Request Date (Local)'].dt.month])['Trip/Eats ID'].count()


trip_counts_2024.columns = ['First Name', 'Year', 'Month', 'Trip Count']
print(trip_counts_2024)

#trips taken by person and their total expense
trip_counts_and_expenses = year_2024_data.groupby('First Name').agg({'Trip/Eats ID': 'count', 'Transaction Amount in Local Currency (incl. Taxes)': 'sum'})
print(trip_counts_and_expenses)

#pivot table of ripda taken by month, by person and their expense by month
pivot_table = year_2024_data.pivot_table(index='First Name', columns=year_2024_data['Request Date (Local)'].dt.strftime('%B').astype(month_category),
                                     values=['Trip/Eats ID', 'Transaction Amount in Local Currency (incl. Taxes)'],
                                     aggfunc={'Trip/Eats ID': 'count', 'Transaction Amount in Local Currency (incl. Taxes)': 'sum'}, fill_value=0)
print(pivot_table)

#pivot table of count of trips taken by person and by program
pivot_table_program = year_2024_data.pivot_table(index='First Name', columns=['Program', year_2024_data['Request Date (Local)'].dt.strftime('%B').astype(month_category)],
                                     values='Trip/Eats ID',
                                     aggfunc='count', fill_value=0)
print(pivot_table_program)

#data frame of trips taken by program by month
trip_counts_program_2024 = year_2024_data.groupby(['Program',year_2024_data['Request Date (Local)'].dt.month])['Trip/Eats ID'].count()
print(trip_counts_program_2024)

#graph of the trips taken by program by month
import matplotlib.pyplot as plt

trip_counts_program_2024.plot(x='Program', y='Trip/Eats ID')

plt.xlabel('Program')
plt.ylabel('Trip Count')
plt.title('Trip Count by Program')

plt.show()

#data frame of the count of trips taken by
trip_counts_by_name_2024 = year_2024_data.groupby('First Name',observed=False)['Trip/Eats ID'].count()

trip_counts_by_name_2024.columns = {'First Name','Trip Count'}

print(trip_counts_by_name_2024)

#graph of trips taken by month
import matplotlib.pyplot as plt

trip_counts_by_name_2024.plot(x='First name', y='Trip Count')

plt.xlabel('First name')
plt.ylabel('Trip Count')
plt.title('Trip Count by name')
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

import pandas as pd
from geopy.geocoders import Nominatim

unique_pickup_addresses = df['Pickup Address'].unique()
pickup_address_df = pd.DataFrame(unique_pickup_addresses, columns=['Unique Pickup Addresses'])
print(pickup_address_df)

# Initialize geolocator
geolocator = Nominatim(user_agent="Uber_usage_workbook", timeout=40)

# Create empty columns for latitude and longitude
pickup_address_df['latitude'] = ""
pickup_address_df['longitude'] = ""

# Iterate over the addresses and get their coordinates
for index, row in pickup_address_df.iterrows():
  try:
    location = geolocator.geocode(row['Unique Pickup Addresses'])
    if location:
      pickup_address_df.loc[index, 'latitude'] = location.latitude
      pickup_address_df.loc[index, 'longitude'] = location.longitude
      #time.sleep(30)
    else:
      print(f"Could not find coordinates for address: {row['Unique Pickup Addresses']}")
  except Exception as e:
    print(f"Error geocoding address: {row['Unique Pickup Addresses']}. Error: {e}")

print(pickup_address_df)

import folium

# Create a map centered on the mean latitude and longitude
map_center = [pickup_address_df['latitude'].mean(), pickup_address_df['longitude'].mean()]
map_obj = folium.Map(location=map_center, zoom_start=12)

# Add markers for each address
for index, row in pickup_address_df.iterrows():
  folium.Marker(
      location=[row['latitude'], row['longitude']],
      popup=row['Unique Pickup Addresses']
  ).add_to(map_obj)

# Display the map
display(map_obj)