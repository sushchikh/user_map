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

for i in tqdm(range(len(address_df['address']))):
    lat = address_df['lat'][i]
    long = address_df['long'][i]
    tooltip = address_df['name'][i]
    folium.Marker([lat, long], popup=f'<i>{tooltip}</i>', tooltip=tooltip, icon=folium.CustomIcon( icon_image='https://imgur.com/Rzs4Zpa.png', icon_size=(8,8) )).add_to(folium_map)

folium_map.save('./../map/kirov_map.html')
