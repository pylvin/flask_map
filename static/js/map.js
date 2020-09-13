ymaps.ready(function () {
    var geolocation = ymaps.geolocation,
        myPlacemark,myMap = new ymaps.Map('map', {
            center: [55, 34],
            zoom: 10
        }, {
            searchControlProvider: 'yandex#search'
        });

    // Сравним положение, вычисленное по ip пользователя и
    // положение, вычисленное средствами браузера.
    geolocation.get({
        provider: 'auto',
        mapStateAutoApply: true
    }).then(function (result) {
        // Красным цветом пометим положение, вычисленное через ip.
        result.geoObjects.options.set('preset', 'islands#redCircleIcon');
        result.geoObjects.get(0).properties.set({
            balloonContentBody: 'Мое местоположение'
        });
        myMap.geoObjects.add(result.geoObjects);
    });
    myMap.events.add('click', function (e) {
        var coords = e.get('coords');
        setCrdnts(coords)
        // Если метка уже создана – просто передвигаем ее.
        if (myPlacemark) {
            myPlacemark.geometry.setCoordinates(coords);
        }
        // Если нет – создаем.
        else {
            myPlacemark = createPlacemark(coords);
            myMap.geoObjects.add(myPlacemark);
            // Слушаем событие окончания перетаскивания на метке.
            myPlacemark.events.add('dragend', function () {
                getAddress(myPlacemark.geometry.getCoordinates(),"");
            });
        }
        getAddress(coords,"");
    });

    // Создаем маркер для активной локации
    $(".item").click(function (){
        var lng = Number($(this).find('td').eq(1).text())
        var lat = Number($(this).find('td').eq(2).text())
        var name_geolocation = $(this).find('td').eq(0).text()
        $(".item").removeClass("active")
        $(this).addClass("active")
        setItemCoords(lng,lat,name_geolocation)
    })
    function setItemCoords(lng,lat,name_geolocation){
        var coords = [lng,lat]
        setCrdnts(coords)
        // Если метка уже создана – просто передвигаем ее.
        if (myPlacemark) {
            myPlacemark.geometry.setCoordinates(coords);
        }
        // Если нет – создаем.
        else {
            myPlacemark = createPlacemark(coords);
            myMap.geoObjects.add(myPlacemark);
            // Слушаем событие окончания перетаскивания на метке.
            myPlacemark.events.add('dragend', function () {
                getAddress(myPlacemark.geometry.getCoordinates());
            });
        }
        getAddress(coords,name_geolocation);
    }

    // Создание метки.
    function createPlacemark(coords) {
        return new ymaps.Placemark(coords, {
            iconCaption: 'Поиск ...',
        }, {
            preset: 'islands#violetDotIconWithCaption',
            draggable: true,
        });
    }

    // Определяем адрес по координатам (обратное геокодирование).
    function getAddress(coords,name_gelocation) {
        ymaps.geocode(coords).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0);
            if (name_gelocation.length===0){
                myPlacemark.properties
                    .set({
                        // Формируем строку с данными об объекте.
                        iconCaption: [
                            // Название населенного пункта или вышестоящее административно-территориальное образование.
                            firstGeoObject.getLocalities().length ? firstGeoObject.getLocalities() : firstGeoObject.getAdministrativeAreas(),
                            // Получаем путь до топонима, если метод вернул null, запрашиваем наименование здания.
                            firstGeoObject.getThoroughfare() || firstGeoObject.getPremise()
                        ].filter(Boolean).join(', '),
                        // В качестве контента балуна задаем строку с адресом объекта.
                        balloonContent: firstGeoObject.getAddressLine(),
                    });
            }
            else{
                myPlacemark.properties.set('iconCaption',name_gelocation);
            }
        });
    }

    // Добавляем новое значение в input'ы
    function setCrdnts(coords){
        $("#lng").val(coords[0])
        $("#lat").val(coords[1])
    }

    // Инициализация для каждой странницы
    function initSetItem(){
        var path = window.location.pathname
        var lng,lat,name_geolocation;
        switch (true){
            case path.includes("items"):
                var item = $(".item").eq(0)
                item.addClass("active")
                lng = Number(item.find('td').eq(1).text())
                lat = Number(item.find('td').eq(2).text())
                name_geolocation = item.find('td').eq(0).text()
                setItemCoords(lng,lat,name_geolocation)
                break;
            case path.includes("update"):
                lng = Number($("#new_lng").val())
                lat = Number($("#new_lat").val())
                name_geolocation = $("#new_name").val()
                setItemCoords(lng,lat,name_geolocation)
                break
        }

    }
    initSetItem()
});

