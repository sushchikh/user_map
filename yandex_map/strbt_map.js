var myMap;

// Дождёмся загрузки API и готовности DOM.
ymaps.ready(init);

function init () {
    var myMap = new ymaps.Map('map', {
            center: [58.584746, 49.624993],
            zoom: 13
        }, {
            searchControlProvider: 'yandex#search'
        }),
        objectManager = new ymaps.ObjectManager({   
            // Чтобы метки начали кластеризоваться, выставляем опцию.
            clusterize: true,
            groupByCoordinates: true,
            // ObjectManager принимает те же опции, что и кластеризатор.
            gridSize: 20,
            clusterDisableClickZoom: true
        });

    // Чтобы задать опции одиночным объектам и кластерам,
    // обратимся к дочерним коллекциям ObjectManager.
    // objectManager.objects.options.set('preset', 'islands#circleIcon');
    // objectManager.clusters.options.set('preset', 'islands#greenClusterIcons');
    myMap.geoObjects.add(objectManager);

    $.ajax({
        url: "address.json"
    }).done(function(data) {
        objectManager.add(data);
    });

}

function setTypeAndPan () {
    // Меняем тип карты на "Гибрид".
    //myMap.setType('yandex#hybrid');
    // Плавное перемещение центра карты в точку с новыми координатами.
    myMap.panTo([58.584755, 49.62491], {
            // Задержка между перемещениями.
            delay: 1500
        });
}