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
    if not (pd.isnull(address_df['long'][i])):
        lat = address_df['lat'][i]
        long = address_df['long'][i]
        tooltip = str(address_df['name'][i]) + "<br>" + str(round(address_df['money'][i], 0)) + ' p.'
        marker_color = './../img/' + str(money_scale_definder(address_df['money'][i])) + '.png'
        folium.Marker([lat, long], popup=f'<i>{tooltip}</i>', tooltip=tooltip, icon=folium.CustomIcon(icon_image=marker_color, icon_size=(8,8))).add_to(folium_map)
        folium.Marker([58.584811, 49.624792], popup='Стройбат на Пугачева 1', tooltip='Стройбат на Пугачева, 1', icon=folium.CustomIcon(icon_image='./../img/strbt2.png', icon_size=(15,15))).add_to(folium_map)
        folium.Marker([58.638811, 49.593283], popup='Стройбат на Пугачева 1', tooltip='Стройбат на Дзержинского, 79А', icon=folium.CustomIcon(icon_image='./../img/strbt2.png', icon_size=(15,15))).add_to(folium_map)
        folium.Marker([58.547225, 50.057344], popup='Стройбат на Пугачева 1', tooltip='Стройбат Чепецк, Мира, 57', icon=folium.CustomIcon(icon_image='./../img/strbt2.png', icon_size=(15,15))).add_to(folium_map)
        folium.Marker([61.644324, 50.825780], popup='Стройбат на Пугачева 1', tooltip='Стройбат в Сыктывкаре, Сысольское шоссе, 29', icon=folium.CustomIcon(icon_image='./../img/strbt2.png', icon_size=(15,15))).add_to(folium_map)



folium_map.save('./../folium_map/kirov_map.html')
