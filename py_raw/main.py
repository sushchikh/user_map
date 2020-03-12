from tqdm import tqdm
from selenium import webdriver
import pandas as pd
import folium
from folium import plugins
import xlsxwriter

#
# pd.set_option('display.max_columns', 60)  # устанавливаем видимость 60 столбцов в датасетах панадаса
# acnc_df = pd.read_excel('./../dats/datadotgov_main.xlsx', keep_default_na=False,)  # пустота вместо NaN
# # создаем копию датафрема, но только сортированную по городу мельбурн, причем так, чтобы вошли все записи
# # создержащие в себе "melbourn"
# mel_df = acnc_df[acnc_df.Town_City.str.contains('melbourne', case=False)][['ABN', 'Charity_Legal_Name', 'Address_Line_1', 'Address_Line_2', 'Address_Line_3', 'Town_City', 'State', 'Postcode', 'Country', 'Date_Organisation_Established', 'Charity_Size']].copy()
# # добавляем новый столбец с полным адресом
# mel_df['Full_Address'] = mel_df['Address_Line_1'].str.cat( mel_df[['Address_Line_2', 'Address_Line_3', 'Town_City']], sep=' ')
#
# # удаляем строки, содержащие в себе адреса с "po box", это кривые адреса
# mel_df = mel_df[~mel_df.Full_Address.str.contains('po box', case=False)].copy()
#
# # меняем все знаки "/" на пробелы
# mel_df.Full_Address = mel_df.Full_Address.str.replace('/', ' ')
#
# # создаем столбец с поисковой строкой, где добавдяем к адресу ссылку
# mel_df['Url'] = ['https://www.google.com/maps/search/' + i for i in mel_df['Full_Address'] ]
#
#
#
# url_with_coordinates = []


address_df = pd.read_excel('./../dats/kirov.xlsx', sheet_name='Sheet1')
address_df['url'] = ['https://www.google.com/maps/search/' + i for i in address_df['address'] ]

driver = webdriver.Chrome()
urls_with_coordinates_list = []
lat = []
long = []
for url in tqdm(address_df['url']):
    driver.get(url)
    urls_with_coordinates_list.append(driver.find_element_by_css_selector('meta[itemprop=image]').get_attribute('content'))

# TODO здесь надо написать правильный парсер со сбором данных в файл и продолжения работы если произошел обрыв

for url_item in tqdm(urls_with_coordinates_list):
    lat.append(url_item.split('?center=')[1].split('&zoom')[0].split('%2C')[0])
    long.append(url_item.split('?center=')[1].split('&zoom')[0].split('%2C')[1])


address_df['lat'] = lat
address_df['long'] = long
print(address_df.head())
driver.close()

writer = pd.ExcelWriter('./../dats/address.xls', engine='xlsxwriter')
address_df.to_excel(writer, sheet_name='address', index=False)
writer.save()
writer.close()



# for url in tqdm(mel_df.Url[:10], leave=False):
#     driver.get(url)
#     url_with_coordinates.append(driver.find_element_by_css_selector('meta[itemprop=image]').get_attribute('content'))
#
# for i in url_with_coordinates:
#     print(i)
# print(mel_df)
