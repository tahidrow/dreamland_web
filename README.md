# dreamland_web
DreamLand MUD: static web site pages and searcher Django app.

## Подготовка окружения

Здесь описаны шаги, которые необходимо проделать один раз для инициализации окружения.
Инструкция проверялась на свежепоставленной Ubuntu 16.04, в других системах команды могут отличаться, а необходимые пакеты уже присутствовать.

### Инициализация питонового окружения
Необходим Python версии от 2.7 и его система управления пакетами (pip):
```
sudo apt-get update
sudo apt-get install python python-pip
```
Создать и активировать виртуальное окружение (имя - любое):
```
pip install virtualenv
virtualenv django-env 
. django-env/bin/activate
```
Инсталлировать необходимые пакеты внутри виртуального окружения:
```
pip install django
pip install djangorestframework
pip install django-filter==1.1.0
pip install django-cors-headers
```
### Инициализация проекта
Скачать исходники и инициализировать базу данных:
```
sudo apt-get install git
git clone https://github.com/dreamland-mud/dreamland_web.git
cd dreamland_web/website
./manage.py migrate
```
Создать локального админа:
```
./manage.py createsuperuser
```

### Генерация сайта из исходников
Установить утилиту для XSLT-процессинга
```
sudo apt-get install xsltproc
```
Сгенерировать страницы из исходников (будет жаловаться на ненайденные файлы, но для локального тестирования это неважно):
```
cd dreamland_web/static
./make-all.sh
```

## Локальное тестирование

### Запуск локального django-сервера
Каждый раз перед началом работы необходимо будет выполнить два шага: активировать виртуальное окружение и запустить в нем сервер.
```
. django-env/bin/activate
cd dreamland_web/website
./manage.py runserver
```
После этого можно пользоваться админ-интерфейсом и тестировать поисковые запросы, зайдя на http://localhost:8000/admin.
Также через этот интерфейс можно создать несколько экземпляров брони и оружия, чтобы было, что отображать в таблице.

Убедиться, что поисковые запросы из JS идут на локальный сервер, а не на официальный сайт, установив 
переменную внутри dreamland_web/static/js/searcher.js:
```
var appUrl = 'http://127.0.0.1:8000/searcher-api'
```

### Запуск локального сайта
В браузере заходим на file:///path/to/dreamland_web/static/index.html для заглавной страницы или на file:///path/to/dreamland_web/static/searcher.html для поисковика

### Создание тестовых данных для поисковика

Для тестирования поисковика можно создать один-два экземпляра, например, оружия через админ-панель (см. выше).
Однако для полноценной работы понадобится настоящая база данных. Информация обо всех предметах
сохранятся в CSV файл с помощью команды, выполненной изнутри мира, а затем загружается в базу.

Вы можете сгенерировать CSV файлы на основе тех зон, которые выложены в открытом доступе
(см. репозитории [dreamland_code](https://github.com/dreamland-mud/dreamland_code.git) и [dreamland_world](https://github.com/dreamland-mud/dreamland_world.git)).
набрав изнутри мира команды
```
searcher weapon
searcher magic
searcher armor
searcher pets
```
Результатом их исполнения будут четыре файла с расширением csv: db_armor.csv, db_pets.csv и так далее,
созданные в каталоге runtime проекта (например, /home/dreamland/runtime/db_armor.csv).
Файлы будут сохранены в кодировке KOI8-R, а приложение хочет работать с UTF-8, поэтому необходима переконвертация:
```
iconv -c -f koi8-r -t utf-8 < /home/dreamland/runtime/db_armor.csv > /tmp/db_armor.csv
```

В дальнейшем команда ```searcher``` будет доработана, чтобы сразу сохранять в нужной кодировке.

Если файлов, основанных на этом ограниченном наборе зон, недостаточно, и нужна полная база,
обратитесь к разработчикам, и вам пришлют эти файлы по почте.


### Загрузка данных в поисковик

Для того, чтобы перенести данные из CSV файла в базу, с которой работает django-приложение, 
нужно выполнить такие команды (предварительно проинициализировав окружение питона):
```bash
cd dreamland_web/website
./manage.py loaditems /tmp/db_armor.csv true
```
1й параметр - путь к файлу, 2й параметр указывает, уничтожить ли старые данные (true) или
добавить новые поверх существующих (false). Для простоты лучше устанавливать его в true.

Для загрузки каждого типа предметов служит своя подкоманда, их список виден, если запустить
```manage.py``` без параметров:
```bash
./manage.py
...

[searcher]
    loaditems
    loadmagic
    loadweapons
```

Для хранения используется база данных sqlite, файл dreamland_web/website/db.sqlite3.
Загруженные данные сразу становятся доступными в админ-панели локального сервера (см. прерыдущие разделы).


