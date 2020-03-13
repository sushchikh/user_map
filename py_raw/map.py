import folium
from folium import plugins
import pandas as pd
from tqdm import tqdm

address_df = pd.read_excel('./../dats/address.xls', sheet_name='address')

print(address_df.head())

folium_map = folium.Map(location=[58.584884, 49.6247921],
                        tiles='OpenStreetMap',
                        zoom_start=13
                        )

def money_scale_definder(money):
    return {
        0 < money < 3000: '1',
        3000 < money < 6000: '2',
        6000 < money < 10000: '3',
        10_000 < money < 15_000: '4',
        15_000 < money < 20_000: '5',
        20_000 < money: '6'
    }[True]

# print(monyey_scale_definder(33500))


for i in tqdm(range(len(address_df['address']))):
    lat = address_df['lat'][i]
    long = address_df['long'][i]
    tooltip = str(address_df['name'][i]) + "   " + str(round(address_df['money'][i], 0)) + ' p.'
    marker_color = './../img/' + str(money_scale_definder(address_df['money'][i])) + '.png'
    print(marker_color)
    folium.Marker([lat, long], popup=f'<i>{tooltip}</i>', tooltip=tooltip, icon=folium.CustomIcon( icon_image=marker_color, icon_size=(8,8) )).add_to(folium_map)

folium_map.save('./../map/kirov_map.html')
