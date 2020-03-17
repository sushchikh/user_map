from tqdm import tqdm
from selenium import webdriver
import pandas as pd
import json
from selenium.common.exceptions import NoSuchElementException
from random import randrange


def grab_the_data():
    # raw data, without coordinates
    address_df = pd.read_excel('./../dats/strbt_orp.xls', sheet_name='Sheet1')

    # add search-request column to datafraim:
    address_df['url'] = ['https://www.google.com/maps/search/' + i for i in address_df['address']]

    # data, that we already taken:
    addresses_that_have_already_been_taken_df = pd.read_excel('./../dats/address.xls', sheet_name='address')

    print('data, that we already taken:', end=' ')
    print(len(addresses_that_have_already_been_taken_df))


    # merge data that we already taken and new data
    merged_df = pd.merge(addresses_that_have_already_been_taken_df, address_df, on=['name', 'url', 'address', 'money'], how='right')

    print('merged data: ', len(merged_df))

    driver = webdriver.Chrome()
    for i in tqdm(range(len(merged_df['name']))):
        try:
            if not(pd.isnull(merged_df['long'][i])):
                print('этот пользователь уже был', merged_df['name'][i])
                continue
            driver.get(merged_df['url'][i])
            # print('a этого пользователя еще не было:', merged_df['name'][i])
            url_with_coordinates = (driver.find_element_by_css_selector('meta[itemprop=image]').get_attribute('content'))
            merged_df['lat'][i] = (url_with_coordinates.split('?center=')[1].split('&zoom')[0].split('%2C')[0])
            merged_df['long'][i] = (url_with_coordinates.split('?center=')[1].split('&zoom')[0].split('%2C')[1])
        except IndexError:
            print('оп, ошибка, адрес не нашелся')
            merged_df['lat'][i] = 58.591730
            merged_df['long'][i] = 49.618762
        except NoSuchElementException:
            print('нас разоблачили, бежим!')
            writer = pd.ExcelWriter('./../dats/address.xls', engine='xlsxwriter')
            merged_df.to_excel(writer, sheet_name='address', index=False)
            writer.save()
            writer.close()
            driver.close()

    writer = pd.ExcelWriter('./../dats/address.xls', engine='xlsxwriter')
    merged_df.to_excel(writer, sheet_name='address', index=False)
    writer.save()
    writer.close()
    driver.close()



def from_xls_to_json():
    """
    старая версия
    :return:
    """
    address_df = pd.read_excel('./../dats/address.xls', sheet_name='address')

    output_json_dict = {
    "type": "FeatureCollection",
    "features": []
    }

    for i in tqdm(range(len(address_df['name']))):
        output_json_item = {
            "type": "Feature",
            "id": i,
            "geometry": {"type": "Point", "coordinates": [address_df['lat'][i], address_df['long'][i]], "maxHeight": "5px", "maxWidth": "5px"},
            "properties": {"balloonContentHeader": "baloon_content_header", "balloonContentBody": str(address_df['name'][i]) + str(address_df['address'][i]),
                            "balloonContentFooter": int(round(address_df['money'][i])), "clusterCaption": "cluster_caption",
                            "hintContent": str(address_df['name'][i]) + ' ' + str(int(round(address_df['money'][i]))) + ' р.'},
            "options": {"iconColor": "#ff0000", "preset": "default#image", "iconImageHref": "img/1.png"}
        }
        output_json_dict["features"].append(output_json_item)

    with open('./../yandex_map/address.json', 'w', encoding="utf-8") as json_file:
        json.dump(output_json_dict, json_file, ensure_ascii=False)


def make_js_file():
    header = """
// Дождёмся загрузки API и готовности DOM.
ymaps.ready(init);
    var myMap;
    var users_less_3k;
    
    
function init () {
    // Создание экземпляра карты и его привязка к контейнеру с
    // заданным id ("map").
    myMap = new ymaps.Map('map', {
        center: [58.584755, 49.624913], // Киров, Пугачева 1
        zoom: 13,
        controls: ['smallMapDefaultSet']
    }, {
        searchControlProvider: 'yandex#search'
    });



    // создаем метки
    myGeoObject = new ymaps.GeoObject({
            // Описание геометрии.
            geometry: {
                type: "Point",
                coordinates: [58.584755, 49.624913]
            }
        });


    // добавляем метку на карту
    myMap.geoObjects
    """
    footer = """
        .add(new ymaps.Placemark([58.584755, 49.62491], {
            balloonContent: '<b>Пугачева 1</b>', 
            hintContent: '<b>Пугачева 1</b>'
}, {
            iconLayout: 'default#image', 
            iconImageHref: 'img/strbt2.png', 
            iconImageSize: [15, 15],
            iconImageOffset: [-10, -10]
}))

        .add(new ymaps.Placemark([58.638823, 49.593275], {
            balloonContent: '<b>Дзержинского, 79А</b>', 
            hintContent: '<b>Дзержинского, 79А</b>'
}, {
            iconLayout: 'default#image', 
            iconImageHref: 'img/strbt2.png', 
            iconImageSize: [15, 15],
            iconImageOffset: [-10, -10]
}))

        .add(new ymaps.Placemark([58.547177, 50.057247], {
            balloonContent: '<b>Мира, 57</b>', 
            hintContent: '<b>Мира, 57</b>'
}, {
            iconLayout: 'default#image', 
            iconImageHref: 'img/strbt2.png', 
            iconImageSize: [15, 15],
            iconImageOffset: [-10, -10]
}))

        .add(new ymaps.Placemark([61.644343, 50.825664], {
            balloonContent: '<b>Сысольское шоссе, 29</b>', 
            hintContent: '<b>Сысольское шоссе, 29</b>'
}, {
            iconLayout: 'default#image', 
            iconImageHref: 'img/strbt2.png', 
            iconImageSize: [15, 15],
            iconImageOffset: [-10, -10]
}))
    
}

// -------------------------------------------------------------------------
users_less_3k = 1;
$('#button_3k').bind({
    click: function () {
        if (users_less_3k == 1) {
            $("#button_3k").attr('value', 'Обновить 3k');
            $("#collector").attr('value', '11.png');
            users_less_3k = 11;

            myMap.destroy();// Деструктор карты
            myMap = null;

            myMap = new ymaps.Map('map', {
                center: [55.010251, 82.958437], // Новосибирск
                zoom: 9,
                controls: ['smallMapDefaultSet']
            }, {
                searchControlProvider: 'yandex#search'
            });

        }
        else {
            $("#button_3k").attr('value', 'Обновить 3k');
            users_less_3k = 1;
            $("#collector").attr('value', '1.png');
            myMap.destroy();// Деструктор карты
            myMap = null;

            myMap = new ymaps.Map('map', {
                center: [55.010251, 82.958437], // Новосибирск
                zoom: 9,
                controls: ['smallMapDefaultSet']
            }, {
                searchControlProvider: 'yandex#search'
            });
        }
    }
});
//-------------------------------------------------------------------------------

function setTypeAndPan () {
    // Меняем тип карты на "Гибрид".
    //myMap.setType('yandex#hybrid');
    // Плавное перемещение центра карты в точку с новыми координатами.
    myMap.panTo([58.584755, 49.62491], {
            // Задержка между перемещениями.
            delay: 1500
        });
}

function setTypeAndPan2 () {
    // Меняем тип карты на "Гибрид".
    //myMap.setType('yandex#hybrid');
    // Плавное перемещение центра карты в точку с новыми координатами.
    myMap.panTo([58.638823, 49.593275], {
            // Задержка между перемещениями.
            delay: 1500
        });
}

function setTypeAndPan3 () {
    // Меняем тип карты на "Гибрид".
    //myMap.setType('yandex#hybrid');
    // Плавное перемещение центра карты в точку с новыми координатами.
    myMap.panTo([58.547177, 50.057247], {
            // Задержка между перемещениями.
            delay: 2500
        });
}

function setTypeAndPan4 () {
    // Меняем тип карты на "Гибрид".
    //myMap.setType('yandex#hybrid');
    // Плавное перемещение центра карты в точку с новыми координатами.
    myMap.panTo([61.644343, 50.825664], {
            // Задержка между перемещениями.
            delay: 3500
        });

}
"""
    address_df = pd.read_excel('./../dats/address.xls', sheet_name='address')

    repeat_index = 0

    for i in tqdm(range(len(address_df['name']))):
        if address_df['money'][i] < 800:
            continue

        iconImageHref = 'img/1.png'
        if 0 < address_df['money'][i] <= 3000:
            iconImageHref = 'img/1.png'
        elif 3000 < address_df['money'][i] <= 6000:
            iconImageHref = 'img/2.png'
        elif 6000 < address_df['money'][i] <= 9000:
            iconImageHref = 'img/3.png'
        elif 9000 < address_df['money'][i] <= 20000:
            iconImageHref = 'img/4.png'
        elif 20000 < address_df['money'][i] <= 40000:
            iconImageHref = 'img/5.png'
        elif 40000 < address_df['money'][i]:
            iconImageHref = 'img/6.png'

        money_format = str('{0:,}'.format(int(address_df['money'][i])).replace(',', ' '))  # форматируем продажи

        if (str(address_df['long'][i]) in header) and (str(address_df['lat'][i]) in header):
            repeat_index += 1
            print('такой адрес уже был', address_df['address'][i])
            address_df['lat'][i] = address_df['lat'][i] + float("0.0001" + str(randrange(5)))
            address_df['long'][i] = address_df['long'][i] + float("0.0001" + str(randrange(5)))

        balloon_content = "<b>" + str(address_df['name'][i]) + "</b>" + "<br>" + str(address_df['address'][i]) + "<br>" + money_format + " p."
        hint_content = balloon_content
        marker_coordinates = f"        .add(new ymaps.Placemark([{address_df['lat'][i]}, {address_df['long'][i]}]," + " {" + "\n"
        marker_content= ("            balloonContent: '" + f"{balloon_content}', \n"
                                               f"            hintContent: '" + f"{hint_content}'" + "\n}, {" +
                                                f"\n            iconLayout: 'default#image', \n            iconImageHref: '{iconImageHref}', \n" +"            iconImageSize: [6, 6],\n            iconImageOffset: [-6, -6]\n}))\n")
        header += marker_coordinates + marker_content

    print('повторившихся позиций на все три города:', repeat_index)
    with open('./../yandex_map/mapbasics.js', 'w', encoding='utf-8') as js_file:
        js_file.write(header + footer)

# grab_the_data()
# from_xls_to_json()
make_js_file()