/* Это основной код, который будет загружать букмарклет.
Он отслеживает, была ли загружена jQuery на текущем сайте, и, если не была, загружает ее.
Если библиотека уже была подключена, код выполняет функцию bookmarklet() */
(function(){
  var site_url = 'https://752d3d1d8766.ngrok.io/'; // URL сайта
  var static_url = site_url + 'static/';           // URL статических файлов
  var min_width = 100;  // минимальные ширина и высота в пикселях для картинок,
  var min_height = 100; // которые будет загружать букмарклет

  function bookmarklet(msg) {
    /* загружаем стили bookmarklet.css, добавляя случайное число
    для предотвращения кеширования стилей браузером */
    const css = $('<link>');
    css.attr({
      rel: 'stylesheet',
      type: 'text/css',
      href: static_url + 'css/bookmarklet.css?r=' + Math.floor(Math.random()*99999999999999999999)
    });
    $('head').append(css);

    /* добавляем HTML-элемент в <body> текущего сайта;
    этот элемент содержит <div> с изображениями, найденными на сайте */
    const box_html = '<div id="bookmarklet"><a href="#" id="close">&times;</a><h1>Выберите изображение:</h1><div class="images"></div></div>';
    $('body').append(box_html);

    /* добавляем событие, которое удаляет HTML (box_html) из документа сайта, когда пользователь
    кликает на кнопку закрытия блока.
    Используем селекторs #bookmarklet и #close, чтобы найти элемент с ID close, у которого есть
    родительский элемент с ID bookmarklet.
    Селекторы jQuery позволяют нам находить HTML-элементы. Они возвращают все подходящие объекты. */
    $('#bookmarklet #close').click(function(){
       $('#bookmarklet').remove();
    });

    /* После загрузки CSS-стилей и HTML-кода для букмарклета необходимо найти все изображения на тек>
    находим картинки на текущем сайте и вставляем их в окно букмарклета */
    $.each($('img[src$="jpg"]'), function(index, image) { // селектор img[src$="jpg"], чтобы найти все <img>-элементы,
                                                          // у которых значение атрибута src заканчивается на jpg.
                                                          // Так мы найдем все JPEG-изображения на текущем сайте. Для итерации по ним обращаемся к методу each
      // Все изображения, большие по ширине и высоте, чем заданные min_width и min_height, добавляем в наш контейнер <div class="images">
      if ($(image).width() >= min_width && $(image).height() >= min_height)
      {
        image_url = $(image).attr('src');
        $('#bookmarklet .images').append('<a href="#"><img src="'+ image_url +'" /></a>');
      }
    });

    // Когда изображение выбрано, добавляем его в список сохраненных картинок на нашем сайте.
    $('#bookmarklet .images a').click(function(e){          // привязываем обработчик события click на ссылку изображения
      selected_image = $(this).children('img').attr('src'); // когда пользователь кликает на изображение, сохраняет адрес картинки в переменную selected_image
      // Скрываем букмарклет
      $('#bookmarklet').hide(); // скрывает букмарклет
      // Открываем новое окно с формой сохранения изображения
      window.open(site_url +'images/create/?url=' // открывает новую вкладку браузера с GET-параметрами (передает заголовок страницы и URL картинки)
                  + encodeURIComponent(selected_image)
                  + '&title='
                  + encodeURIComponent($('title').text()),
                  '_blank');
    });
  };

  // Проверка на подключение jQuery
  if(typeof window.$ != 'undefined') {
    bookmarklet();
  } else {
    // Проверяем, что атрибут $ окна не занят другим объектом.
    var conflict = typeof window.$ != 'undefined';
    // Создание тега <script> с загрузкой jQuery.
    var script = document.createElement('script');
    script.src = '/static/jquery-3.6.0.min.js';
    // Добавление тега в блок <head> документа
    document.head.appendChild(script);
    // Добавление возможности использовать несколько попыток для загрузки jQuery.
    var attempts = 15;
    (function(){
      // Проверка, подключена ли jQuery
      if(typeof window.$ == 'undefined') {
        if(--attempts > 0) {
          // Если не подключена, пытаемся снова загрузить
          window.setTimeout(arguments.callee, 250)
        } else {
          // Выводим сообщение, если превышено число попыток загрузки jQuery
          alert('Превышено число попыток загрузки jQuery')
        }
      } else {
          bookmarklet();
      }
    })();
  }
})()
