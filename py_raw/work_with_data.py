from tqdm import tqdm
from selenium import webdriver
import pandas as pd




address_df = pd.read_excel('./../dats/strbt_orp.xls', sheet_name='Sheet1')  # raw data, without coordinates
address_df['url'] = ['https://www.google.com/maps/search/' + i for i in address_df['address']]  # add search-request

# data, that we already taken:
addresses_that_have_already_been_taken_df = pd.read_excel('./../dats/address.xls', sheet_name='address')

print('data, that we already taken:', end=' ')
print(len(addresses_that_have_already_been_taken_df))


# merge data that we already taken and new data
merged_df = pd.merge(addresses_that_have_already_been_taken_df, address_df, on=['name', 'url', 'address', 'money'], how='right')

print('merged data: ', len(merged_df))


driver = webdriver.Chrome()
for i in tqdm(range(len(merged_df['name']))):
    if not(pd.isnull(merged_df['long'][i])):
        print('этот пользователь уже был', merged_df['name'][i])
        continue
    driver.get(merged_df['url'][i])
    print('a этого пользователя еще не было:', merged_df['name'][i])
    url_with_coordinates = (driver.find_element_by_css_selector('meta[itemprop=image]').get_attribute('content'))
    merged_df['lat'][i] = (url_with_coordinates.split('?center=')[1].split('&zoom')[0].split('%2C')[0])
    merged_df['long'][i] = (url_with_coordinates.split('?center=')[1].split('&zoom')[0].split('%2C')[1])

writer = pd.ExcelWriter('./../dats/address.xls', engine='xlsxwriter')
merged_df.to_excel(writer, sheet_name='address', index=False)
writer.save()
writer.close()


driver.close()

