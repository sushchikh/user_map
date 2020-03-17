// Как только будет загружен API и готов DOM, выполняем инициализацию
ymaps.ready(init);

// Инициализация и уничтожение карты при нажатии на кнопку.
function init () {
    var myMap;
    var users_less_3k;

    myMap = new ymaps.Map('map', {
        center: [55.010251, 82.958437], // Новосибирск
        zoom: 9,
        controls: ['smallMapDefaultSet']
    }, {
        searchControlProvider: 'yandex#search'
    });





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


}